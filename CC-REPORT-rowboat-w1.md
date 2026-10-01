# CC-REPORT — Rowboat W1: L04 Row Row Row Your Boat, world 1 (river morning + Modhu), on Wan 3.0 (2026-10-01)

Queue `queue\2026-10-01-rowboat-w1`. **Result: 10/10 rendered, 0 failed. 45 s total. Estimate $4.50 at list price** (~$3.15 with
the 30% discount; hard cap $5.00). 1280×720 16:9, 30 fps, audio off, seed 30313. No pod, no upscale. Nothing was written to
`C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\`.

## item-01 — checks and render
- `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- Credentials: `credentials present: True`.
- **Dry-run** (`--only I1,I2,V1b,V1c,V2a,V2b,V2c,V2d,X1a,X1b`): 10 rows, all `720P 16:9 audio=off`, **`estimated $4.50`**,
  0 MISSING/ERROR/OVER BUDGET hits.
- **Seating check:**
  - "on the low wooden bench at the other end of the boat" is present in `04_V1b.raw.txt`.
  - "face to face" appears in **no** `shots\*.raw.txt`.
- **Protected files:** the md5 of `V1a-seed30313-w3.mp4` and every `*-v1-*` file (14 files, including the `_qc` PNGs) was recorded
  before the run. The check after the run, and again after item-02, matched: **all 14 unchanged**. V1a was not re-rendered.
  None of the 10 output names existed beforehand.
- **Render window:** **17:57:50 → 18:08:41 UTC, 2026-10-01** (13:57:50 → 14:08:41 Toronto EDT). 3 tasks in parallel,
  `--max-usd 5.00 --timeout-min 40`, and the runner exited 0.

| shot | status | task id | wall s | length | frames | refs | est (list) | streams | verbatim prompt |
|---|---|---|---|---|---|---|---|---|---|
| I1 | done | `d5e86f59-d723-4ed3-b9a8-ad62a15d42e4` | 131.3 | 8 s | 240 | 0 | $0.80 | video | yes |
| I2 | done | `adc657df-3bb6-47e8-9fbb-e1c9328cd154` | 194.6 | 6 s | 180 | 6 | $0.60 | video | yes |
| V1b | done | `8c946de9-4034-403b-a8d8-b84387c85069` | 147.0 | 3 s | 90 | 4 | $0.30 | video | yes |
| V1c | done | `add135e2-f928-4510-843c-5e303e863ce3` | 162.5 | 3 s | 90 | 6 | $0.30 | video | yes |
| V2a | done | `7cfcd830-44cb-4853-9006-0054bf4e7ffe` | 147.6 | 3 s | 90 | 2 | $0.30 | video | yes |
| V2b | done | `90f16e98-dc06-4a29-8005-34f317d09334` | 163.4 | 3 s | 90 | 4 | $0.30 | video | yes |
| V2c | done | `ec3207f3-5af2-4877-b24d-ad3a3f032f08` | 156.9 | 3 s | 90 | 1 | $0.30 | video | yes |
| V2d | done | `61ef984a-4780-43e3-bec4-d18534447b7c` | 194.5 | 4 s | 120 | 4 | $0.40 | video | yes |
| X1a | done | `679acac1-d78b-4c7b-a8ca-06c5419fdf24` | 195.8 | 6 s | 180 | 7 | $0.60 | video | yes |
| X1b | done | `960137fc-c8ef-41a5-9b06-ad1db60fe00b` | 195.5 | 6 s | 180 | 6 | $0.60 | video | yes |

- The task ids come from each clip's sidecar, which is the authoritative row ↔ task mapping.
- "Verbatim prompt" means the sidecar prompt equals the shot's `*.raw.txt` (stripped).
- **Failures:** none. No URL or key appears in any sidecar or in the log. All 10 `shots.csv` status cells are `done`.

## item-02 — sheets and stills
- **Contact sheets:** 5×2, 10 frames evenly spaced from the first frame to the last (frame `round(i·(N−1)/9)`, i = 0…9), each 384 wide → 1920×432.
- **100% stills** at 10 %, 50 % and 95 % of the frame count N, 1280×720:

| shot | N | stills |
|---|---|---|
| I1 | 240 | f024, f120, f228 |
| I2, X1a, X1b | 180 | f018, f090, f171 |
| V2d | 120 | f012, f060, f114 |
| V1b, V1c, V2a, V2b, V2c | 90 | f009, f045, f086 |

- Nothing was copied to the song folder.

## Paths
Clips and sidecars (`C:\Projects\opencode\video_image\songs\rowboat\out\`):
- `C:\Projects\opencode\video_image\songs\rowboat\out\I1-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\I2-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V1b-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V1c-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V2a-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V2b-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V2c-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V2d-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\X1a-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\X1b-seed30313-w3.mp4` (+ `.json`)

QC (`C:\Projects\opencode\video_image\songs\rowboat\out\_qc\`), per shot: `<ID>-strip.png`, `<ID>-contact.png` and the three stills above, e.g.
- `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\I1-contact.png`, `...\_qc\I1-f024.png`, `...\_qc\I1-f120.png`, `...\_qc\I1-f228.png`
- `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\X1a-contact.png`, `...\_qc\X1a-f018.png`, `...\_qc\X1a-f090.png`, `...\_qc\X1a-f171.png`
- and likewise for I2, V1b, V1c, V2a, V2b, V2c, V2d and X1b.

Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_w1.log`

## Commit
The `[skip ci]` commit containing this report. It holds `songs/rowboat/_make_rowboat.py` (the gate-2 V1a seating override),
the regenerated `shots/` (23 changed `*.raw.txt`), `shots.csv` (10 new `done` cells), `cutplan.json` (unchanged, so a no-op),
the queue folder and this report. `out/` is not included. The hash is in CC's chat reply. Not committed: Fable's uncommitted edit
to `REVIEW-learning-batch1-2026-09-29.md`.

## Not judged
Fable reviews.
