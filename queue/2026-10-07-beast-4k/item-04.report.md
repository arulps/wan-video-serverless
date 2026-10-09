# item-04 — full 4K run + 4K cuts — FINISHED and verified (see the end)

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

## Verification (item-05 step 2) — DONE 2026-10-08, all checks pass

**What happened to the run.** The upscale finished on its own at 23:59 on 7 Oct (32 clips, 5,067 frames, 0.52 s/frame,
`ALL DONE: 32 clips`). The first cut attempt right after it **failed**: Beast's ffmpeg 9.0.2 rejects
`-filter_complex_script`. Fable fixed `comfy/song_cuts.py` (uses `-/filter_complex` on ffmpeg 7+) and added version
checks to `tests/test_song_cuts_reuse.py`; Arul ran the test (PASS) and re-ran `song_4k.ps1` on 8 Oct ~00:44. That
second run skipped all 33 clips (`to do: 0 clips`) and built both cuts (TA written 00:47, EN 00:50). The failed
attempt left no error text in `upscale_4k.log` — the log only shows the upscale, then the re-run.

**Upscaled takes — `songs\a07-butterfly\out_4k\`**
- 33 `.mp4` + 33 `.json` sidecars; the 33 names match the 33 takes in `cutplan.json` exactly (none missing, none extra;
  10 are `-splice.mp4`).
- All 33 are 3840×2160, 30/1 fps (ffprobe `r_frame_rate` and `avg_frame_rate`). Frame counts total 5,217.

**4K cuts — song folder `_cuts\`** (ffprobe `-count_frames`)

| File | Video frames | Video | Audio | Size |
|---|---|---|---|---|
| `A07-BUTTERFLY-ROUGH3-4K-TA.mp4` | **6481** (target 6481) | h264 3840×2160, 30 fps, 216.033 s | 1 × AAC, 216.040 s | 994 MB |
| `A07-BUTTERFLY-ROUGH3-4K-EN.mp4` | **6665** (target 6665) | h264 3840×2160, 30 fps, 222.167 s | 1 × AAC, 222.160 s | 1,017 MB |

- Each file has exactly two streams (one video, one AAC).
- Cut logs: no "holds last frame" lines at all, in either `.cutlog.txt` or in `upscale_4k.log`.
- Both 4K cut logs are line-for-line the same as the ROUGH3 cut logs (same slots, same in-points, same frame counts),
  so the 4K cuts have the same cut points as ROUGH3.
- ROUGH, ROUGH2 and ROUGH3 cuts were not touched (dates unchanged: 2 Oct, 6 Oct, 6 Oct).

**Test.** `py tests\test_song_cuts_reuse.py` on Beast (ffmpeg 9.0.2), run again in this session:
`PASS: ffmpeg filter option by version; rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit, both stand-in cuts frame-exact`

**Stills for Fable — `songs\a07-butterfly\out_4k\_qc\`** (PNG, 3840×2160, one frame each, not committed)
- `ROUGH3-4K-TA-0030.png`, `ROUGH3-4K-TA-0200.png`
- `ROUGH3-4K-EN-0030.png`, `ROUGH3-4K-EN-0200.png`

**Not checked here:** picture quality. The stills were made and are the right size, but nobody has looked at them yet —
that is Fable's review.

**Note for later:** `.gitignore` has `out/` and `*.mp4` but no `out_4k/` line, so the `.json` sidecars in `out_4k\`
show up as untracked. They were not staged. A one-line `out_4k/` in `.gitignore` would stop that.
