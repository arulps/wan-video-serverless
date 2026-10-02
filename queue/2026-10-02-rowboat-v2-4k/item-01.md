# item-01 — V2 cuts (1080p, hard cuts), commit ($0) — **REDO 2026-10-02 (Fable fixed song_cuts.py)**

**Why the REDO:** run 1 (see `item-01.report-1-blocked.md`) produced a 13.4 s video track: hard cuts were 1-frame xfades whose
offset ran past the accumulated stream. Fable rewrote `cut()` to be **frame-exact**: every shot starts at
round((in − t0) × 30); hard cuts are a plain `concat`, dissolves an `xfade` only where real frames exist; every stream is
normalised to timebase 1/30. It now **fails loudly** if the encoded video frame count differs from the plan. Fable tested with
the new `--preview` mode (480×270 full-length encode): TA 3713 frames = plan 3713, EN 2908 = plan 2908, 0 frozen frames, cuts
on the planned frames. The two defective V2 files in `_cuts\` from run 1 are simply overwritten by this run.


1. `python comfy\song_cuts.py songs\rowboat cut --lang both --src out --tag V2 2>&1 | tee songs\rowboat\cuts_v2.log`
   → writes `...\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-V2-TA.mp4` and `...-V2-EN.mp4` + their cutlogs. Error → **blocked**.
2. The tool must print `wrote ... 3713 video frames = plan 3713` (TA) and `2908 video frames = plan 2908` (EN); a
   `VIDEO FRAME CHECK FAILED` line → **blocked**. Then ffprobe both: **video stream** frames/duration (TA 3713 / ≈123.77 s,
   EN 2908 / ≈96.93 s), 1920x1080, 30 fps, one AAC stream. `grep -c "holds last frame"` on both V2
   cutlogs must be **0**. Confirm the `*-ROUGH-*` files are unchanged (md5 before/after).
3. Remove the empty folder `songs\rowboat\out_4k_test` (left by a Fable test). Keep `songs\rowboat\out_4k\` (empty, used next).
4. Commit with `[skip ci]` and push: `comfy/song_cuts.py`, `comfy/prompt_lint.py`, `scripts/upscale_song.py`,
   `scripts/song_4k.ps1`, `queue/2026-10-02-rowboat-v2-4k`.
**item-01.report.md:** both outputs (duration/size/streams), the hold-count check, md5 check, commit hash.
