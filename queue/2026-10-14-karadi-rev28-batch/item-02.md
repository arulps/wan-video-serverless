# item-02 — ROUGH3: full TA + EN rough cuts of the family trek, sheets, commit ($0)

Run even if a batch row failed in item-01 — then the cut stops on the missing clip; report that line and skip to step 4.
1. `py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\make_cutplan.py" songs\a12-karadi-w3` → `… TA 29 slots 154.800 s,
   EN 24 slots 128.000 s, 21 clips — all slots fit their clips, no gaps`. Report the `take` of the CAa entries: it must be `CAa-seed30313-w3-splice.mp4`.
2. Cut both languages straight from `out\` (no staging):
   ```
   py comfy\song_cuts.py songs\a12-karadi-w3 cut --lang both --src out --tag ROUGH3
   ```
   Expect `_cuts\A12-KARADI-MAMA-ROUGH3-TA.mp4` (4644 video frames) and `…-ROUGH3-EN.mp4` (3840), each "video frames = plan". Report any
   cutlog line with "holds last frame". Never overwrite an existing file (the ROUGH/ROUGH2 cuts have different names).
3. Sheets into `_cuts\`: `A12-ROUGH3-TA-sheet.jpg`, `A12-ROUGH3-EN-sheet.jpg` (one frame every 2.2 s, 240 wide, timestamp burned in,
   10 columns — same tool as the ROUGH2 sheets) and **per-slot sheets** `A12-ROUGH3-TA-slots.jpg` / `-EN-slots.jpg`: one row per slot
   (29 / 24 rows), 3 frames per row = the first, middle and last played frame of the slot, 240 wide, the slot number and clip ID burned in at the left.
4. Commit with `[skip ci]` and push: `songs/a12-karadi-w3/` except `out/` (shots.csv, shots/, cutplan.json, logs), `queue/2026-10-14-karadi-rev27b-gateB2`
   (with its FABLE-VERDICT.md), `queue/2026-10-14-karadi-rev28-batch`, `queue/A12-WATCH-LOG.md`. **Do not judge the cut.**

**item-02.report.md:** step outputs verbatim (cutlogs' held-frame lines only), the four sheet paths with sizes, the two cut paths with
frame counts and sizes, the commit hash.
