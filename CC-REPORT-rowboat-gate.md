# CC-REPORT — Rowboat gate: L04 Row Row Row Your Boat, shot V1a only (look-lock), on Wan 3.0 (2026-10-01)

Queue `queue\2026-10-01-rowboat-gate`. **Result: V1a rendered. Estimate $0.60 at list price** (~$0.42 with the 30% discount;
cap $0.70). 1280×720 16:9, 6 s, audio off, seed 30313. No pod, no upscale. Nothing was written to
`C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\`.

## item-01 — checks and render
- `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
  `py_compile` of `batch_runner.py` and `song_cuts.py` OK.
- Credentials: `credentials present: True`.
- **Dry-run, all 29 rows:** 29 rows, all `720P 16:9 audio=off`, **`estimated $12.90`**, 0 MISSING/ERROR/OVER BUDGET hits.
  - Lengths: 13× 3 s, 4× 4 s, 11× 6 s, 1× 8 s.
  - Refs per row: between 0 and 7.
- **V1a dry-run:** `wan3.0-video 720P 16:9 6s audio=off, est $0.60`, refs=6, labelled Appa, Appa, Mintu, Mintu, Minnu, Minnu
  (`01-appa-face`, `02-appa-body`, `03-mintu-front`, `04-mintu-side`, `05-minnu-face`, `06-minnu-body`).
- **Render window:** **14:34:44 → 14:37:14 UTC, 2026-10-01** (10:34:44 → 10:37:14 Toronto EDT).

| row | status | task id | wall s | length | est (list) |
|---|---|---|---|---|---|
| V1a | done | `46c02932-f924-430b-80fb-1c164849d89f` | 148.9 | 6 s | $0.60 |

- `usage`: duration 6.0, output_video_duration 6.0, fps 30, video_count 1, SR 720, ratio 16:9. `params.audio` = False.
- Output: 1280×720 @ 30 fps, 180 frames, video stream only (audio off, as specified).
- **Verbatim prompt check:** the sidecar prompt equals `songs\rowboat\shots\03_V1a.raw.txt` exactly, except the file's trailing
  newline (2480 vs 2481 chars). The new `*.raw.txt` path sends the prompt as-is.
- **Failures:** none. No URL or key appears in the sidecar or the log. The `shots.csv` status for V1a is `done`; the other 28 are blank.

## item-02 — sheet and stills
- Contact sheet: 5×2 tiles, every 18th frame (0, 18 … 162), 384 wide → 1920×432.
- Full-size stills: frames 30, 90 and 170, at 1280×720.
- Nothing was copied to the song folder (per the item).

## Paths
- `C:\Projects\opencode\video_image\songs\rowboat\out\V1a-seed30313-w3.mp4`
- `C:\Projects\opencode\video_image\songs\rowboat\out\V1a-seed30313-w3.json`
- `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\V1a-strip.png`
- `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\V1a-contact.png`
- `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\V1a-f030.png`
- `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\V1a-f090.png`
- `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\V1a-f170.png`
- Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_gate.log`

## Commit
The `[skip ci]` commit containing this report. It holds:
- `comfy/batch_runner.py` (verbatim `*.raw.txt` support) and `comfy/song_cuts.py`;
- `songs/rowboat/`: `_make_rowboat.py`, `shots/`, `shots.csv`, `cutplan.json`, `style.txt`, `world.txt`, `characters.txt`, and
  `refs/*.jpg` added with `-f`. `out/` and `batch_gate.log` are not included;
- the queue folder and this report.

The hash is in CC's chat reply. Not committed: Fable's uncommitted edit to `REVIEW-learning-batch1-2026-09-29.md`.

## Not judged
Fable reviews V1a's look-lock before the other 28 shots ($12.30 list) are rendered.
