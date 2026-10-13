# item-01 — cutplan, stage, TA + EN rough cuts, sheets, commit ($0.00)

1. Run the plan script, then check the plan file:
   ```
   py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\make_cutplan.py" songs\a12-karadi-w3
   ```
   - Expect: `wrote songs\a12-karadi-w3\cutplan.json: TA 29 slots 154.800 s, EN 24 slots 128.000 s, 18 clips — all slots fit their
     clips, no gaps`.
   - Anything else (above all `CUTPLAN CHECK FAILED`) → **blocked**.
   - Check that `cutplan.json`'s `song_folder` is `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama`.
2. `py comfy\song_cuts.py songs\a12-karadi-w3 stage`. Expect 18 files `NN_ID_slug.mp4` copied into the song folder. Report the list.
3. `py comfy\song_cuts.py songs\a12-karadi-w3 cut --lang both`.
   - Expect `_cuts\A12-KARADI-MAMA-ROUGH-TA.mp4` (4644 video frames) and `...-ROUGH-EN.mp4` (3840), with "video frames = plan"
     for each.
   - Report any cutlog line that says "holds last frame" (Fable expects none).
   - Any error → **blocked**, with the error verbatim.
4. For each cut, write a contact sheet into the song folder's `_cuts\`: one frame every 2.2 s, 240 wide, timestamp burned in, 10
   columns. Name them `A12-ROUGH-TA-sheet.jpg` and `A12-ROUGH-EN-sheet.jpg`.
5. Commit with `[skip ci]` and push:
   - `songs/a12-karadi-w3/cutplan.json`;
   - `queue/2026-10-13-karadi-batch1/FABLE-VERDICT.md`;
   - `queue/2026-10-13-karadi-cuts`;
   - `queue/A12-WATCH-LOG.md`.

   **Do not judge the cuts.**

**item-01.report.md** must cover:
- step outputs verbatim;
- the staged files;
- the cut paths with frame counts and sizes;
- any held-frame lines;
- the sheet paths;
- the commit hash.
