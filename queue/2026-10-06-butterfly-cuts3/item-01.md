# item-01 — re-stage O3, build ROUGH3 cuts, commit ($0)

1. `python tests\test_song_cuts_reuse.py --plan-only` → PASS; `python comfy\prompt_lint.py --song songs\a07-butterfly` → LINT PASS.
   Every `take` in `cutplan.json` exists in `songs\a07-butterfly\out\` (33 distinct, 10 splices incl. O3). Else → **blocked**.
2. Copy `songs\a07-butterfly\out\O3-seed30313-w3-splice.mp4` over
   `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\32_O3_they-land-and-fall-asleep.mp4` (md5 must match; other 32 unchanged).
3. Build both cuts:
   ```
   python comfy\song_cuts.py songs\a07-butterfly cut --lang both --src out --tag ROUGH3 --song-folder "C:\Channel Contents\MinMiniKids\songs\A07-Butterfly" 2>&1 | tee songs\a07-butterfly\cuts_rough3.log
   ```
   Expected `…\_cuts\A07-BUTTERFLY-ROUGH3-TA.mp4` = 6481 frames, `-ROUGH3-EN.mp4` = 6665 frames; no hold lines over 1 frame.
   In the TA cutlog, `CH1=RA` must start at `in 9.150` and `O3` at `in 209.340`.
4. ffprobe both: 1920×1080, 30 fps, one AAC stream.
5. Commit `[skip ci]` and push: `songs/a07-butterfly/_splices.py`, `cutplan.json`, `shots.csv`, `shots/`, `cuts_rough3.log`,
   `queue/2026-10-06-butterfly-cuts3`.
**item-01.report.md:** checks; O3 copy md5; both `wrote …` lines; the CH1 and O3 TA in-points; ffprobe; hold lines; commit hash.
