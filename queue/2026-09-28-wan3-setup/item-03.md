# item-03 — 4K upscale, side-by-side comparisons, copies, report, commit ($0)

1. Dispatch 6e Part D exactly: upscale the three Twinkle clips (and L01_w3 if it exists) — Wan 3.0 is 30 fps, so
   **no `-Fps`**; `-Height 2160` for 16:9, `-Height 3840` for L01. Sidecars should show `ncnn scale x3`.
2. The three comparison PNGs (time-based `-ss 2.5`, Wan 3.0 left, Phantom right) and, for L01, the `-stream_loop 2`
   loop preview + first/last frame PNG (read the frame count with ffprobe for the last index).
3. Copy the 4K files and PNGs to `C:\Channel Contents\MinMiniKids\songs\Twinkle Twinkle\wan3-test\` and L01's to
   `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\wan3\`.
4. Write `CC-REPORT-phase6e.md` in the repo root (dispatch 6e Part E list), then commit
   `songs/_ab7-2026-09-28-wan3/shots.csv`, `songs/shorts-loops/shots.csv` and the report with `[skip ci]`, push.

**item-03.report.md:** upscale sidecar values and seconds per clip; full Windows paths of all 4K files, comparison PNGs,
loop preview and copies; commit hash. **Do not judge the clips** — Fable frame-checks.
