# item-01 — stage clips, build both rough cuts, commit ($0)

1. `python tests\test_song_cuts_reuse.py --plan-only` → PASS. Else → **blocked**.
2. Every `take` named in `songs\a07-butterfly\cutplan.json` exists in `songs\a07-butterfly\out\` (33 distinct files). Else → **blocked**.
3. Stage the numbered clips into the song folder (copies only, one file per clip even when a clip fills several slots):
   `python comfy\song_cuts.py songs\a07-butterfly stage --song-folder "C:\Channel Contents\MinMiniKids\songs\A07-Butterfly"`
   → 33 files `01_I1_….mp4` … `33_O4_….mp4`.
4. Build both cuts, hard cuts everywhere:
   ```
   python comfy\song_cuts.py songs\a07-butterfly cut --lang both --src out --tag ROUGH --song-folder "C:\Channel Contents\MinMiniKids\songs\A07-Butterfly" 2>&1 | tee songs\a07-butterfly\cuts_rough1.log
   ```
   Expected: `…\_cuts\A07-BUTTERFLY-ROUGH-TA.mp4` (6481 frames ≈ 216.04 s) and `…-ROUGH-EN.mp4` (6665 frames ≈ 222.16 s); the tool
   itself fails if the frame count is off. Note any "holds last frame" lines in the report (there should be none over 1 frame).
5. ffprobe both: 1920×1080, 30 fps, one AAC stream; durations as above.
6. Commit with `[skip ci]` and push: `songs/a07-butterfly/_splices.py`, `songs/a07-butterfly/cutplan.json`,
   `songs/a07-butterfly/cuts_rough1.log`, `queue/2026-10-02-butterfly-cuts`.
**item-01.report.md:** plan test; the 33 staged names; both `wrote …` lines; ffprobe table; any hold lines verbatim; commit hash.
