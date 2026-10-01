"""Stage numbered clips and build Tamil/English rough cuts of a song from its cutplan.json.

    python comfy/song_cuts.py songs/rowboat stage [--force] [--song-folder PATH]
        copy each shot's chosen take (songs/<slug>/out/<take>) into the song folder as NN_ID_slug.mp4
        (VIDEO-PRODUCTION-STANDARD sec 8). Copies only: renders, audio masters and runsheets are never touched.
    python comfy/song_cuts.py songs/rowboat cut --lang ta|en|both [--song-folder PATH] [--src staged|out]
        lay the clips on the song's master WAV at the cutplan in-points -> <song folder>/_cuts/<NAME>-ROUGH-TA|EN.mp4
        0.4 s cross-fades, hard cuts into SFX shots, SFX clips slipped to the measured onsets, fade in/out,
        1920x1080 30 fps H.264 CRF 16 + AAC 256k 48 kHz. Shorter clips hold their last frame. Ready for CapCut polish.
Needs python 3.8+ and ffmpeg/ffprobe on PATH (Windows or Linux)."""
import argparse, json, os, re, shutil, subprocess, sys
from pathlib import Path

FPS = 30

def probe_len(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)

def load(song_dir, folder_arg):
    plan = json.load(open(Path(song_dir) / "cutplan.json", encoding="utf-8"))
    folder = Path(folder_arg) if folder_arg else Path(plan["song_folder"])
    if not folder.exists():
        sys.exit("song folder not found: %s (pass --song-folder)" % folder)
    return plan, folder

def staged_name(s):
    return "%s_%s_%s.mp4" % (s["n"], s["id"], s["slug"])

def stage(song_dir, plan, folder, force):
    missing = []
    for s in plan["shots"]:
        src = Path(song_dir) / "out" / s["take"]
        dst = folder / staged_name(s)
        if not src.exists():
            missing.append(s["take"]); continue
        if dst.exists() and not force:
            print("keep   ", dst.name); continue
        shutil.copy2(src, dst); print("staged ", dst.name, "<-", s["take"])
    if missing:
        print("not rendered yet:", ", ".join(missing))

def clip_path(song_dir, folder, s, src_mode):
    if src_mode == "out":
        return Path(song_dir) / "out" / s["take"]
    return folder / staged_name(s)

def cut(song_dir, plan, folder, lang, src_mode, out_dir=None):
    shots = [s for s in plan["shots"] if s[lang + "_in"] is not None]
    xf = float(plan.get("xfade", 0.4))
    hard = 1.0 / FPS
    t0 = shots[0][lang + "_in"]
    length = float(plan["length"][lang])
    wav = folder / plan["audio"][lang]
    if not wav.exists():
        sys.exit("audio not found: %s" % wav)
    inputs, chains, log = [], [], []
    for k, s in enumerate(shots):
        p = clip_path(song_dir, folder, s, src_mode)
        if not p.exists():
            sys.exit("clip missing for %s: %s (run 'stage' first, or --src out)" % (s["id"], p))
        start = float(s.get("slip", {}).get(lang, 0.0))
        use = s[lang + "_out"] - s[lang + "_in"]
        nxt = shots[k + 1] if k + 1 < len(shots) else None
        ov = 0.0 if nxt is None else (hard if nxt["kind"] == "sfx" else xf)
        need = use + ov
        avail = probe_len(p) - start
        take = min(avail, need)
        hold = max(0.0, need - take)
        inputs += ["-i", str(p)]
        chains.append("[%d:v]trim=start=%.4f:duration=%.4f,setpts=PTS-STARTPTS,fps=%d,"
                      "scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos,"
                      "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p,"
                      "tpad=stop_mode=clone:stop_duration=%.4f,trim=duration=%.4f,setpts=PTS-STARTPTS[c%d]"
                      % (k, start, take, FPS, hold + 0.1, need, k))
        log.append("%s %-4s in %8.3f use %6.3f slip %.3f %s%s" % (s["n"], s["id"], s[lang + "_in"], use, start,
                   "" if nxt is None else ("hard-cut" if ov == hard else "xfade %.1f" % ov),
                   " (holds last frame %.2f s)" % hold if hold > 0.05 else ""))
    cur = "c0"
    for k in range(1, len(shots)):
        prev = shots[k - 1]; s = shots[k]
        d = hard if s["kind"] == "sfx" else xf
        off = s[lang + "_in"] - t0
        chains.append("[%s][c%d]xfade=transition=fade:duration=%.4f:offset=%.4f[x%d]" % (cur, k, d, off, k))
        cur = "x%d" % k
    fin = plan["fades"][lang]
    chains.append("[%s]fade=t=in:st=0:d=%.3f,fade=t=out:st=%.3f:d=%.3f,trim=duration=%.4f[v]"
                  % (cur, fin["in"], length - fin["out"], fin["out"], length))
    name = re.sub(r"[^A-Za-z0-9]+", "-", plan["song"]).strip("-").upper()
    out_dir = Path(out_dir) if out_dir else folder / "_cuts"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / ("%s-ROUGH-%s.mp4" % (name, lang.upper()))
    graph = out_dir / ("_graph-%s.txt" % lang)
    graph.write_text(";\n".join(chains), encoding="utf-8")
    cmd = ["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-i", str(wav), "-filter_complex_script", str(graph),
           "-map", "[v]", "-map", "%d:a" % len(shots), "-t", "%.3f" % length,
           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", str(out)]
    print("\n".join(log))
    subprocess.run(cmd, check=True)
    (out_dir / ("%s-ROUGH-%s.cutlog.txt" % (name, lang.upper()))).write_text("\n".join(log) + "\n", encoding="utf-8")
    print("wrote", out, "%.3f s (audio %.3f s)" % (probe_len(out), length))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("song_dir"); ap.add_argument("action", choices=["stage", "cut"])
    ap.add_argument("--lang", default="both", choices=["ta", "en", "both"])
    ap.add_argument("--song-folder"); ap.add_argument("--src", default="staged", choices=["staged", "out"])
    ap.add_argument("--out-dir"); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    plan, folder = load(a.song_dir, a.song_folder)
    if a.action == "stage":
        stage(a.song_dir, plan, folder, a.force)
    else:
        for lang in (["ta", "en"] if a.lang == "both" else [a.lang]):
            cut(a.song_dir, plan, folder, lang, a.src, a.out_dir)

if __name__ == "__main__":
    main()
