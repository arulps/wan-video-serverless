"""Stand-in test for comfy/song_cuts.py with re-used clips and per-language order (A07 Butterfly rev 3). $0, local ffmpeg.

    python tests/test_song_cuts_reuse.py [--song-folder "C:\\Channel Contents\\MinMiniKids\\songs\\A07-Butterfly"]

1. Rowboat regression: for both languages, sorting the cut plan by in-point gives exactly the old list order (the sort
   added for Butterfly changes nothing for existing songs).
2. Butterfly: every slot's slip + slot length fits inside its clip's generate length; the same clip never plays twice
   in a row; Tamil 47 / English 48 slots; the English break sits before Hook 3.
3. Butterfly: make one stand-in clip per take (testsrc2, 160x90, the clip's generate length) in a temp folder, then build
   both cuts with --preview (480x270) into that temp folder. song_cuts.py itself fails if the video frame count is off.
Nothing is written to the repo or the song folder (the master WAVs are only read)."""
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("--song-folder", default=r"C:\Channel Contents\MinMiniKids\songs\A07-Butterfly")
ap.add_argument("--plan-only", action="store_true", help="checks 1-2 only, no encode")
a = ap.parse_args()

# 0 ffmpeg option by version: ffmpeg 9 (Beast) rejects -filter_complex_script; >= 7 must use -/filter_complex
sys.path.insert(0, str(ROOT / "comfy"))
import song_cuts as sc
for text, want in (("ffmpeg version 9.0.2-full_build-www.gyan.dev Copyright", "-/filter_complex"),
                   ("ffmpeg version 7.0.2-static https://johnvansickle.com/ffmpeg/", "-/filter_complex"),
                   ("ffmpeg version n7.1 Copyright", "-/filter_complex"),
                   ("ffmpeg version N-117000-g1234abcd Copyright", "-/filter_complex"),
                   ("ffmpeg version 2026-09-01-git-abcdef-full_build-www.gyan.dev", "-/filter_complex"),
                   ("ffmpeg version 6.1.1-3ubuntu5 Copyright", "-filter_complex_script"),
                   ("ffmpeg version 4.4.2-0ubuntu0.22.04.1", "-filter_complex_script")):
    got = sc.filter_graph_args("g.txt", text)
    assert got == [want, "g.txt"], (text, got)

# 1 rowboat regression
rp = json.load(open(ROOT / "songs/rowboat/cutplan.json", encoding="utf-8"))
for lang in ("ta", "en"):
    old = [s["id"] for s in rp["shots"] if s[lang + "_in"] is not None]
    new = [s["id"] for s in sorted((s for s in rp["shots"] if s[lang + "_in"] is not None), key=lambda s: s[lang + "_in"])]
    assert old == new, ("rowboat order changed", lang)

# 2 butterfly plan checks
bp = json.load(open(ROOT / "songs/a07-butterfly/cutplan.json", encoding="utf-8"))
assert bp["xfade"] == 0
for lang, n in (("ta", 47), ("en", 48)):
    sh = sorted((s for s in bp["shots"] if s[lang + "_in"] is not None), key=lambda s: s[lang + "_in"])
    assert len(sh) == n, (lang, len(sh))
    for p, q in zip(sh, sh[1:]):
        assert p["take"] != q["take"], ("same clip twice in a row", lang, p["slot"], q["slot"])
        assert abs(p[lang + "_out"] - q[lang + "_in"]) < 0.002, (lang, p["slot"], q["slot"])
    for s in sh:
        use = s[lang + "_out"] - s[lang + "_in"]
        assert s.get("slip", {}).get(lang, 0) + use <= s["gen"] + 1e-6, (lang, s["slot"])
    order = [s["slot"] for s in sh]
    if lang == "en":
        assert order.index("BRKb") + 1 == order.index("H3a"), "English break must sit before Hook 3"
    else:
        assert order.index("H3b") + 1 == order.index("BRKa"), "Tamil break must follow Hook 3"

if a.plan_only:
    print("PASS (plan only): ffmpeg filter option by version; rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit"); sys.exit(0)

# 3 stand-in encode
folder = Path(a.song_folder)
for lang in ("ta", "en"):
    assert (folder / bp["audio"][lang]).exists(), "master WAV not found: %s" % bp["audio"][lang]
with tempfile.TemporaryDirectory() as td:
    td = Path(td); (td / "out").mkdir()
    (td / "cutplan.json").write_text(json.dumps(bp), encoding="utf-8")
    for take, gen in sorted({(s["take"], s["gen"]) for s in bp["shots"]}):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                        "testsrc2=size=160x90:rate=30:duration=%d" % gen, "-c:v", "libx264", "-preset", "ultrafast",
                        str(td / "out" / take)], check=True)
    r = subprocess.run([sys.executable, str(ROOT / "comfy/song_cuts.py"), str(td), "cut", "--lang", "both", "--src", "out",
                        "--preview", "--song-folder", str(folder), "--out-dir", str(td / "cuts")],
                       capture_output=True, text=True)
    print("\n".join(l for l in r.stdout.splitlines() if "wrote " in l or "plan:" in l)); print(r.stderr[-1500:])
    assert r.returncode == 0, "song_cuts failed"
    assert r.stdout.count("video frames = plan") == 2, "frame check line missing"
    assert "holds last frame" not in r.stdout, "a clip is too short for its slot"
print("PASS: ffmpeg filter option by version; rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit, both stand-in cuts frame-exact")
