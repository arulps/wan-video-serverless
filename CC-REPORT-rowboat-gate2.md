# CC-REPORT — Rowboat gate 2: L04 Row Row Row Your Boat, new seating, V1a retake + V1b, on Wan 3.0 (2026-10-01)

Queue `queue\2026-10-01-rowboat-gate2`. **Result: 2/2 rendered. Estimate $0.90 at list price** (~$0.63 with the 30% discount;
cap $1.00). 1280×720 16:9, audio off, seed 30313. No pod, no upscale. Nothing was written to
`C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\`.

## item-01 — checks and render
- `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- Credentials: `credentials present: True`.
- **Dry-run** (`--only V1a,V1b`): 2 rows, both `720P 16:9 audio=off`. V1a is 6 s with refs=6 ($0.60); V1b is 3 s with refs=4 ($0.30).
  **`estimated $0.90`**, 0 MISSING/ERROR hits.
- **Seating check:** "two low wooden benches face each other" is present in both `03_V1a.raw.txt` and `04_V1b.raw.txt`.
  "side by side" appears in **no** `shots\*.raw.txt`.
- **Render window:** **15:09:27 → 15:12:43 UTC, 2026-10-01** (11:09:27 → 11:12:43 Toronto EDT). 2 tasks in parallel.

| shot | status | task id | wall s | length | frames | refs | est (list) |
|---|---|---|---|---|---|---|---|
| V1a | done | `5d302529-dcc3-4667-b5fd-39c4d19ed2de` | 195.2 | 6 s | 180 | 6 (Appa, Mintu, Minnu face+body) | $0.60 |
| V1b | done | `468a6fb5-4b3f-4698-9d17-8ff9923e22f5` | 147.9 | 3 s | 90 | 4 (Mintu, Minnu face+body) | $0.30 |

- **Verbatim:** each sidecar prompt equals its `*.raw.txt` (stripped), including the benches phrase.
- Both are 1280×720 @ 30 fps, video only, `params.audio` = False.
- **Failures:** none. No URL or key appears in the sidecars or the log. The V1a/V1b status cells are `done`.
- **Old V1a kept:** `V1a-seed30313-w3-v1-rimseat.mp4` (+ `.json`) and its 6 `_qc\V1a-v1-rimseat-*.png` files are present and
  untouched. The new V1a is a different file (md5 differs).

## item-02 — sheets and stills
- V1a: contact sheet 5×2, every 18th frame (0–162), 384 wide → 1920×432. 100% stills of frames 30, 90 and 170 (1280×720).
- V1b: contact sheet 5×2, every 9th frame (0–81), 384 wide → 1920×432. 100% stills of frames 15, 45 and 80 (1280×720).
- Nothing was copied to the song folder.

## Paths
- `C:\Projects\opencode\video_image\songs\rowboat\out\V1a-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V1b-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\V1a-strip.png`, `V1a-contact.png`, `V1a-f030.png`, `V1a-f090.png`, `V1a-f170.png`
- `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\V1b-strip.png`, `V1b-contact.png`, `V1b-f015.png`, `V1b-f045.png`, `V1b-f080.png`
- Old take for comparison: `C:\Projects\opencode\video_image\songs\rowboat\out\V1a-seed30313-w3-v1-rimseat.mp4`, `...\out\_qc\V1a-v1-rimseat-contact.png`
- Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_gate2.log`

## Commit
The `[skip ci]` commit containing this report. It holds `songs/rowboat/_make_rowboat.py` (the SEAT_ALL / SEAT_SHOT override), the
regenerated `shots/` (23 changed `*.raw.txt`), `shots.csv`, `cutplan.json` (unchanged, so a no-op), the queue folder and this
report. `out/` is not included. The hash is in CC's chat reply. Not committed: Fable's uncommitted edit to
`REVIEW-learning-batch1-2026-09-29.md`.

## Not judged
Fable reviews the new seating (kids on facing benches in the back half, Appa rowing in front) before the other 27 shots.
