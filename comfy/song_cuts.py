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
    missing, seen = [], set()
    for s in plan["shots"]:
        src = Path(song_dir) / "out" / s["take"]
        dst = folder / staged_name(s)
        if dst in seen:                       # a re-used clip (several slots, one take) is staged once
            continue
        seen.add(dst)
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
    if src_mode == "out4k":   # per-clip 4K upscales made by scripts/upscale_video.py (same file names)
        return Path(song_dir) / "out_4k" / s["take"]
    return folder / staged_name(s)

def video_frames(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)

def cut(song_dir, plan, folder, lang, src_mode, out_dir=None, transitions="auto", tag="ROUGH", height=1080, dry=False,
        preview=False):
    """Frame-exact assembly. Every shot starts at frame round((in - t0) * FPS) of the timeline. A shot is followed by
    either a hard cut (plain concat, frame-exact) or a dissolve of D frames, which needs D real frames of the outgoing
    clip after its slot; transitions="auto" dissolves only where those frames exist (no frozen last frame), "dissolve"
    always dissolves (v1 behaviour: may hold the last frame). Cuts into SFX shots are always hard. After encoding, the
    video frame count is checked against the plan (a short video track is an error, not a warning)."""
    W, H = (3840, 2160) if height >= 2160 else (1920, 1080)
    if preview:
        W, H = 480, 270
    # entries are slots; sort per language (the two languages may order sections differently, e.g. a moved break)
    shots = sorted((s for s in plan["shots"] if s[lang + "_in"] is not None), key=lambda s: s[lang + "_in"])
    D = int(round(float(plan.get("xfade", 0.4)) * FPS))
    t0 = shots[0][lang + "_in"]
    length = float(plan["length"][lang])
    total = int(round(length * FPS))
    wav = folder / plan["audio"][lang]
    if not wav.exists():
        sys.exit("audio not found: %s" % wav)
    T = [int(round((s[lang + "_in"] - t0) * FPS)) for s in shots] + [total]
    inputs, chains, log = [], [], []
    seg_len, d_out = [], []
    for k, s in enumerate(shots):
        p = clip_path(song_dir, folder, s, src_mode)
        if not p.exists():
            sys.exit("clip missing for %s: %s (run 'stage' first, or --src out)" % (s["id"], p))
        start = float(s.get("slip", {}).get(lang, 0.0))
        seg = T[k + 1] - T[k]
        nxt = shots[k + 1] if k + 1 < len(shots) else None
        avail = int((probe_len(p) - start) * FPS + 1e-6)          # whole real frames after the slip point
        if nxt is None or nxt["kind"] == "sfx":
            dk = 0
        elif transitions == "dissolve" or avail >= seg + D:
            dk = D
        else:
            dk = 0
        need = seg + dk
        hold = max(0, need - avail)
        seg_len.append(need); d_out.append(dk)
        inputs += ["-i", str(p)]
        chains.append("[%d:v]trim=start=%.4f,setpts=PTS-STARTPTS,fps=%d,"
                      "scale=%d:%d:force_original_aspect_ratio=decrease:flags=lanczos,"
                      "pad=%d:%d:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p,"
                      "tpad=stop_mode=clone:stop=%d,trim=end_frame=%d,settb=1/%d,setpts=N[c%d]"
                      % (k, start, FPS, W, H, W, H, hold + 2, need, FPS, k))
        log.append("%s %-4s in %8.3f use %6.3f slip %.3f frames %4d%s%s" % (
            s["n"], s["id"] if s.get("slot", s["id"]) == s["id"] else "%s=%s" % (s["slot"], s["id"]), s[lang + "_in"], seg / FPS, start, seg,
            "" if nxt is None else (" dissolve %d f" % dk if dk else " hard-cut"),
            " (holds last frame %d f)" % hold if hold > 1 else ""))   # 1 frame = in-point rounding, invisible
    cur, cur_len = "c0", seg_len[0]
    for k in range(1, len(shots)):
        dk = d_out[k - 1]
        if dk:
            assert cur_len - dk == T[k], (k, cur_len, dk, T[k])
            chains.append("[%s][c%d]xfade=transition=fade:duration=%.6f:offset=%.6f,settb=1/%d,setpts=N[x%d]"
                          % (cur, k, dk / FPS, (cur_len - dk) / FPS, FPS, k))
            cur_len += seg_len[k] - dk
        else:
            assert cur_len == T[k], (k, cur_len, T[k])
            chains.append("[%s][c%d]concat=n=2:v=1:a=0,settb=1/%d,setpts=N[x%d]" % (cur, k, FPS, k))
            cur_len += seg_len[k]
        cur = "x%d" % k
    assert cur_len == total, (cur_len, total)
    fin = plan["fades"][lang]
    chains.append("[%s]fade=t=in:st=0:d=%.3f,fade=t=out:st=%.3f:d=%.3f,trim=end_frame=%d,setpts=PTS-STARTPTS[v]"
                  % (cur, fin["in"], length - fin["out"], fin["out"], total))
    name = re.sub(r"[^A-Za-z0-9]+", "-", plan["song"]).strip("-").upper()
    out_dir = Path(out_dir) if out_dir else folder / "_cuts"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / ("%s-%s-%s%s.mp4" % (name, tag, lang.upper(), "-PREVIEW" if preview else ""))
    graph = out_dir / ("_graph-%s.txt" % lang)
    graph.write_text(";\n".join(chains), encoding="utf-8")
    enc = (["-c:v", "libx264", "-preset", "ultrafast", "-crf", "30"] if preview else
           ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p"]
           + (["-profile:v", "high", "-level", "5.1"] if H >= 2160 else []))
    cmd = (["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-i", str(wav), "-filter_complex_script", str(graph),
           "-map", "[v]", "-map", "%d:a" % len(shots), "-t", "%.3f" % length] + enc +
           ["-r", str(FPS), "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", str(out)])
    print("\n".join(log))
    print("plan: %d frames (%.3f s)" % (total, total / FPS))
    if not preview:
        (out_dir / ("%s-%s-%s.cutlog.txt" % (name, tag, lang.upper()))).write_text("\n".join(log) + "\n", encoding="utf-8")
    if dry:
        print("dry run: graph + cutlog written, no encode"); return out
    subprocess.run(cmd, check=True)
    got = video_frames(out)
    if abs(got - total) > 1:
        sys.exit("VIDEO FRAME CHECK FAILED: %s has %d video frames, plan %d" % (out, got, total))
    print("wrote", out, "%d video frames = plan %d; container %.3f s (audio %.3f s)" % (got, total, probe_len(out), length))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("song_dir"); ap.add_argument("action", choices=["stage", "cut"])
    ap.add_argument("--lang", default="both", choices=["ta", "en", "both"])
    ap.add_argument("--song-folder"); ap.add_argument("--src", default="staged", choices=["staged", "out", "out4k"])
    ap.add_argument("--transitions", default="auto", choices=["auto", "dissolve"])
    ap.add_argument("--tag", default="ROUGH", help="output name part: <SONG>-<TAG>-<LANG>.mp4 (e.g. V2, V2-4K)")
    ap.add_argument("--height", type=int, default=1080, choices=[1080, 2160])
    ap.add_argument("--dry", action="store_true", help="write graph + cutlog only, no encode")
    ap.add_argument("--preview", action="store_true", help="fast 480x270 test encode (checks the full frame count)")
    ap.add_argument("--out-dir"); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    plan, folder = load(a.song_dir, a.song_folder)
    if a.action == "stage":
        stage(a.song_dir, plan, folder, a.force)
    else:
        for lang in (["ta", "en"] if a.lang == "both" else [a.lang]):
            cut(a.song_dir, plan, folder, lang, a.src, a.out_dir, a.transitions, a.tag, a.height, a.dry, a.preview)

if __name__ == "__main__":
    main()
