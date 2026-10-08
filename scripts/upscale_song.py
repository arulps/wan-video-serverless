#!/usr/bin/env python3
"""Upscale every chosen take of a song (cutplan.json "take") to 4K, resumable, for a 4K master cut.

    python scripts/upscale_song.py songs/rowboat              # all takes -> songs/rowboat/out_4k/<take>
    python scripts/upscale_song.py songs/rowboat --only V2d,T1
    python scripts/upscale_song.py songs/rowboat --dry        # list what would run + frame count, no work

Each take goes through scripts/upscale_video.py (Real-ESRGAN realesr-animevideov3 via realesrgan-ncnn-vulkan, x4 then
lanczos to 3840x2160, same 30 fps, h264 crf 16). A take counts as done only when its out_4k .mp4 AND .mp4.json sidecar
exist (the sidecar is written last), so an interrupted run resumes at the clip it was on; a half-written mp4 is redone.
Forces --backend ncnn: on a laptop without CUDA the torch-CPU fallback is ~29 s/frame (a song would take >30 h), so if
the Vulkan tool is missing it stops instead. The first of <repo>\\tools\\realesrgan-ncnn-vulkan (git-ignored, installed
per machine) or C:\\tools\\realesrgan-ncnn-vulkan (old location) that exists is put on PATH.
Then: python comfy/song_cuts.py songs/<slug> cut --src out4k --height 2160 --tag V2-4K --lang both
"""
import argparse, json, os, shutil, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent

def frames(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("song_dir"); ap.add_argument("--only", default="")
    ap.add_argument("--height", type=int, default=2160); ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    song = Path(a.song_dir)
    plan = json.load(open(song / "cutplan.json", encoding="utf-8"))
    only = {x.strip() for x in a.only.split(",") if x.strip()}
    takes, seen = [], set()
    for s in plan["shots"]:
        if (only and s["id"] not in only) or s["take"] in seen:
            continue
        seen.add(s["take"]); takes.append((s["id"], s["take"]))
    tool_dirs = (HERE.parent / "tools" / "realesrgan-ncnn-vulkan", Path(r"C:\tools\realesrgan-ncnn-vulkan"))
    for d in tool_dirs:
        if d.is_dir():
            os.environ["PATH"] = str(d) + os.pathsep + os.environ["PATH"]
            break
    if not a.dry and not shutil.which("realesrgan-ncnn-vulkan"):
        sys.exit("realesrgan-ncnn-vulkan not found (expected in %s or %s) -- stopping" % tool_dirs)
    dst_dir = song / "out_4k"; dst_dir.mkdir(exist_ok=True)
    todo = []
    for sid, take in takes:
        src, dst = song / "out" / take, dst_dir / take
        if not src.exists():
            sys.exit("missing source take for %s: %s" % (sid, src))
        if dst.exists() and Path(str(dst) + ".json").exists():
            print("skip (done)", sid, take); continue
        todo.append((sid, src, dst, frames(src)))
    total = sum(t[3] for t in todo)
    print("to do: %d clips, %d frames" % (len(todo), total))
    if a.dry:
        for sid, src, dst, n in todo: print("  ", sid, src.name, n, "frames")
        return
    t0, done = time.time(), 0
    for i, (sid, src, dst, n) in enumerate(todo, 1):
        for stale in (dst, Path(str(dst) + ".json")):
            if stale.exists(): stale.unlink()
        print("[%d/%d] %s %s (%d frames)" % (i, len(todo), sid, src.name, n), flush=True)
        r = subprocess.run([sys.executable, str(HERE / "upscale_video.py"), str(src), str(dst), "--height", str(a.height),
                            "--backend", "ncnn"])
        if r.returncode != 0 or not Path(str(dst) + ".json").exists():
            sys.exit("upscale failed for %s (exit %s) -- rerun the same command to resume" % (sid, r.returncode))
        done += n
        el = time.time() - t0
        print("   done %s; %d/%d frames, %.2f s/frame, ETA %.0f min" % (sid, done, total, el / done,
              (total - done) * el / done / 60), flush=True)
    print("ALL DONE: %d clips in %s" % (len(todo), dst_dir))

if __name__ == "__main__":
    main()
