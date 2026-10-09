# item-01 — cutplan, stage, TA + EN rough cuts, commit ($0.00)

1. Run the plan script, then check the plan file:
   ```
   py "C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\_gen\make_cutplan.py" songs\l05-urulai-w3
   ```
   - Expect: `wrote songs\l05-urulai-w3\cutplan.json: 33 slots, 17 clips, TA 148.261 s, EN 148.400 s — all slots fit their clips,
     no gaps`.
   - Anything else (above all `CUTPLAN CHECK FAILED`) → **blocked**.
   - Check that `cutplan.json`'s `song_folder` is the song folder path above.
2. `py comfy\song_cuts.py songs\l05-urulai-w3 stage`. Expect 17 files `NN_ID_slug.mp4` copied into the song folder. Report the list.
3. `py comfy\song_cuts.py songs\l05-urulai-w3 cut --lang both`.
   - Expect `_cuts\L05-URULAIKIZHANGU-ROUGH-TA.mp4` (4448 video frames) and `...-ROUGH-EN.mp4` (4452), with "video frames = plan"
     for each.
   - Report the cutlog lines that say "holds last frame" (Fable expects none).
   - Any error → **blocked**, with the error verbatim.
4. For each cut, write a contact sheet into the song folder's `_cuts\`: one frame every 2.2 s, 240 wide, timestamp burned in, 10
   columns. Name them `L05-ROUGH-TA-sheet.jpg` and `L05-ROUGH-EN-sheet.jpg`.
5. Commit with `[skip ci]` and push:
   - `songs/l05-urulai-w3/cutplan.json`;
   - `queue/2026-10-09-urulai-cuts`;
   - `queue/2026-10-09-urulai-gate4/FABLE-VERDICT.md` (if untracked);
   - `queue/L05-WATCH-LOG.md`.

   **Do not judge the cuts.**

**item-01.report.md** must cover:
- step outputs verbatim;
- the staged files;
- the cut paths with frame counts and sizes;
- any held-frame lines;
- the sheet paths;
- the commit hash.
