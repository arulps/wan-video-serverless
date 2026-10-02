# item-02 — 4K smoke test on ONE clip, then report the overnight command ($0)

1. Tool check: `C:\tools\realesrgan-ncnn-vulkan\realesrgan-ncnn-vulkan.exe` exists (from phase 6b). If not → **blocked**
   (do not download anything; report).
2. Free disk on C: — report GB free (the full run needs ~15 GB temporary + ~2 GB output).
3. Smoke test, one 3 s clip (~90 frames, expect ~5–8 min):
   `python scripts\upscale_song.py songs\rowboat --only T1 2>&1 | tee songs\rowboat\upscale_4k_smoke.log`
   → `songs\rowboat\out_4k\T1-seed30313-w3.mp4` + `.json`. Report from the sidecar: `backend` (must be `ncnn`),
   output 3840x2160 @ 30 fps, seconds per stage, **s/frame** (upscale seconds ÷ 90), and the GPU line the tool printed.
4. Do **not** start the full run. Report the ETA for the remaining 28 clips (3770 frames × s/frame) and this command for Arul:
   `powershell -ExecutionPolicy Bypass -File scripts\song_4k.ps1 -Song songs\rowboat -Tag V2-4K`
   (it skips T1, upscales the rest, then builds `...-V2-4K-TA.mp4` and `...-V2-4K-EN.mp4` in the song's `_cuts\`).
