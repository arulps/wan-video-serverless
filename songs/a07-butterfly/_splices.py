"""A07 Butterfly — splices Arul asked for on 2 Oct (instead of retakes). Writes out\\<ID>-seed30313-w3-splice.mp4
from the batch takes (never touches the originals). Frame numbers are the take's own (30 fps, 0-based).

    python songs/a07-butterfly/_splices.py [ID ...]      (default: all)

Each piece: (start_frame, end_frame_inclusive, slow, zoom, (cx, cy))
  slow  = playback stretch (1.0 = real time; 1.3 = 30 % slower, motion-interpolated)
  zoom  = centre punch-in (1.0 = full frame), around (cx, cy) in 1280x720 pixels
Pieces are joined with hard cuts. The result must cover the clip's longest slot (checked against cutplan.json)."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
W, H, FPS = 1280, 720, 30

SPLICES = {
    # V2b: two yellow butterflies until ~f69; one from f72. Opening girls-only frames (f0-29) punched in 1.35x so the two
    # tiny side butterflies are cropped out, then the single-butterfly part f72-149, both gently slowed.
    "V2b": [(0, 26, 1.40, 1.7, (640, 300)), (72, 149, 1.30, 1.0, (640, 360))],   # 1.7x medium shot: side butterflies out of frame
    # V2c: f30-110 = butterfly to the jasmine, girls peek up, close-up (before the jump to the open lawn at ~f114);
    # then a tight punch-in on the butterfly on the jasmine (f84-112) to make up the line.
    "V2c": [(30, 110, 1.15, 1.0, (640, 360)), (84, 112, 1.50, 1.6, (640, 430))],
    # V3a: cut before the fade (butterfly starts to go transparent at f137); tiny stretch to cover the 4.59 s English line.
    "V3a": [(0, 136, 1.015, 1.0, (640, 360))],
    # V6b: four butterflies on the sunflower f0-74, kids join from ~f36; they fade out from ~f78. Open on a slow close-up of
    # the four smiling butterflies (f0-37, before the kids), then the wide f0-74.
    "V6b": [(0, 37, 1.40, 1.35, (640, 330)), (0, 74, 1.15, 1.0, (640, 360))],
    # V1c: Mintu (alone with the rose) f0-30; he dissolves f33-36 ("two Mintus"); keep f39 on (rose, Leo walks in, Mintu
    # walks in, both boys to the end).
    "V1c": [(0, 30, 1.0, 1.0, (640, 360)), (39, 149, 1.0, 1.0, (640, 360))],
    # --- Arul's review of ROUGH-TA, 6 Oct ---
    # V1b (0:35): two red butterflies come in from both sides and merge into one (f4-52). Keep the single-butterfly part f56-149,
    # then a 1.45x close-up on the butterfly between the boys' faces (f70-115).
    "V1b": [(56, 149, 1.0, 1.0, (640, 360)), (70, 115, 1.0, 1.45, (640, 360))],
    # V4b (2:05): two green butterflies merge (f4-48). Keep the single-butterfly part f52-149, slowed 1.42x.
    "V4b": [(52, 149, 1.42, 1.0, (640, 360))],
    # V4a (~2:00): the big leaf floats in mid-air (f0-11, f36-79). Keep the butterfly close-up f16-35 at a 1.4x punch-in (crops the
    # leaf tip under it), then the four kids with the butterfly f72-149 at 1.12x (crops the leaf edge on the right); both slowed.
    "V4a": [(16, 35, 1.4, 1.4, (640, 330)), (72, 149, 1.42, 1.12, (560, 380))],
    # O3: after the Tamil anchor fix (6 Oct) the Tamil outro's last line is 6.7 s; the 5 s take slowed 1.36x (sleepy ending, fades out).
    "O3": [(0, 149, 1.36, 1.0, (640, 360))],   # 1.12x left-shifted crop drops the leaf edge at f72-79
}


def piece_filter(i, a, b, slow, zoom, c):
    f = f"[0:v]trim=start_frame={a}:end_frame={b + 1},setpts=PTS-STARTPTS"
    if zoom != 1.0:
        cw, ch = int(round(W / zoom / 2) * 2), int(round(H / zoom / 2) * 2)
        x = min(max(int(c[0] - cw / 2), 0), W - cw)
        y = min(max(int(c[1] - ch / 2), 0), H - ch)
        f += f",crop={cw}:{ch}:{x}:{y},scale={W}:{H}:flags=lanczos"
    if slow != 1.0:
        f += f",setpts={slow}*PTS,minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1"
    f += f",fps={FPS},settb=1/{FPS},setpts=N,format=yuv420p[p{i}]"
    return f


def need_frames(cid):
    plan = json.load(open(os.path.join(HERE, "cutplan.json"), encoding="utf-8"))
    n = 0
    for s in plan["shots"]:
        if s["id"] != cid:
            continue
        for l in ("ta", "en"):
            if s[l + "_in"] is not None:
                n = max(n, round((s[l + "_out"] - s[l + "_in"]) * FPS + s.get("slip", {}).get(l, 0) * FPS))
    return n


def count(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_frames", "-of", "csv=p=0", p], capture_output=True, text=True)
    return int(r.stdout.strip())


for cid in (sys.argv[1:] or SPLICES):
    pieces = SPLICES[cid]
    src = os.path.join(OUT, f"{cid}-seed30313-w3.mp4")
    dst = os.path.join(OUT, f"{cid}-seed30313-w3-splice.mp4")
    chains = [piece_filter(i, *p) for i, p in enumerate(pieces)]
    chains.append("".join(f"[p{i}]" for i in range(len(pieces))) + f"concat=n={len(pieces)}:v=1:a=0[v]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", ";".join(chains), "-map", "[v]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-r", str(FPS), dst],
                   check=True)
    got, need = count(dst), need_frames(cid)
    print(f"{cid}: {got} frames ({got / FPS:.2f} s), longest slot needs {need} -> {'OK' if got >= need else 'SHORT'}")
