#!/usr/bin/env python3
"""Build every VACE reference sheet the two song folders point at.

Two steps per sheet:
  1. cut the character out of its source image (rembg / u2net) onto transparency,
     because a reference carries its own background into the shot -- playbook
     section 5, the same way the OpenArt frame carried the Mazhai living room
     into V1a. Modhu arrives in a jungle, Singa on a savanna and Thangam in a
     pastel dawn sky; none of those belong in these songs.
  2. comfy/make_ref_sheet.py flattens the alpha onto white, trims, scales the
     tiles to a common height and centres them on a 1280x720 canvas (playbook
     section 3: native ComfyUI takes ONE reference and centre-crops it).

    python scripts/build_song_refs.py            # build everything
    python scripts/build_song_refs.py --song twinkle-twinkle
    python scripts/build_song_refs.py --no-cut   # reuse existing cutouts

Needs: pillow, rembg (pip install rembg onnxruntime).
"""
import argparse
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIBLE = r"C:\Channel Contents\MinMiniKids\charecter bible"
DAD = r"C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Dad"
MINTU = r"C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Mintu_Latest"
ROWSRC = r"C:\Channel Contents\MinMiniKids\songs\6 row row row your boat"
TWSRC = r"C:\Channel Contents\MinMiniKids\songs\Twinkle Twinkle"
CUTS = os.path.join(REPO, "outputs", "cutouts")

# ---- sources -------------------------------------------------------------
# cut=True  -> run background removal first (busy or tinted background)
# cut=False -> already on clean white/near-white; make_ref_sheet trims it
SRC = {
    # Mintu -- Arul's call 2026-09-22: use the Mintu_Latest four-view turnaround (2816x1536 Gemini renders on a
    # light-grey studio background -> cut). Views identified by eye: front is a T-POSE with an open-mouth smile,
    # so every Mintu shot keeps the T-pose NOT-lines / negative (playbook section 2) and "open mouth" stays negative.
    "mintu_front":  (os.path.join(MINTU, "Gemini_Generated_Image_c82nyxc82nyxc82n.jpeg"), True),   # front, T-pose
    "mintu_left":   (os.path.join(MINTU, "Gemini_Generated_Image_7euvr7euvr7euvr7.jpeg"), True),   # profile facing left
    "mintu_right":  (os.path.join(MINTU, "Gemini_Generated_Image_hbj14khbj14khbj1.jpeg"), True),   # profile facing right
    "mintu_back":   (os.path.join(MINTU, "Gemini_Generated_Image_t0cqrot0cqrot0cq.jpeg"), True),   # back, T-pose
    # (the older bible set generation-refs-2026-08-31/Mintu-gemini2 is superseded; its skin read yellow-plastic in S03)
    "minnu_face":   (os.path.join(BIBLE, "generation-refs-2026-08-31", "Minnu", "face-front.png"), False),
    "minnu_face34": (os.path.join(BIBLE, "generation-refs-2026-08-31", "Minnu", "face-threequarter.png"), False),
    "minnu_body":   (os.path.join(BIBLE, "generation-refs-2026-08-31", "Minnu", "body-relaxed-front.png"), False),
    "minnu_body34": (os.path.join(BIBLE, "generation-refs-2026-08-31", "Minnu", "body-relaxed.png"), False),
    # Appa -- the new four-view turnaround
    "appa_front":   (os.path.join(DAD, "front.png"), True),
    "appa_left":    (os.path.join(DAD, "left.png"), True),
    "appa_right":   (os.path.join(DAD, "right.png"), True),
    "appa_back":    (os.path.join(DAD, "back.png"), True),
    # animals
    "modhu":  (os.path.join(ROWSRC, "Gemini_Generated_Image_eoqn5zeoqn5zeoqn.jpeg"), True),   # jungle bg
    "singa":  (os.path.join(ROWSRC, "Gemini_Generated_Image_x4gmz8x4gmz8x4gm.jpeg"), True),   # savanna bg
    "karadi": (os.path.join(ROWSRC, "Gemini_Generated_Image_h9glkh9glkh9glkh.jpeg"), True),   # grey bg
    "chiku":  (os.path.join(ROWSRC, "Gemini_Generated_Image_54et8p54et8p54et.jpeg"), True),   # T-POSE, white bg
    # Twinkle cast
    "thangam":      (os.path.join(TWSRC, "Gemini_Generated_Image_h5wolrh5wolrh5wo.jpeg"), True),  # dawn sky bg
    "minmini_front":(os.path.join(TWSRC, "Gemini_Generated_Image_njp6oxnjp6oxnjp6.jpeg"), True),
    "minmini_sideA":(os.path.join(TWSRC, "Gemini_Generated_Image_35g14b35g14b35g1.jpeg"), True),
    "minmini_sideB":(os.path.join(TWSRC, "Gemini_Generated_Image_48lj8j48lj8j48lj.jpeg"), True),
    "minmini_back": (os.path.join(TWSRC, "Gemini_Generated_Image_nmaq3bnmaq3bnmaq.jpeg"), True),
    "minmini_wink": (os.path.join(TWSRC, "Gemini_Generated_Image_ctoke5ctoke5ctok.jpeg"), True),
}

# ---- sheets: song -> out name -> tiles, left to right ---------------------
SHEETS = {
    "twinkle-twinkle": {
        "mintu-4view-16x9.png":      ["mintu_front", "mintu_left", "mintu_right", "mintu_back"],
        "minnu-4view-16x9.png":      ["minnu_face", "minnu_face34", "minnu_body", "minnu_body34"],
        "kids-16x9.png":             ["mintu_front", "minnu_body"],
        "thangam-16x9.png":          ["thangam"],
        "minmini-4view-16x9.png":    ["minmini_front", "minmini_sideA", "minmini_sideB", "minmini_back"],
        # neutral + wink in ONE sheet: identity and target expression together,
        # the playbook section 2 pose-reference fix that got V1a right first try
        "minmini-wink-16x9.png":     ["minmini_front", "minmini_wink"],
        # 4g: the two-tile wink sheet produced a ghost second TV at one seed -- single-tile variant for the A/B
        "minmini-front-16x9.png":    ["minmini_front"],
        "minmini-thangam-16x9.png":  ["minmini_front", "thangam"],
        "kids-thangam-16x9.png":     ["mintu_front", "minnu_body", "thangam"],
        "kids-minmini-16x9.png":     ["mintu_front", "minnu_body", "minmini_front"],
        "mintu-thangam-16x9.png":    ["mintu_front", "thangam"],
        # 2026-09-23 (_ab4): SEPARATE one-tile sheets, one per child, for the multi-reference rows
        # (ref column "minnu-body-16x9.png|mintu-front-16x9.png"); core WanVaceToVideo takes only one image,
        # comfy/custom_nodes/wan_vace_multiref.py and Phantom take the batch
        "mintu-front-16x9.png":      ["mintu_front"],
        "minnu-body-16x9.png":       ["minnu_body"],
        "minmini-sideA-16x9.png":    ["minmini_sideA"],   # _ab5: second Phantom ref for side-on mascot shots
    },
    "row-row-row-your-boat": {
        "appa-mintu-minnu-16x9.png": ["appa_front", "mintu_front", "minnu_body"],
        # A/B 2026-09-22: the two children side by side merged into one child in S03;
        # Appa between them keeps the two child tiles apart on the sheet
        "minnu-appa-mintu-16x9.png": ["minnu_body", "appa_front", "mintu_front"],
        "kids-modhu-16x9.png":       ["mintu_front", "minnu_body", "modhu"],
        "kids-singa-16x9.png":       ["mintu_front", "minnu_body", "singa"],
        "kids-karadi-16x9.png":      ["mintu_front", "minnu_body", "karadi"],
        "kids-chiku-16x9.png":       ["mintu_front", "minnu_body", "chiku"],
        "animals-3up-16x9.png":      ["modhu", "singa", "karadi"],
    },
}


def cut(key, path, do_cut):
    """Background-removed PNG for `key`, or the original when no cut is needed."""
    if not do_cut:
        return path
    os.makedirs(CUTS, exist_ok=True)
    out = os.path.join(CUTS, key + ".png")
    if os.path.exists(out):
        return out
    from rembg import remove          # imported late so --no-cut needs no rembg
    from PIL import Image
    with Image.open(path) as im:
        remove(im.convert("RGBA")).save(out)
    print("  cut", key, "->", out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--song", default=None, help="only this song slug")
    ap.add_argument("--no-cut", action="store_true", help="reuse existing cutouts, never run rembg")
    a = ap.parse_args()

    missing = [k for k, (p, _) in SRC.items() if not os.path.exists(p)]
    if missing:
        sys.exit("source image(s) not found:\n  " + "\n  ".join("%s -> %s" % (k, SRC[k][0]) for k in missing))

    made = 0
    for song, sheets in SHEETS.items():
        if a.song and song != a.song:
            continue
        outdir = os.path.join(REPO, "songs", song, "refs")
        os.makedirs(outdir, exist_ok=True)
        print("\n==", song)
        for name, keys in sheets.items():
            tiles = []
            for k in keys:
                src, do = SRC[k]
                tiles.append(src if (a.no_cut and not os.path.exists(os.path.join(CUTS, k + ".png"))) else cut(k, src, do))
            out = os.path.join(outdir, name)
            subprocess.run([sys.executable, os.path.join(REPO, "comfy", "make_ref_sheet.py"),
                            "--out", out] + tiles, check=True)
            made += 1
    print("\n%d sheets built." % made)
    print("LOOK AT THEM before spending GPU time: three tiles in 1280x720 is tight, and if a")
    print("face is too small to read the shot will drift. Crop to head-and-shoulders and rebuild")
    print("that sheet if so.")


if __name__ == "__main__":
    main()
