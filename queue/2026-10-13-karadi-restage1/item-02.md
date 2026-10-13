# item-02 — ROUGH2 cuts with the new clips, sheets, commit ($0.00)

1. **Fallback for a failed clip.** If any of the four has no new `out\<ID>-seed30313-w3.mp4` after item-01 (e.g. refused by the
   service), **copy** (not move) its `out\<ID>-seed30313-w3-v1-picnic.mp4` to `out\<ID>-seed30313-w3.mp4`, so the cut can go
   ahead with the old picture. List which ones in the report. This does not overwrite anything.
2. **Retire the old staged copies.** In the song folder, **move** the four staged files `09_V1A_*.mp4`, `11_V2A_*.mp4`,
   `13_V3A_*.mp4` and `15_V4A_*.mp4` into `_superseded-2026-10-13\`. Report their names.
3. `py comfy\song_cuts.py songs\a12-karadi-w3 stage`. Expect `staged` for the four clips and `keep` for the other 14.
4. `py comfy\song_cuts.py songs\a12-karadi-w3 cut --lang both --tag ROUGH2`.
   - Expect `_cuts\A12-KARADI-MAMA-ROUGH2-TA.mp4` (4644 video frames) and `...-ROUGH2-EN.mp4` (3840), with "video frames = plan".
   - Report any "holds last frame" line.
   - The first ROUGH cuts stay as they are.
   - Any error → **blocked**, with the error verbatim.
5. Write contact sheets `A12-ROUGH2-TA-sheet.jpg` and `A12-ROUGH2-EN-sheet.jpg` into `_cuts\`, in the same format as the ROUGH sheets.
6. Commit with `[skip ci]` and push:
   - `songs/a12-karadi-w3/` except `out/`;
   - `queue/2026-10-13-karadi-restage1`;
   - `queue/A12-WATCH.md`;
   - `queue/A12-WATCH-LOG.md`.

   **Do not judge the clips or the cuts.**

**item-02.report.md** must cover:
- any fallbacks used;
- the moved files;
- the stage output;
- the cut paths, frame counts and sizes;
- the sheet paths;
- the commit hash.
