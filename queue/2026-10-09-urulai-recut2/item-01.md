# item-01 — cutplan rev 2 and the ROUGH2 1080p cuts ($0.00, no renames)

1. Run:
   ```
   py "C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\_gen\make_cutplan.py" songs\l05-urulai-w3
   ```
   - Expect: "33 slots, 17 clips … all slots fit their clips, no gaps".
   - Check that the I1 slot in `cutplan.json` has `"take": "I1-seed30313-w3-splice.mp4"`.
   - Anything else → **blocked**.
2. `py comfy\song_cuts.py songs\l05-urulai-w3 cut --lang both --src out --tag ROUGH2`
   - Expect new files `_cuts\L05-URULAIKIZHANGU-ROUGH2-TA.mp4` (4448 video frames) and `...-ROUGH2-EN.mp4` (4452), each reporting
     "= plan".
   - No "holds last frame" lines.
   - Any error → **blocked**, verbatim.
3. Make new contact sheets: every 2.2 s, 240 wide, timestamp burned in, 10 columns. Name them `L05-ROUGH2-TA-sheet.jpg` and
   `L05-ROUGH2-EN-sheet.jpg`.

**item-01.report.md** must cover:
- step outputs verbatim;
- the frame counts and sizes of both cuts;
- the sheet paths.
