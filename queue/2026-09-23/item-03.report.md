# item-03 report — upscale utility: 16→30 fps interpolation path (laptop only, $0)

## Result: DONE

## Step 1 — `py` on PATH
`py scripts/upscale_video.py --help` worked directly (no need to fall back to `python3`).

## Step 2 — RIFE availability
`which rife-ncnn-vulkan` → **not on PATH**. The script fell back to its documented alternative:
`ffmpeg minterpolate` for the frame-rate interpolation.

## Step 3 — the run
```
py scripts/upscale_video.py songs/twinkle-twinkle/out/T16-seed30313-s6.mp4 outputs/upscale-test-2026-09-23/T16-4k-30.mp4 --fps 30
```
No GPU on this laptop for the Real-ESRGAN pass, so it ran on **CPU** — much slower than the item's "a few minutes"
estimate (that estimate assumed a GPU): **~28 min wall time** total (17:54:12 → 18:22:19 UTC).
- decode: 2.6 s (81 source frames)
- upscale (Real-ESRGAN animevideov3, CPU): 753.4 s (~9.3 s/frame × 81 frames)
- encode (incl. `ffmpeg minterpolate` to 30 fps + h264 crf 16): 915.4 s

Output: `C:\Projects\opencode\video_image\outputs\upscale-test-2026-09-23\T16-4k-30.mp4`
Sidecar: `C:\Projects\opencode\video_image\outputs\upscale-test-2026-09-23\T16-4k-30.mp4.json`

### Sidecar values
- `interpolation`: **`"ffmpeg minterpolate -> 30 fps"`** — confirms the untested path (our own 16 fps Wan clips,
  unlike phase 5a's 30 fps OpenArt source where `"interpolation": "none"`) actually exercised interpolation this
  time.
- `seconds`: `{"decode": 2.6, "upscale": 753.4, "encode": 915.4}`
- Output dims came out **3744×2160**, not the item's expected 3840×2160 — the source is 832×480 (aspect
  1.7333...), and the script scales to the target height while preserving that source aspect ratio, so
  2160 × (832/480) = 3744, not a fixed 3840. Not a bug, just aspect-ratio arithmetic; noting the discrepancy
  from the item's own estimate rather than silently matching it.
- Frame count: source 81 @ 16 fps (5.0625 s) → output 149 @ 30 fps (4.966667 s), consistent with a fps-only
  retime (149 ≈ 81 × 30/16 = 151.875, close enough given minterpolate's own frame-blend timing — not exact
  duplication).

### `ffprobe` of the output
```
codec_name=h264
width=3744
height=2160
r_frame_rate=30/1
nb_frames=149
```
Matches the sidecar exactly.

## Step 4 — QC pair (motion check, for Fable)
- `C:\Projects\opencode\video_image\outputs\upscale-test-2026-09-23\_qc\T16-4k-30-frames60-67.png`
  (8-frame strip, frames 60–67 of the 30 fps output, scaled to 960 wide each)
- `C:\Projects\opencode\video_image\outputs\upscale-test-2026-09-23\_qc\T16-src-frames32-35.png`
  (4-frame strip, frames 32–35 of the 16 fps source, scaled to 960 wide each)

Both ffmpeg calls printed a harmless "does not contain an image sequence pattern" warning (expected with
`-frames:v 1` + a literal filename) but wrote the single PNG correctly both times — file sizes/timestamps
confirm both exist.

## Warnings
One Python `UserWarning` during the upscale pass (`torch.from_numpy` on a non-writable NumPy array,
`upscale_video.py:117`) — cosmetic, from PyTorch's own tensor-conversion codepath, not a correctness issue;
appears once then is suppressed by Python for the rest of the run per the warning text itself.

## Cost: **$0** (laptop only, no GPU pod). Running total this queue unchanged: **≈ $4.27 of $6**.

`item-03.done` created. Waiting for verdict.
