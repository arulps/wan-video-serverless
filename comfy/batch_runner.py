#!/usr/bin/env python3
"""Run a whole song's shot list (songs/<slug>/shots.csv, see
docs/SHOT-LIST-SPEC.md) against one or more ComfyUI hosts.

    python comfy/batch_runner.py --song songs/mazhai \
        --hosts http://a:8188,http://b:8188 --seed 30313 \
        --stop-cmd "runpodctl stop pod XYZ"

    --only V1a,V2c          only run these shot_ids
    --retry-failed          also re-run rows with status=failed (not just blank/pending)
    --dry-run               print the fully assembled prompt for each pending shot, no network
    --max-minutes N         hard wall clock; stop-cmd runs when hit
    --crf 16                SaveVideo codec quality, only if the workflow's SaveVideo node has
                             a matching input
    --workflow PATH         defaults to comfy/vace_ref2v_api.json

Prompt assembly (docs/SHOT-LIST-SPEC.md "How the runner builds the prompt"):
    world.txt line 1 (place clause) -> shot paragraph (plain, or assembled from
    ATMOSPHERE/ANGLE/SHOT/POSE/MOTION keys) -> style.txt -> world.txt lines 2+ ->
    CHARACTERS lock line(s) for `cast` -> "No text, no captions, no watermark."
    Negative = shot file's NEGATIVE: line + song/shot negative file.

Only the standard library is used (Python >= 3.10), except that this file has
no third-party imports at all -- comfy/make_ref_sheet.py is the one that
needs Pillow.
"""
import argparse
import csv
import os
import queue
import re
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import run_comfy  # noqa: E402  (comfy/run_comfy.py -- HTTP helpers, build_workflow, submit_and_wait)

# Shot text (negative prompts especially) carries non-ASCII (the tuned Chinese
# negative default). Windows' console defaults stdout/stderr to the system
# codepage (cp1252), which raises UnicodeEncodeError on those characters the
# first time a shot with that negative is logged. Force UTF-8 so logging never
# crashes the run; found in production (phase4e, songs/_selftest dry-run).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

FALLBACK_STYLE_SOURCE = os.path.join(REPO_ROOT, "prompts", "mazhai", "V2c-minnu-impatience-v3.txt")
FALLBACK_NEGATIVE = os.path.join(REPO_ROOT, "prompts", "mazhai", "NEGATIVE.txt")
PLAYBOOK = os.path.join(REPO_ROOT, "docs", "PROMPT-PLAYBOOK.md")
NO_TEXT_LINE = "No text, no captions, no watermark."

CSV_FIELDS = ["shot_id", "cast", "ref", "prompt", "duration_s", "steps", "cfg", "mode", "keyframe",
              "seed", "size", "negative", "status", "notes"]

print_lock = threading.Lock()
csv_lock = threading.Lock()
stop_event = threading.Event()


def log(*a):
    with print_lock:
        print(*a, flush=True)


# ---------------------------------------------------------------- prompt bits

LOCK_NAME_RE = re.compile(r"^([A-Z][A-Za-z0-9_-]*):")


def _parse_lock_lines(body, where):
    """Parse 'Name: lock line' blocks. A line starting 'Name:' opens a new
    character; wrapped continuation lines are joined onto it. Blank lines and
    lines starting '#' are ignored."""
    groups = {}
    cur_name, cur_lines = None, []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        mm = LOCK_NAME_RE.match(line)
        if mm:
            if cur_name:
                groups[cur_name] = " ".join(cur_lines)
            cur_name, cur_lines = mm.group(1), [line]
        elif cur_name:
            cur_lines.append(line)
        else:
            raise ValueError("%s: text before any 'Name:' lock line: %r" % (where, line[:60]))
    if cur_name:
        groups[cur_name] = " ".join(cur_lines)
    return groups


def parse_character_lines(playbook_path):
    """Extract the verbatim CHARACTERS lock lines from PROMPT-PLAYBOOK.md
    section 8, joining each character's wrapped markdown lines into one
    line. These are the channel-wide characters; a song adds or overrides
    its own in songs/<slug>/characters.txt."""
    text = open(playbook_path, encoding="utf-8").read()
    m = re.search(r"^## 8.*?\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    if not m:
        raise RuntimeError("could not find '## 8' character-lock section in " + playbook_path)
    groups = _parse_lock_lines(m.group(1), playbook_path + " section 8")
    for want in ("Mintu", "Minnu"):
        if want not in groups:
            raise RuntimeError("PROMPT-PLAYBOOK.md section 8 is missing the %s line" % want)
    return groups


def song_character_lines(song_dir, base):
    """songs/<slug>/characters.txt -- per-song character lock lines in the same
    'Name: ...' format as PROMPT-PLAYBOOK.md section 8. A name defined here
    overrides section 8 for this song; new names (Appa, Thangam, an animal) are
    added to the cast this song may use. The file is optional."""
    out = dict(base)
    p = os.path.join(song_dir, "characters.txt")
    if os.path.exists(p):
        out.update(_parse_lock_lines(open(p, encoding="utf-8").read(), p))
    return out


def extract_nth_paragraph(text, n):
    """1-indexed paragraph (blank-line-separated block) from a text file."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    if len(paras) < n:
        raise RuntimeError("expected at least %d paragraphs, found %d" % (n, len(paras)))
    return paras[n - 1]


SHOT_KEYS = ("ATMOSPHERE", "ANGLE", "SHOT", "POSE", "MOTION", "NEGATIVE")


def parse_shot_file(text):
    """Return (shot_paragraph, shot_negative). A shot file is either a plain
    paragraph (used verbatim, negative "") or KEY: value lines using
    ATMOSPHERE / ANGLE / SHOT / POSE / MOTION / NEGATIVE (values may wrap onto
    following lines; keys are case-insensitive; unknown keys are an error so a
    typo cannot silently drop a block). Assembly order is fixed:
    ATMOSPHERE. Camera placement: ANGLE. Framing: SHOT. POSE. MOTION."""
    text = text.strip()
    key_re = re.compile(r"^\s*([A-Za-z]+)\s*:\s*(.*)$")
    first = text.splitlines()[0] if text else ""
    m0 = key_re.match(first)
    if not (m0 and m0.group(1).upper() in SHOT_KEYS):
        return text, ""
    fields, cur = {}, None
    for line in text.splitlines():
        m = key_re.match(line)
        if m and m.group(1).upper() in SHOT_KEYS:
            cur = m.group(1).upper()
            fields[cur] = m.group(2).strip()
        elif m and m.group(1).isupper():
            raise ValueError("unknown shot key %r (allowed: %s)" % (m.group(1), ", ".join(SHOT_KEYS)))
        elif cur:
            fields[cur] = (fields[cur] + " " + line.strip()).strip()
    def s(k, cap=True):
        v = fields.get(k, "").strip().rstrip(".")
        return ((v[0].upper() + v[1:]) if cap else v) if v else ""
    parts = []
    if s("ATMOSPHERE"):
        parts.append(s("ATMOSPHERE") + ".")
    if s("ANGLE"):
        parts.append("Camera placement: " + s("ANGLE", cap=False) + ".")
    if s("SHOT"):
        parts.append("Framing: " + s("SHOT", cap=False) + ".")
    if s("POSE"):
        parts.append(s("POSE") + ".")
    if s("MOTION"):
        parts.append(s("MOTION") + ".")
    if s("ATMOSPHERE"):
        parts.append(s("ATMOSPHERE") + ".")   # repeated on purpose: cfg-1 sampling drops it
    if not parts:
        raise ValueError("shot file has keys but no ATMOSPHERE/ANGLE/SHOT/POSE/MOTION content")
    return " ".join(parts), fields.get("NEGATIVE", "").strip()


# Wan was trained with a 512-token umt5 context. The official Wan code hard-
# truncates the prompt there; ComfyUI's WanT5 tokenizer (min_length=512,
# max_length unbounded) sends the whole thing instead, so an over-long prompt
# is not cut -- it is out of the trained range and every detail gets a thinner
# slice of cross-attention (the "rain disappeared" mechanism). Either way the
# lock lines + NO_TEXT_LINE at the END of our prompt are the first casualties.
# Over-budget shots are refused before any GPU time unless --allow-long.
T5_TOKEN_LIMIT = 512
T5_TOKENS_PER_WORD = 1.7   # measured on the pod 2026-09-22 with the real umt5 tokenizer (T09a 283 words -> 472 tokens, S03 322 -> 558); was 1.4


def estimate_t5_tokens(text):
    return int(len(re.findall(r"\S+", text)) * T5_TOKENS_PER_WORD) + 2


def token_budget_warning(prompt_text, cast):
    """Return a warning string (or None) when the assembled prompt is near or
    over the encoder limit -- printed in --dry-run and before every submit; it
    does not block, because the estimate is approximate."""
    est = estimate_t5_tokens(prompt_text)
    n_cast = 0 if not cast or cast.strip().lower() == "none" else len([n for n in cast.split("+") if n.strip()])
    if est > T5_TOKEN_LIMIT:
        return ("OVER BUDGET ~%d tokens > %d trained context: the tail (%d character lock(s), no-text line) is what "
                "loses adherence -- shorten world/style/lock lines or split into shots with fewer characters "
                "(playbook 3b budgets)" % (est, T5_TOKEN_LIMIT, n_cast))
    if est > int(T5_TOKEN_LIMIT * 0.9):
        return "note ~%d tokens, close to the %d limit (%d cast) -- trim if the next shot adds anyone" % (est, T5_TOKEN_LIMIT, n_cast)
    return None


def characters_lines(cast, char_lines):
    """cast is 'none' (or blank), a single name, or names joined with '+'
    (e.g. 'Appa+Minnu+Mintu'). Lock lines come back in cast order, deduped."""
    cast = (cast or "").strip()
    if not cast or cast.lower() == "none":
        return []
    out, seen = [], set()
    for name in [n.strip() for n in cast.split("+") if n.strip()]:
        if name not in char_lines:
            raise ValueError(
                "unknown cast name %r (known: %s). Add it to the song's "
                "characters.txt or to PROMPT-PLAYBOOK.md section 8."
                % (name, ", ".join(sorted(char_lines)) or "<none>"))
        if name in seen:
            continue
        seen.add(name)
        out.append(char_lines[name])
    return out


def resolve_path(song_dir, p):
    if not p:
        return None
    p = p.strip()
    if not p:
        return None
    return p if os.path.isabs(p) else os.path.join(song_dir, p)


def frames_for_duration(duration_s, default_frames=81):
    """4n+1 nearest to duration_s*16 fps; default_frames (81 = 5.0s) when
    duration_s is not given."""
    if duration_s is None:
        return default_frames
    target = duration_s * 16.0
    n = round((target - 1) / 4.0)
    if n < 0:
        n = 0
    return 4 * n + 1


class SongContext:
    """Everything shared across shots in one song: paths, cached file
    contents, the character lock lines, and the base workflow dict."""

    def __init__(self, song_dir, seed, workflow_path, crf):
        self.song_dir = song_dir
        self.seed = seed
        self.world_path = os.path.join(song_dir, "world.txt")
        if not os.path.exists(self.world_path):
            sys.exit("missing required %s" % self.world_path)
        self.style_path = os.path.join(song_dir, "style.txt")
        self.default_negative_path = os.path.join(song_dir, "negative.txt")
        self._world_cache = {}
        self._style_text = None
        self.char_lines = song_character_lines(song_dir, parse_character_lines(PLAYBOOK))

        self.wf_base = __import__("json").load(open(workflow_path, encoding="utf-8"))
        self.save_node_id, self.crf_key = self._find_crf_slot()
        self.crf = crf
        if crf is not None:
            if self.crf_key is None:
                log("note: --crf %s given but the workflow's SaveVideo node has no "
                    "crf/quality-like input; leaving it alone." % crf)

    def _find_crf_slot(self):
        for nid, node in self.wf_base.items():
            if node.get("class_type") == "SaveVideo":
                for k in node.get("inputs", {}):
                    if re.search(r"crf|quality", k, re.I):
                        return nid, k
                return nid, None
        return None, None

    def world_text(self, row):
        override = resolve_path(self.song_dir, row.get("world", ""))
        path = override or self.world_path
        if path not in self._world_cache:
            self._world_cache[path] = open(path, encoding="utf-8").read()
        return self._world_cache[path]

    def style_text(self):
        if os.path.exists(self.style_path):
            return open(self.style_path, encoding="utf-8").read().strip()
        if self._style_text is None:
            src = open(FALLBACK_STYLE_SOURCE, encoding="utf-8").read()
            self._style_text = extract_nth_paragraph(src, 3)
        return self._style_text

    def negative_text(self, row):
        """Song/shot negative file, with the shot file's own NEGATIVE: line
        (if any) prepended -- per-shot pose negatives live next to the pose
        they guard against."""
        p = resolve_path(self.song_dir, row.get("negative", ""))
        if p:
            base = open(p, encoding="utf-8").read().strip()
        elif os.path.exists(self.default_negative_path):
            base = open(self.default_negative_path, encoding="utf-8").read().strip()
        else:
            base = open(FALLBACK_NEGATIVE, encoding="utf-8").read().strip()
        shot_path = resolve_path(self.song_dir, row.get("prompt", ""))
        shot_neg = ""
        if shot_path and os.path.exists(shot_path):
            _, shot_neg = parse_shot_file(open(shot_path, encoding="utf-8").read())
        return (shot_neg.rstrip(", ") + ", " + base) if shot_neg else base

    def assemble_prompt(self, row):
        """world.txt line 1 = the PLACE clause (e.g. the runsheet's INTERIOR
        clause), the rest = the WORLD block. Shot file = either a plain
        paragraph or KEY: value lines (ANGLE / SHOT / POSE / MOTION /
        ATMOSPHERE / NEGATIVE) which are assembled in the order that produced
        the keepers: atmosphere first (it is what the distilled model drops),
        then camera, framing, pose, motion."""
        world_text = self.world_text(row)
        wlines = [l for l in world_text.strip().splitlines()]
        place_clause = wlines[0].strip() if wlines else ""
        world_block = "\n".join(wlines[1:]).strip()
        shot_path = resolve_path(self.song_dir, row["prompt"])
        if not shot_path or not os.path.exists(shot_path):
            raise RuntimeError("shot paragraph file not found: %r" % shot_path)
        shot_text, _shot_neg = parse_shot_file(open(shot_path, encoding="utf-8").read())
        style_text = self.style_text()
        chars = characters_lines(row.get("cast", ""), self.char_lines)
        parts = [place_clause, shot_text, style_text, world_block] + chars + [NO_TEXT_LINE]
        return "\n\n".join(p for p in parts if p)


def shot_params(ctx, row):
    steps = int(row["steps"]) if row.get("steps", "").strip() else 6
    cfg = float(row["cfg"]) if row.get("cfg", "").strip() else 1.0
    seed = int(row["seed"]) if row.get("seed", "").strip() else ctx.seed
    size = (row.get("size", "").strip() or "1280x720").lower()
    try:
        w, h = (int(x) for x in size.split("x"))
    except Exception:
        raise RuntimeError("bad size %r (expected e.g. 1280x720)" % row.get("size"))
    duration_s = float(row["duration_s"]) if row.get("duration_s", "").strip() else None
    frames = frames_for_duration(duration_s)
    ref = resolve_path(ctx.song_dir, row.get("ref", ""))
    # `mode` column: "distilled" (default: lightx2v LoRA, lcm, steps/cfg from the row) or
    # "full" (no LoRA, uni_pc/simple, defaults steps 30 / cfg 5 unless the row sets them --
    # ~8x slower, for the shots where cfg-1 adherence is not enough: expressions, who holds what).
    mode = (row.get("mode", "") or "").strip().lower() or "distilled"
    if mode not in ("distilled", "full"):
        raise RuntimeError("bad mode %r (distilled | full)" % row.get("mode"))
    if mode == "full":
        if not row.get("steps", "").strip():
            steps = 30
        if not row.get("cfg", "").strip():
            cfg = 5.0
    return {"steps": steps, "cfg": cfg, "seed": seed, "width": w, "height": h,
            "frames": frames, "ref": ref, "mode": mode,
            # `keyframe` column: image pinned as frame 0 (VACE first-frame-to-video); the shot then
            # only has to HOLD or continue what the frame shows -- the fix for expressions the
            # sampler will not produce on cue (playbook 3d step 3). Must be the output aspect.
            "keyframe": resolve_path(ctx.song_dir, row.get("keyframe", ""))}


# --------------------------------------------------------------------- CSV

def read_shots(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        fieldnames = list(r.fieldnames or [])
        rows = [dict(row) for row in r]
    if "status" not in fieldnames:
        fieldnames = fieldnames + ["status"]
        for row in rows:
            row["status"] = ""
    return fieldnames, rows


def write_shots_atomic(csv_path, fieldnames, rows):
    d = os.path.dirname(os.path.abspath(csv_path))
    fd, tmp = None, None
    import tempfile
    fd, tmp = tempfile.mkstemp(prefix=".shots-", suffix=".csv.tmp", dir=d)
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for row in rows:
                w.writerow({k: row.get(k, "") for k in fieldnames})
        os.replace(tmp, csv_path)
    except Exception:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
        raise


def set_status(csv_path, fieldnames, rows, row, status):
    with csv_lock:
        row["status"] = status
        write_shots_atomic(csv_path, fieldnames, rows)


# --------------------------------------------------------------------- QC strip

def write_qc_strip(mp4_path, out_png):
    import shutil
    if shutil.which("ffmpeg") is None:
        log("note: ffmpeg not on PATH; skipping QC strip for", os.path.basename(mp4_path))
        return False
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    vf = "select='eq(n,0)+eq(n,20)+eq(n,40)+eq(n,60)+eq(n,80)',tile=5x1"
    cmd = ["ffmpeg", "-y", "-i", mp4_path, "-vf", vf, "-vsync", "0", "-frames:v", "1", out_png]
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        if p.returncode != 0:
            log("note: ffmpeg QC strip failed for", os.path.basename(mp4_path), "-",
                p.stdout.decode(errors="replace")[-300:])
            return False
        return True
    except Exception as e:
        log("note: ffmpeg QC strip errored for", os.path.basename(mp4_path), "-", e)
        return False


# --------------------------------------------------------------------- run one shot

def process_shot(host, ctx, row, args, csv_path, fieldnames, rows, results, out_dir, qc_dir, timeout_min):
    shot_id = row["shot_id"]
    t0 = time.time()
    try:
        prompt_text = ctx.assemble_prompt(row)
        negative_text = ctx.negative_text(row)
        warn = token_budget_warning(prompt_text, row.get("cast", ""))
        if warn:
            log("[%s] %s" % (row["shot_id"], warn))
            if warn.startswith("OVER BUDGET") and not args.allow_long:
                raise RuntimeError("refused before GPU time: prompt over the 512-token budget "
                                   "(trim per playbook 3b, or rerun with --allow-long to spend anyway)")
        p = shot_params(ctx, row)
        cast = (row.get("cast", "") or "").strip()
        if not p["ref"] and cast.lower() != "none":
            raise RuntimeError("ref is required for cast=%r but none given" % cast)
        if p["ref"] and not os.path.exists(p["ref"]):
            raise RuntimeError("ref file not found: %s" % p["ref"])

        # cast=none with no ref = plain text-to-video through VACE (no LoadImage node);
        # a room/establishing frame may still be given as ref for continuity.
        if p["keyframe"] and not os.path.exists(p["keyframe"]):
            raise RuntimeError("keyframe file not found: %s" % p["keyframe"])
        ref_name = run_comfy.upload_image(host, p["ref"]) if p["ref"] else None
        kf_name = run_comfy.upload_image(host, p["keyframe"]) if p["keyframe"] else None
        prefix = "%s-seed%d-s%d" % (shot_id, p["seed"], p["steps"])
        wf = run_comfy.build_workflow(
            ctx.wf_base, prompt=prompt_text, negative=negative_text, ref_name=ref_name,
            width=p["width"], height=p["height"], length=p["frames"], seed=p["seed"],
            steps=p["steps"], cfg=p["cfg"],
            sampler="uni_pc" if p["mode"] == "full" else "lcm", scheduler="simple", shift=5.0,
            lora=run_comfy.DEFAULT_LORA, lora_strength=1.0, no_lora=(p["mode"] == "full"), prefix=prefix)
        if kf_name:
            wf = run_comfy.add_first_frame_keyframe(wf, kf_name, p["width"], p["height"])
        if ctx.crf is not None and ctx.crf_key and ctx.save_node_id in wf:
            wf[ctx.save_node_id]["inputs"][ctx.crf_key] = ctx.crf

        log("[%s] -> %s (steps=%d cfg=%g seed=%d frames=%d %dx%d)" %
            (shot_id, host, p["steps"], p["cfg"], p["seed"], p["frames"], p["width"], p["height"]))
        result = run_comfy.submit_and_wait(host, wf, prefix, out_dir, timeout_min)
        wall_s = result["wall_s"]

        dest = result["dest"]
        json_sidecar = dest[:-4] + ".json"
        sidecar = {
            "shot_id": shot_id, "host": host, "wall_s": wall_s,
            "prompt": prompt_text, "negative": negative_text,
            "params": {"steps": p["steps"], "cfg": p["cfg"], "seed": p["seed"],
                       "width": p["width"], "height": p["height"], "length": p["frames"],
                       "mode": p["mode"],
                       "sampler": "uni_pc" if p["mode"] == "full" else "lcm", "scheduler": "simple", "shift": 5.0,
                       "lora": None if p["mode"] == "full" else run_comfy.DEFAULT_LORA, "crf": ctx.crf},
            "ref": p["ref"], "keyframe": p["keyframe"], "bytes": result["bytes"], "server_file": result["server_file"],
            "prompt_id": result["prompt_id"],
        }
        import json as _json
        _json.dump(sidecar, open(json_sidecar, "w", encoding="utf-8"), indent=1)

        strip_png = os.path.join(qc_dir, "%s-strip.png" % shot_id)
        write_qc_strip(dest, strip_png)

        set_status(csv_path, fieldnames, rows, row, "done")
        with print_lock:
            results.append({"shot_id": shot_id, "status": "done", "wall_s": wall_s, "file": dest})
        log("[%s] done in %.1fs -> %s" % (shot_id, wall_s, dest))
    except Exception as e:
        set_status(csv_path, fieldnames, rows, row, "failed")
        with print_lock:
            results.append({"shot_id": shot_id, "status": "failed", "wall_s": round(time.time() - t0, 1),
                             "file": str(e)})
        log("[%s] FAILED on %s: %s" % (shot_id, host, e))


def worker(host, work_q, ctx, args, csv_path, fieldnames, rows, results, out_dir, qc_dir, timeout_min):
    while not stop_event.is_set():
        try:
            row = work_q.get_nowait()
        except queue.Empty:
            return
        process_shot(host, ctx, row, args, csv_path, fieldnames, rows, results, out_dir, qc_dir, timeout_min)


def run_stop_cmd(cmd):
    if not cmd:
        return
    log("running --stop-cmd:", cmd)
    try:
        # shell=True so shell operators (&&, |, ...) in the command are actually
        # interpreted -- shlex.split() + shell=False previously turned "cmd1 &&
        # cmd2" into literal extra argv tokens for cmd1, silently swallowing cmd2
        # (this is why the pod never stopped itself in Phase 4g/4h: out-push ran,
        # "&& runpodctl stop pod ..." was just inert arguments to it).
        result = subprocess.run(cmd, shell=True, check=False)
        log("--stop-cmd exit code:", result.returncode)
    except Exception as e:
        log("--stop-cmd failed:", e)


def print_summary(results):
    log("")
    log("%-10s %-8s %10s  %s" % ("SHOT", "STATUS", "WALL_S", "FILE"))
    total_wall = 0.0
    for r in results:
        wall = r["wall_s"] if r["wall_s"] is not None else 0.0
        if r["status"] == "done":
            total_wall += wall
        log("%-10s %-8s %10s  %s" % (r["shot_id"], r["status"], "%.1f" % wall if r["wall_s"] is not None else "-", r["file"]))
    log("")
    log("total GPU-minutes (done shots): %.1f" % (total_wall / 60.0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--song", required=True, help="songs/<slug> folder")
    ap.add_argument("--hosts", required=True, help="comma-separated ComfyUI base URLs")
    ap.add_argument("--seed", type=int, default=30313, help="song seed, used when a row has none")
    ap.add_argument("--only", default="", help="comma-separated shot_ids to restrict to")
    ap.add_argument("--retry-failed", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--stop-cmd", default="", help="shell command run once when the queue drains")
    ap.add_argument("--max-minutes", type=float, default=None)
    ap.add_argument("--workflow", default=os.path.join(HERE, "vace_ref2v_api.json"))
    ap.add_argument("--crf", type=int, default=None)
    ap.add_argument("--timeout-min", type=int, default=60, help="per-shot ComfyUI timeout")
    ap.add_argument("--allow-long", action="store_true",
                    help="submit shots whose prompt estimate exceeds the 512-token budget instead of failing them")
    args = ap.parse_args()

    song_dir = args.song
    csv_path = os.path.join(song_dir, "shots.csv")
    if not os.path.exists(csv_path):
        sys.exit("no shots.csv at %s" % csv_path)
    fieldnames, rows = read_shots(csv_path)

    ctx = SongContext(song_dir, args.seed, args.workflow, args.crf)

    only = {s.strip() for s in args.only.split(",") if s.strip()} or None

    def is_pending(row):
        if only is not None and row["shot_id"] not in only:
            return False
        status = (row.get("status") or "").strip()
        if status == "done":
            return False
        if status == "failed":
            return args.retry_failed
        return True

    pending = [r for r in rows if is_pending(r)]

    if args.dry_run:
        if not pending:
            log("nothing pending.")
            return
        missing_refs = []
        over_budget = []
        for row in pending:
            log("=" * 70)
            log("shot_id:", row["shot_id"], " cast:", row.get("cast"))
            try:
                prompt_text = ctx.assemble_prompt(row)
                negative_text = ctx.negative_text(row)
                p = shot_params(ctx, row)
            except Exception as e:
                log("  ERROR assembling prompt:", e)
                continue
            log("--- params ---")
            log("mode=%s steps=%d cfg=%g seed=%d size=%dx%d frames=%d ref=%s ~tokens=%d" %
                (p["mode"], p["steps"], p["cfg"], p["seed"], p["width"], p["height"], p["frames"], p["ref"],
                 estimate_t5_tokens(prompt_text)))
            warn = token_budget_warning(prompt_text, row.get("cast", ""))
            if warn:
                log("  " + warn)
                if warn.startswith("OVER BUDGET"):
                    over_budget.append((row["shot_id"], estimate_t5_tokens(prompt_text)))
            # a missing sheet only surfaces at run time otherwise, so --dry-run
            # would pass a song that cannot actually shoot a single shot
            if p["ref"] and not os.path.exists(p["ref"]):
                missing_refs.append((row["shot_id"], p["ref"]))
                log("  !! REF MISSING: %s" % p["ref"])
            if p["keyframe"]:
                log("keyframe=%s%s" % (p["keyframe"], "" if os.path.exists(p["keyframe"]) else "  !! KEYFRAME MISSING"))
                if not os.path.exists(p["keyframe"]):
                    missing_refs.append((row["shot_id"], p["keyframe"]))
            elif not p["ref"] and (row.get("cast", "") or "").strip().lower() not in ("", "none"):
                missing_refs.append((row["shot_id"], "<no ref column value>"))
                log("  !! cast=%s but no ref given" % row.get("cast"))
            log("--- prompt (blocks separated by blank lines, in assembly order) ---")
            log(prompt_text)
            log("--- negative ---")
            log(negative_text)
        if over_budget:
            log("")
            log("=" * 70)
            log("%d shot(s) over the 512-token prompt budget (would be refused at run time without --allow-long):" % len(over_budget))
            log("  " + "  ".join("%s~%d" % t for t in over_budget))
        if missing_refs:
            log("")
            log("=" * 70)
            log("%d shot(s) point at a reference sheet that does not exist yet:" % len(missing_refs))
            for sid, ref in missing_refs:
                log("  %-6s %s" % (sid, ref))
            log("Build them (scripts/build_song_refs.py) before running the batch --")
            log("every one of these shots would fail at run time.")
        return

    if not pending:
        log("nothing to do (all shots done, or none matched --only).")
        run_stop_cmd(args.stop_cmd)
        return

    hosts = [h.strip() for h in args.hosts.split(",") if h.strip()]
    if not hosts:
        sys.exit("--hosts required")

    out_dir = os.path.join(song_dir, "out")
    qc_dir = os.path.join(out_dir, "_qc")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(qc_dir, exist_ok=True)

    work_q = queue.Queue()
    for row in pending:
        work_q.put(row)

    results = []
    threads = [threading.Thread(target=worker, args=(h, work_q, ctx, args, csv_path, fieldnames, rows,
                                                       results, out_dir, qc_dir, args.timeout_min),
                                 daemon=True)
               for h in hosts]

    watchdog = None
    if args.max_minutes:
        def _watchdog():
            time.sleep(args.max_minutes * 60)
            if not stop_event.is_set():
                log("--max-minutes (%s) reached; interrupting in-flight jobs and stopping." % args.max_minutes)
                stop_event.set()
                for h in hosts:
                    run_comfy.interrupt(h)
        watchdog = threading.Thread(target=_watchdog, daemon=True)
        watchdog.start()

    for t in threads:
        t.start()

    try:
        for t in threads:
            while t.is_alive():
                t.join(timeout=1.0)
    except KeyboardInterrupt:
        log("Ctrl-C: interrupting in-flight jobs on all hosts...")
        stop_event.set()
        for h in hosts:
            run_comfy.interrupt(h)
        for t in threads:
            t.join(timeout=10.0)
        print_summary(results)
        run_stop_cmd(args.stop_cmd)
        sys.exit(130)

    print_summary(results)
    run_stop_cmd(args.stop_cmd)


if __name__ == "__main__":
    main()
