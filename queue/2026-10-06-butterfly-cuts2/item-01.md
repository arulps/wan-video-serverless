# item-01 — re-stage 3 clips, build ROUGH2 cuts, commit ($0)

1. `python tests\test_song_cuts_reuse.py --plan-only` → PASS. Every `take` in `songs\a07-butterfly\cutplan.json` exists in
   `songs\a07-butterfly\out\` (33 distinct; V1b, V4a, V4b now `-splice`). Else → **blocked**.
2. Replace exactly three staged clips in `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\` by copying the splices over them
   (do NOT run `stage --force`, which would rewrite all 33):
   - `out\V1b-seed30313-w3-splice.mp4` → `08_V1b_pretty-little-butterfly.mp4`
   - `out\V4a-seed30313-w3-splice.mp4` → `20_V4a_hello-green-butterfly.mp4`
   - `out\V4b-seed30313-w3-splice.mp4` → `21_V4b_leafy-green-butterfly.mp4`
   md5 of each staged file must equal its splice afterwards; the other 30 staged clips md5 unchanged.
3. Build both cuts:
   ```
   python comfy\song_cuts.py songs\a07-butterfly cut --lang both --src out --tag ROUGH2 --song-folder "C:\Channel Contents\MinMiniKids\songs\A07-Butterfly" 2>&1 | tee songs\a07-butterfly\cuts_rough2.log
   ```
   Expected `…\_cuts\A07-BUTTERFLY-ROUGH2-TA.mp4` = 6481 frames (216.04 s) and `-ROUGH2-EN.mp4` = 6665 frames (222.16 s); no
   "holds last frame" lines over 1 frame.
4. ffprobe both: 1920×1080, 30 fps, one AAC stream.
5. Commit with `[skip ci]` and push: `songs/a07-butterfly/_splices.py`, `songs/a07-butterfly/cutplan.json`,
   `songs/a07-butterfly/cuts_rough2.log`, `queue/2026-10-06-butterfly-cuts2`.
**item-01.report.md:** plan test; the 3 copies with md5; both `wrote …` lines; ffprobe table; hold lines; commit hash.
