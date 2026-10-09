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
    --workflow PATH         defaults to comfy/vace_ref2v_api.json (engine=vace rows);
                             engine=phantom rows use comfy/phantom_s2v_api.json

CSV `ref` = one sheet, or SEPARATE reference images joined with "|" (needs
comfy/custom_nodes/wan_vace_multiref.py on the pod for engine=vace; Phantom
encodes each image natively, max 4). `engine` = vace (default) | phantom.

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
import json
import os
import queue
import re
import signal
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import run_comfy  # noqa: E402  (comfy/run_comfy.py -- HTTP helpers, build_workflow, submit_and_wait)
import wan3_api  # noqa: E402  (comfy/wan3_api.py -- Alibaba Model Studio Wan 3.0, engine=wan3)

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

CSV_FIELDS = ["shot_id", "cast", "ref", "prompt", "duration_s", "steps", "cfg", "mode", "engine", "keyframe",
              "lastframe", "ref_labels", "audio", "seed", "size", "negative", "status", "notes"]

# `ref` column: one sheet, or SEPARATE reference images joined with "|" (one
# 16:9 tile per character; playbook 3c). Separate refs need node support: VACE
# via comfy/custom_nodes/wan_vace_multiref.py, Phantom natively.
REF_SEP = "|"
# `engine` column: which conditioning model/workflow renders the row.
# flf2v = Wan2.2-I2V-A14B first-last-frame-to-video: `keyframe` = frame 0, `lastframe` = last frame
# (blank -> the keyframe again = a seamless loop); identity comes from those stills, `ref` is unused.
# wan3 = Wan 3.0 over Alibaba's API (no ComfyUI, no pod): up to 10 `ref` images named "Image 1.." in the
# prompt (labels from `ref_labels`, else cast names + "the set"), OR `keyframe`/`lastframe` as first/last frame
# (the API forbids mixing the two). `mode` = standard | prime. Hosts are ignored: --hosts api,api,api = 3 tasks
# in parallel. Needs --max-usd (list-price estimate) and DASHSCOPE_API_KEY + DASHSCOPE_WORKSPACE_ID in env/.env.
ENGINES = {"vace": "vace_ref2v_api.json", "phantom": "phantom_s2v_api.json", "flf2v": "wan22_flf2v_api.json",
           "wan3": None}
spend_lock = threading.Lock()
SPEND = {"usd": 0.0}

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


def resolve_refs(song_dir, ref_cell):
    """The `ref` cell -> list of paths (empty when blank). '|' separates
    SEPARATE reference images."""
    return [resolve_path(song_dir, part) for part in (ref_cell or "").split(REF_SEP) if part.strip()]


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

    def __init__(self, song_dir, seed, workflow_path, crf, workflow_dir=HERE):
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
        # per-engine base workflows (comfy/<file>), loaded lazily; engine "vace" = --workflow
        self.workflow_dir = workflow_dir
        self._wf_by_engine = {"vace": self.wf_base}
        self.save_node_id, self.crf_key = self._find_crf_slot()
        self.crf = crf
        if crf is not None:
            if self.crf_key is None:
                log("note: --crf %s given but the workflow's SaveVideo node has no "
                    "crf/quality-like input; leaving it alone." % crf)

    def workflow_for(self, engine):
        if engine in ENGINES and ENGINES[engine] is None:
            return None          # API engine, no ComfyUI workflow
        if engine not in self._wf_by_engine:
            path = os.path.join(self.workflow_dir, ENGINES[engine])
            if not os.path.exists(path):
                raise RuntimeError("engine %r needs %s" % (engine, path))
            self._wf_by_engine[engine] = __import__("json").load(open(path, encoding="utf-8"))
        return self._wf_by_engine[engine]

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
    refs = resolve_refs(ctx.song_dir, row.get("ref", ""))
    # `engine` column: "vace" (default; Wan2.1-VACE-14B, one sheet or separate refs via the multi-ref node)
    # or "phantom" (Phantom-Wan-14B subject-to-video: up to 4 separate refs, encoded one by one natively).
    engine = (row.get("engine", "") or "").strip().lower() or "vace"
    if engine not in ENGINES:
        raise RuntimeError("bad engine %r (%s)" % (row.get("engine"), " | ".join(ENGINES)))
    if engine == "phantom" and len(refs) > 4:
        raise RuntimeError("phantom takes at most 4 reference images, got %d" % len(refs))
    # `mode` column: "distilled" (default: lightx2v LoRA, lcm, steps/cfg from the row) or
    # "full" (no LoRA, uni_pc/simple, defaults steps 30 / cfg 5 unless the row sets them --
    # ~8x slower, for the shots where cfg-1 adherence is not enough: expressions, who holds what).
    if engine == "wan3":
        mode = (row.get("mode", "") or "").strip().lower() or "standard"
        if mode not in wan3_api.MODELS:
            raise RuntimeError("bad mode %r for engine=wan3 (%s)" % (row.get("mode"), " | ".join(wan3_api.MODELS)))
    else:
        mode = (row.get("mode", "") or "").strip().lower() or "distilled"
        if mode not in ("distilled", "full"):
            raise RuntimeError("bad mode %r (distilled | full)" % row.get("mode"))
    if engine == "flf2v":
        d = run_comfy.FLF2V_MODES[mode]
        if not row.get("steps", "").strip():
            steps = d["steps"]
        if not row.get("cfg", "").strip():
            cfg = d["cfg"]
    elif mode == "full":
        if not row.get("steps", "").strip():
            steps = 30
        if not row.get("cfg", "").strip():
            cfg = 5.0
    keyframe = resolve_path(ctx.song_dir, row.get("keyframe", ""))
    lastframe = resolve_path(ctx.song_dir, row.get("lastframe", "")) or (keyframe if engine == "flf2v" else "")
    if engine == "flf2v" and not keyframe:
        raise RuntimeError("engine=flf2v needs a keyframe (the first frame; also the last unless lastframe is set)")
    if lastframe and engine not in ("flf2v", "wan3"):
        raise RuntimeError("lastframe is only supported by engine=flf2v and engine=wan3")
    ref_labels = []
    wan3 = None
    if engine == "wan3":
        if refs and (keyframe or lastframe):
            raise RuntimeError("engine=wan3: ref images and keyframe/lastframe cannot be combined (API rule)")
        if len(refs) > wan3_api.MAX_REFS:
            raise RuntimeError("engine=wan3 takes at most %d ref images, got %d" % (wan3_api.MAX_REFS, len(refs)))
        ref_labels = [x.strip() for x in (row.get("ref_labels", "") or "").split(REF_SEP) if x.strip()]
        cast_names = [c.strip() for c in (row.get("cast", "") or "").split("+") if c.strip() and c.strip().lower() != "none"]
        if refs and not ref_labels:
            if len(refs) == len(cast_names):
                ref_labels = cast_names
            elif len(refs) == len(cast_names) + 1:
                ref_labels = cast_names + ["the set: the place, exactly as shown"]
            else:
                raise RuntimeError("engine=wan3: %d refs for cast %r -- set ref_labels (one label per ref, joined with |)"
                                   % (len(refs), row.get("cast")))
        if refs and len(ref_labels) != len(refs):
            raise RuntimeError("engine=wan3: ref_labels has %d labels for %d refs" % (len(ref_labels), len(refs)))
        res, ratio = wan3_api.size_to_resolution(w, h)
        dur = int(round(duration_s)) if duration_s else 5
        audio_cell = (row.get("audio", "") or "").strip().lower()
        if audio_cell not in ("", "yes", "no", "true", "false", "1", "0"):
            raise RuntimeError("bad audio %r (yes | no)" % row.get("audio"))
        wan3 = {"resolution": res, "ratio": ratio, "duration": dur, "est_usd": wan3_api.estimate_usd(res, dur, mode),
                "model": wan3_api.MODELS[mode], "audio": audio_cell in ("yes", "true", "1")}
    return {"steps": steps, "cfg": cfg, "seed": seed, "width": w, "height": h,
            "frames": frames, "ref": refs[0] if len(refs) == 1 else (refs or None), "refs": refs,
            "mode": mode, "engine": engine,
            # `keyframe` column: image pinned as frame 0 (VACE first-frame-to-video); the shot then
            # only has to HOLD or continue what the frame shows -- the fix for expressions the
            # sampler will not produce on cue (playbook 3d step 3). Must be the output aspect.
            "keyframe": keyframe, "lastframe": lastframe, "ref_labels": ref_labels, "wan3": wan3}


def wan3_prompt(ctx, row, p):
    """engine=wan3 prompt: a reference legend naming Image 1..n (the API's own convention), the normal
    assembled prompt, and the shot's NEGATIVE: line as an 'Avoid:' sentence (the API has no negative prompt;
    the long song negative file is Wan2.x-specific and is not sent)."""
    shot_path = resolve_path(ctx.song_dir, row.get("prompt", ""))
    if shot_path and shot_path.endswith(".raw.txt"):
        # A *.raw.txt shot file is a complete, runsheet-assembled Wan 3.0 prompt (legend, style, world, characters,
        # scene, audio, negative already in it): sent verbatim, nothing added.
        return open(shot_path, encoding="utf-8").read().strip()
    body = ctx.assemble_prompt(row)
    legend = ""
    if p["ref_labels"]:
        legend = "Reference images: " + "; ".join("Image %d is %s" % (i + 1, lab) for i, lab in enumerate(p["ref_labels"])) + \
                 ". Keep every character exactly as in their reference image."
    elif p["keyframe"]:
        legend = "The video starts on the given first frame" + \
                 (" and ends exactly on the given last frame." if p["lastframe"] else ".") + \
                 " Keep every character exactly as it appears there."
    shot_path = resolve_path(ctx.song_dir, row.get("prompt", ""))
    shot_neg = parse_shot_file(open(shot_path, encoding="utf-8").read())[1] if shot_path and os.path.exists(shot_path) else ""
    avoid = ("Avoid: " + shot_neg.rstrip(" ,.") + ".") if shot_neg else ""
    return "\n\n".join(x for x in (legend, body, avoid) if x)


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
    # no -vsync: ffmpeg 9 (Beast) removed it, and with select+tile+-frames:v 1 it never changed the image (checked
    # pixel-identical on ffmpeg 6.1 and 7.0, 9 Oct 2026)
    cmd = ["ffmpeg", "-y", "-i", mp4_path, "-vf", vf, "-frames:v", "1", out_png]
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
        p0 = shot_params(ctx, row)
        if p0["engine"] == "wan3":
            return process_wan3_shot(ctx, row, p0, args, csv_path, fieldnames, rows, results, out_dir, qc_dir, timeout_min)
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
        if not p["refs"] and cast.lower() != "none" and p["engine"] != "flf2v":
            raise RuntimeError("ref is required for cast=%r but none given" % cast)
        for r in p["refs"]:
            if not os.path.exists(r):
                raise RuntimeError("ref file not found: %s" % r)

        # cast=none with no ref = plain text-to-video through VACE (no LoadImage node);
        # a room/establishing frame may still be given as ref for continuity.
        if p["keyframe"] and not os.path.exists(p["keyframe"]):
            raise RuntimeError("keyframe file not found: %s" % p["keyframe"])
        ref_names = [run_comfy.upload_image(host, r) for r in p["refs"]]
        ref_name = ref_names if len(ref_names) > 1 else (ref_names[0] if ref_names else None)
        if p["lastframe"] and not os.path.exists(p["lastframe"]):
            raise RuntimeError("lastframe file not found: %s" % p["lastframe"])
        kf_name = run_comfy.upload_image(host, p["keyframe"]) if p["keyframe"] else None
        if kf_name and p["engine"] not in ("vace", "flf2v"):
            raise RuntimeError("keyframe is only supported by engine=vace and engine=flf2v")
        prefix = "%s-seed%d-s%d" % (shot_id, p["seed"], p["steps"])
        if p["engine"] == "flf2v":
            d = run_comfy.FLF2V_MODES[p["mode"]]
            lf_name = kf_name if p["lastframe"] == p["keyframe"] else run_comfy.upload_image(host, p["lastframe"])
            wf = run_comfy.build_flf2v_workflow(
                ctx.workflow_for("flf2v"), prompt=prompt_text, negative=negative_text,
                start_name=kf_name, end_name=lf_name, width=p["width"], height=p["height"], length=p["frames"],
                seed=p["seed"], steps=p["steps"], cfg=p["cfg"], shift=d["shift"], sampler=d["sampler"],
                scheduler=d["scheduler"], use_lora=d["lora"], prefix=prefix)
            sampler_used, shift_used = d["sampler"], d["shift"]
            lora_used = "wan22_i2v_lightning_4step_high/low" if d["lora"] else None
        else:
            sampler_used, shift_used = ("uni_pc" if p["mode"] == "full" else "lcm"), 5.0
            lora_used = None if p["mode"] == "full" else run_comfy.DEFAULT_LORA
        if p["engine"] != "flf2v":
            wf = run_comfy.build_workflow(
                ctx.workflow_for(p["engine"]), prompt=prompt_text, negative=negative_text, ref_name=ref_name,
                width=p["width"], height=p["height"], length=p["frames"], seed=p["seed"],
                steps=p["steps"], cfg=p["cfg"],
                sampler="uni_pc" if p["mode"] == "full" else "lcm", scheduler="simple", shift=5.0,
                lora=run_comfy.DEFAULT_LORA, lora_strength=1.0, no_lora=(p["mode"] == "full"), prefix=prefix)
            if kf_name:
                wf = run_comfy.add_first_frame_keyframe(wf, kf_name, p["width"], p["height"])
        if ctx.crf is not None and ctx.crf_key and ctx.save_node_id in wf:
            wf[ctx.save_node_id]["inputs"][ctx.crf_key] = ctx.crf

        log("[%s] -> %s (engine=%s mode=%s steps=%d cfg=%g seed=%d frames=%d %dx%d refs=%d)" %
            (shot_id, host, p["engine"], p["mode"], p["steps"], p["cfg"], p["seed"], p["frames"], p["width"], p["height"], len(p["refs"])))
        result = run_comfy.submit_and_wait(host, wf, prefix, out_dir, timeout_min)
        wall_s = result["wall_s"]

        dest = result["dest"]
        json_sidecar = dest[:-4] + ".json"
        sidecar = {
            "shot_id": shot_id, "host": host, "wall_s": wall_s,
            "prompt": prompt_text, "negative": negative_text,
            "params": {"steps": p["steps"], "cfg": p["cfg"], "seed": p["seed"],
                       "width": p["width"], "height": p["height"], "length": p["frames"],
                       "mode": p["mode"], "engine": p["engine"],
                       "sampler": sampler_used, "scheduler": "simple", "shift": shift_used,
                       "lora": lora_used, "crf": ctx.crf},
            "ref": p["ref"], "refs": p["refs"], "keyframe": p["keyframe"], "lastframe": p["lastframe"], "bytes": result["bytes"], "server_file": result["server_file"],
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


def process_wan3_shot(ctx, row, p, args, csv_path, fieldnames, rows, results, out_dir, qc_dir, timeout_min):
    shot_id = row["shot_id"]
    t0 = time.time()
    try:
        for f in p["refs"] + [x for x in (p["keyframe"], p["lastframe"]) if x]:
            if not os.path.exists(f):
                raise RuntimeError("file not found: %s" % f)
        est = p["wan3"]["est_usd"]
        with spend_lock:
            if SPEND["usd"] + est > args.max_usd + 1e-9:
                raise RuntimeError("--max-usd %.2f would be exceeded (spent ~%.2f + this row ~%.2f); not submitted"
                                   % (args.max_usd, SPEND["usd"], est))
            SPEND["usd"] += est          # reserve before submitting, so parallel workers cannot overshoot
        prompt_text = wan3_prompt(ctx, row, p)
        body = wan3_api.build_request(prompt_text, refs=p["refs"], first_frame=p["keyframe"] or None,
                                      last_frame=p["lastframe"] or None, resolution=p["wan3"]["resolution"],
                                      ratio=p["wan3"]["ratio"], duration=p["wan3"]["duration"], seed=p["seed"],
                                      mode=p["mode"], prompt_extend=args.wan3_prompt_extend, audio=p["wan3"]["audio"])
        prefix = "%s-seed%d-w3%s" % (shot_id, p["seed"], "p" if p["mode"] == "prime" else "")
        dest = os.path.join(out_dir, prefix + ".mp4")
        log("[%s] -> wan3 %s %s %s %ds refs=%d first=%s last=%s est $%.2f" % (
            shot_id, p["wan3"]["model"], p["wan3"]["resolution"], p["wan3"]["ratio"], p["wan3"]["duration"],
            len(p["refs"]), bool(p["keyframe"]), bool(p["lastframe"]), est))
        result = wan3_api.render(body, dest, timeout_min=timeout_min, log=log)
        sidecar = {"shot_id": shot_id, "engine": "wan3", "wall_s": result["wall_s"], "prompt": prompt_text,
                   "params": {"model": p["wan3"]["model"], "resolution": p["wan3"]["resolution"],
                              "ratio": body["parameters"]["ratio"], "duration": p["wan3"]["duration"], "seed": p["seed"],
                              "prompt_extend": args.wan3_prompt_extend, "audio": p["wan3"]["audio"]},
                   "refs": p["refs"], "ref_labels": p["ref_labels"], "keyframe": p["keyframe"], "lastframe": p["lastframe"],
                   "task_id": result["task_id"], "usage": result["usage"], "est_usd_list_price": est, "bytes": result["bytes"]}
        json.dump(sidecar, open(dest[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        write_qc_strip(dest, os.path.join(qc_dir, "%s-strip.png" % shot_id))
        set_status(csv_path, fieldnames, rows, row, "done")
        with print_lock:
            results.append({"shot_id": shot_id, "status": "done", "wall_s": result["wall_s"], "file": dest})
        log("[%s] done in %.1fs -> %s (running list-price estimate $%.2f)" % (shot_id, result["wall_s"], dest, SPEND["usd"]))
    except Exception as e:
        set_status(csv_path, fieldnames, rows, row, "failed")
        with print_lock:
            results.append({"shot_id": shot_id, "status": "failed", "wall_s": round(time.time() - t0, 1), "file": str(e)})
        log("[%s] FAILED (wan3): %s" % (shot_id, e))


def stop_requested(args):
    """Graceful stop: a STOP file (default <song>/STOP) or SIGTERM lets the row in flight finish and
    starts no new row. Found in production (phase 6a): SIGINT sent to a runner started with
    `nohup ... &` from a non-interactive shell is ignored (inherited SIG_IGN), so the runner kept
    going into an unwanted ~$0.65 full-sampling row. `touch songs/<slug>/STOP` always works."""
    if os.path.exists(args.stop_file):
        if not stop_event.is_set():
            log("STOP file found (%s): finishing the row in flight, starting no new row." % args.stop_file)
        stop_event.set()
    return stop_event.is_set()


def worker(host, work_q, ctx, args, csv_path, fieldnames, rows, results, out_dir, qc_dir, timeout_min):
    while not stop_requested(args):
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
    ap.add_argument("--stop-file", default=None,
                    help="graceful stop: when this file exists no new row starts (default: <song>/STOP)")
    ap.add_argument("--max-usd", type=float, default=None,
                    help="engine=wan3: hard cap on the list-price estimate of this run (required for wan3 rows)")
    ap.add_argument("--wan3-prompt-extend", action="store_true",
                    help="engine=wan3: let Alibaba rewrite/extend the prompt (default off: our prompt is sent as written)")
    ap.add_argument("--allow-long", action="store_true",
                    help="submit shots whose prompt estimate exceeds the 512-token budget instead of failing them")
    args = ap.parse_args()

    song_dir = args.song
    args.stop_file = args.stop_file or os.path.join(song_dir, "STOP")
    if os.path.exists(args.stop_file) and not args.dry_run:
        os.remove(args.stop_file)      # a stale STOP from an earlier run must not end this one
        print("removed stale stop file %s" % args.stop_file, flush=True)
    # Ctrl-C must raise KeyboardInterrupt even when started in the background (SIGINT may be
    # inherited as SIG_IGN); SIGTERM = graceful stop after the row in flight.
    signal.signal(signal.SIGINT, signal.default_int_handler)
    try:
        signal.signal(signal.SIGTERM, lambda *_: (log("SIGTERM: finishing the row in flight, starting no new row."), stop_event.set()))
    except (ValueError, AttributeError):
        pass
    csv_path = os.path.join(song_dir, "shots.csv")
    if not os.path.exists(csv_path):
        sys.exit("no shots.csv at %s" % csv_path)
    fieldnames, rows = read_shots(csv_path)

    ctx = SongContext(song_dir, args.seed, args.workflow, args.crf)
    try:
        for row in rows:
            ctx.workflow_for((row.get("engine", "") or "").strip().lower() or "vace")   # fail early, before any upload
    except (KeyError, RuntimeError) as e:
        sys.exit("engine column: %s" % e)

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
        wan3_total = [0.0]
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
            log("engine=%s mode=%s steps=%d cfg=%g seed=%d size=%dx%d frames=%d ref=%s ~tokens=%d" %
                (p["engine"], p["mode"], p["steps"], p["cfg"], p["seed"], p["width"], p["height"], p["frames"],
                 (REF_SEP.join(p["refs"]) if len(p["refs"]) > 1 else p["ref"]), estimate_t5_tokens(prompt_text)))
            if len(p["refs"]) > 1:
                log("  %d SEPARATE references (%s)" % (len(p["refs"]),
                    "WanVaceToVideoMultiRef custom node" if p["engine"] == "vace" else "Phantom native"))
            warn = None if p["engine"] == "wan3" else token_budget_warning(prompt_text, row.get("cast", ""))
            if p["engine"] == "wan3":
                w = p["wan3"]
                wan3_total[0] += w["est_usd"]
                log("  wan3: %s %s %s %ds audio=%s, est $%.2f (list price); refs=%d labels=%s first=%s last=%s" % (
                    w["model"], w["resolution"], w["ratio"], w["duration"], "on" if w["audio"] else "off", w["est_usd"], len(p["refs"]),
                    p["ref_labels"], p["keyframe"] or "-", p["lastframe"] or "-"))
                prompt_text = wan3_prompt(ctx, row, p)
            if warn:
                log("  " + warn)
                if warn.startswith("OVER BUDGET"):
                    over_budget.append((row["shot_id"], estimate_t5_tokens(prompt_text)))
            # a missing sheet only surfaces at run time otherwise, so --dry-run
            # would pass a song that cannot actually shoot a single shot
            for r in p["refs"]:
                if not os.path.exists(r):
                    missing_refs.append((row["shot_id"], r))
                    log("  !! REF MISSING: %s" % r)
            if p["keyframe"]:
                log("keyframe=%s%s" % (p["keyframe"], "" if os.path.exists(p["keyframe"]) else "  !! KEYFRAME MISSING"))
                if not os.path.exists(p["keyframe"]):
                    missing_refs.append((row["shot_id"], p["keyframe"]))
                if p["engine"] == "flf2v":
                    if p["lastframe"] == p["keyframe"]:
                        log("lastframe=<same as keyframe> (seamless loop)")
                    else:
                        log("lastframe=%s%s" % (p["lastframe"], "" if os.path.exists(p["lastframe"]) else "  !! LASTFRAME MISSING"))
                        if not os.path.exists(p["lastframe"]):
                            missing_refs.append((row["shot_id"], p["lastframe"]))
            elif not p["refs"] and (row.get("cast", "") or "").strip().lower() not in ("", "none"):
                missing_refs.append((row["shot_id"], "<no ref column value>"))
                log("  !! cast=%s but no ref given" % row.get("cast"))
            log("--- prompt (blocks separated by blank lines, in assembly order) ---")
            log(prompt_text)
            log("--- negative ---")
            log(negative_text)
        if wan3_total[0]:
            log("")
            log("=" * 70)
            log("engine=wan3 rows: estimated $%.2f at list price (a launch discount may lower it); run with --max-usd >= that"
                % wan3_total[0])
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
    wan3_rows = [r for r in pending if (r.get("engine", "") or "").strip().lower() == "wan3"]
    if wan3_rows:
        if args.max_usd is None:
            sys.exit("engine=wan3 rows pending: --max-usd is required (list-price cap for this run)")
        if not wan3_api.credentials_present():
            sys.exit("engine=wan3 rows pending: DASHSCOPE_API_KEY and DASHSCOPE_WORKSPACE_ID must be set (env or .env)")

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
