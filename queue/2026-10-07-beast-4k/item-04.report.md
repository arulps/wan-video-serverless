# item-04 — full 4K run + 4K cuts — STARTED (running on its own)

- **Started:** 2026-10-07 23:15:08 on `arulps-beast`, in its own PowerShell window (PID 19568, `-NoExit`), with the
  command from the dispatch:
  `powershell -ExecutionPolicy Bypass -File scripts\song_4k.ps1 -Song songs\a07-butterfly -Tag ROUGH3-4K`
- **Confirmed running:** log shows `skip (done) V1a`, then `to do: 32 clips, 5067 frames`, `[1/32] I1 ... on vulkan`,
  `Real-ESRGAN x3 via realesrgan-ncnn-vulkan`.
- **Expected finish:** upscale ≈ 46 min (5,067 frames × 0.54 s/frame, item-03) → about **00:00–00:05**, then the two 4K
  cut encodes (not measured; allow up to ~15 min) → roughly **00:05–00:20 on 2026-10-08**.
- **Log:** `songs\a07-butterfly\upscale_4k.log` (the window prints `DONE: 4K cuts are in the song folder's _cuts\` at the end).
- **Outputs:** `songs\a07-butterfly\out_4k\` (33 takes + `.json` sidecars), then
  `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\_cuts\A07-BUTTERFLY-ROUGH3-4K-TA.mp4` and `-ROUGH3-4K-EN.mp4`.
- **If it stops** (window closed, error): run the same command again — finished clips are skipped.

## Verification (item-05 step 2) — NOT DONE YET
To be appended in a later session once Arul says the run finished.
