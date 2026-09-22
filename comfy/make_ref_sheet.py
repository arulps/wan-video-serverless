#!/usr/bin/env python3
"""Build a VACE reference sheet: flatten alpha to white, auto-trim each
image's white/near-white margins, scale all tiles to a common height so the
row fits inside the canvas, and centre the row on a white canvas (default
1280x720 -- native ComfyUI centre-crops one reference image to the output
aspect, so sheets must already be that shape).

    python comfy/make_ref_sheet.py --out refs/minnu-4view-16x9.png \
        a.png b.png c.png d.png [--size 1280x720] [--gap 24] [--margin 24]

Reproduces the logic described in docs/PROMPT-PLAYBOOK.md section 3 (the
one-off script that made outputs/vace/refs/minnu-4view-16x9.png): trim to
content bbox with a 30px margin, common height = canvas_H - 2*margin, shrink
the row if it would exceed canvas_W - 2*margin, 24px gap between tiles.

Needs Pillow (the one third-party import allowed for this tool). Everything
else in comfy/ is stdlib-only.
"""
import argparse
import os
import sys

from PIL import Image

TRIM_THRESHOLD = 12  # 0-255; pixels this close to white count as background
TRIM_CONTENT_MARGIN = 30  # px of white kept around the trimmed content bbox


def flatten_to_white(im):
    """Composite any alpha channel onto a white background; return RGB."""
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def trim_white_margins(im, threshold=TRIM_THRESHOLD, margin=TRIM_CONTENT_MARGIN):
    """Trim near-white borders down to the content bounding box, then pad
    `margin` px of white back around it."""
    gray = im.convert("L")
    # Non-background = anything darker than (255 - threshold): pixels within
    # `threshold` of pure white count as background.
    bg_level = 255 - threshold
    mask = gray.point(lambda p: 255 if p < bg_level else 0)
    bbox = mask.getbbox()
    if bbox is None:
        return im  # blank image; nothing to trim
    left, top, right, bottom = bbox
    left = max(0, left - margin)
    top = max(0, top - margin)
    right = min(im.width, right + margin)
    bottom = min(im.height, bottom + margin)
    return im.crop((left, top, right, bottom))


def build_sheet(paths, out_path, canvas_w, canvas_h, gap, margin, trim):
    tiles = []
    for p in paths:
        im = Image.open(p)
        im = flatten_to_white(im)
        if trim:
            im = trim_white_margins(im, margin=TRIM_CONTENT_MARGIN)
        tiles.append(im)

    if not tiles:
        sys.exit("no input images given")

    # Common height: the canvas height minus the outer margin on top+bottom.
    common_h = canvas_h - 2 * margin
    if common_h <= 0:
        sys.exit("--margin too large for --size")

    scaled = []
    for im in tiles:
        w, h = im.size
        new_w = max(1, round(w * (common_h / h)))
        scaled.append(im.resize((new_w, common_h), Image.LANCZOS))

    row_w = sum(im.width for im in scaled) + gap * (len(scaled) - 1)
    max_row_w = canvas_w - 2 * margin
    if row_w > max_row_w:
        # Shrink every tile uniformly so the row (including gaps) fits.
        scale = (max_row_w - gap * (len(scaled) - 1)) / sum(im.width for im in scaled)
        if scale <= 0:
            sys.exit("too many images / too small a canvas for --gap and --margin")
        new_h = max(1, round(common_h * scale))
        scaled = [im.resize((max(1, round(im.width * scale)), new_h), Image.LANCZOS) for im in scaled]
        row_w = sum(im.width for im in scaled) + gap * (len(scaled) - 1)

    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    row_h = max(im.height for im in scaled)
    x = (canvas_w - row_w) // 2
    y = (canvas_h - row_h) // 2
    for im in scaled:
        tile_y = y + (row_h - im.height) // 2
        canvas.paste(im, (x, tile_y))
        x += im.width + gap

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    canvas.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+", help="input image paths, left to right")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1280x720")
    ap.add_argument("--gap", type=int, default=24)
    ap.add_argument("--margin", type=int, default=24, help="outer white margin on the canvas")
    ap.add_argument("--no-trim", action="store_true", help="skip auto-trimming white margins")
    a = ap.parse_args()

    try:
        w, h = (int(x) for x in a.size.lower().split("x"))
    except Exception:
        sys.exit("--size must look like 1280x720")

    out = build_sheet(a.images, a.out, w, h, a.gap, a.margin, trim=not a.no_trim)
    print("wrote", out)


if __name__ == "__main__":
    main()
