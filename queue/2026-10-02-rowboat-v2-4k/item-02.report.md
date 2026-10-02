# item-02 report — 4K smoke test on ONE clip, overnight command ($0)

## 1. Tool check
`C:\tools\realesrgan-ncnn-vulkan\realesrgan-ncnn-vulkan.exe` is present (6,161,408 B, phase 6b install), with
`models\realesr-animevideov3-x2/x3/x4 .bin/.param`. Nothing was downloaded.

## 2. Free disk on C:
- Before the smoke test: **13.6 GB free** (of 952.3 GB). After it: 15.5 GB free.
- **⚠ The full run needs ~15 GB temporary + ~2 GB output ≈ 17 GB, more than is free now.** Free up a few GB (e.g. old
  `outputs\`, the defective/partial files, or temp folders) before starting the overnight run, or it may fail partway.
  `song_4k.ps1` / `upscale_song.py` are resumable, so a disk-full stop can be continued after freeing space.

## 3. Smoke test — T1 (90 frames)
`python scripts\upscale_song.py songs\rowboat --only T1` → exit 0, **10:07:45 → 10:20:21 UTC** (06:07 → 06:20 Toronto).
The log is `C:\Projects\opencode\video_image\songs\rowboat\upscale_4k_smoke.log`.

- Output: `C:\Projects\opencode\video_image\songs\rowboat\out_4k\T1-seed30313-w3.mp4` (11,896,330 B) + `T1-seed30313-w3.mp4.json`.
- Sidecar: **`backend: ncnn`**, `device: vulkan`, model `animevideov3`, `upscale_factor: 3`, interpolation none, h264 crf 16.
  - Output **3840×2160 @ 30 fps, 90 frames, 3.00 s**, video only (ffprobe `-count_frames`: 90).
  - `seconds`: decode **7.3**, upscale **636.0**, encode **96.8**.
- **s/frame (upscale ÷ 90): 7.07 s/frame.** The wall time including decode + encode was 8.40 s/frame (as the tool reported).
- **GPU line:** `[0 Intel(R) Iris(R) Xe Graphics]  queueC=0[1]  queueG=0[1]  queueT=0[1]`. The tool's own log does not echo
  realesrgan's banner, so this line comes from running the same exe on one T1 frame right after the test (temp files deleted).

## 4. Overnight run (NOT started)
- ETA for the remaining 28 clips (3770 frames):
  - upscale only: 3770 × 7.07 s ≈ **26,600 s ≈ 7.4 h**;
  - with decode + encode, at the measured 8.40 s/frame: ≈ **31,700 s ≈ 8.8 h**;
  - plus building the two 4K cuts afterwards (the 1080p V2 build took ~18 min; 4K will take longer).
- Command for Arul (from the repo root `C:\Projects\opencode\video_image`):

```
powershell -ExecutionPolicy Bypass -File scripts\song_4k.ps1 -Song songs\rowboat -Tag V2-4K
```

It skips T1 (already in `out_4k\`), upscales the other 28 takes, then builds `...-V2-4K-TA.mp4` and `...-V2-4K-EN.mp4` in
`C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\`. **Free disk space first (see 2).**

## Commit
The `[skip ci]` commit containing this file (queue record only; `out_4k\` is not committed). item-01's commit was `a79dad7`.
