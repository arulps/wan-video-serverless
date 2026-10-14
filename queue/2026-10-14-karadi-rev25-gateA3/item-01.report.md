# item-01 report — DONE: HKa rendered ($0.80), QC sheets for HKa + O1, four slot cuts with the music, slot sheet

Run by CC (A12 watcher), 2026-10-14 08:52–08:58 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
One render, no retries. The clips were not judged.

## Step 1 — client update
- `comfy\wan3_api.py` contains `def _never_sent(` (1 match).
- `py -m py_compile comfy\wan3_api.py` → no output, exit 0.
- `py tests\test_wan3_retry_mock.py` → `PASS test_wan3_retry_mock: 10 checks`
- `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
- Credentials check → `credentials present: True`

## Step 2 — checks
- `shots.csv`: HKa `failed`, O1 `done`. OK (the item allows `failed` or `todo`).
- `out\O1-seed30313-w3.mp4` exists, `ffprobe -count_frames` → 210. OK.
- `out\` had no `HKa-seed30313-w3.mp4`. OK.
- `shots\05_HKa.raw.txt` contains "the children do their own quick full turn beside him". OK.
- `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`

## Step 3 — dry-run
Exactly 1 row: `wan3: wan3.0-video 720P 16:9 8s audio=off, est $0.80 (list price); refs=7 labels=['Mintu', 'Minnu', 'Karadi Mama',
'Amma', 'Appa', 'Appa', 'the lower forest path set']`. Refs: `01-mintu-front`, `02-minnu-front`, `03-karadi-mama`, `06-amma-front`,
`07-appa-face`, `08b-appa-body-backpack`, `11-set-path-low`. Total line: `engine=wan3 rows: estimated $0.80 at list price`.
No `ERROR` / `MISSING` / `OVER BUDGET` / `Traceback`.

## Step 4 — render: DONE
Command as given (`--only HKa --retry-failed --hosts api --max-usd 0.90 --timeout-min 40`), log `songs\a12-karadi-w3\batch_gateA3.log`
(checked: no URL in it or in the sidecar).

**Run window:** 2026-10-14 12:52:29 – 12:56:33 UTC = 08:52:29 – 08:56:33 Toronto (EDT).

| Clip | Status | Task id | Wall s | Length | Frames | Refs | Est |
|---|---|---|---|---|---|---|---|
| HKa | done | `2d01d015-511e-4eb3-9d68-fb9129c0e7bf` | 243.1 | 8.000 s, 1280×720, 30 fps | 240 | 7 | $0.80 |

No retry lines, no `NOT resubmitted` line. The log, verbatim:
```
[HKa] -> wan3 wan3.0-video 720P 16:9 8s refs=7 first=False last=False est $0.80
  wan3 submitted task 2d01d015-511e-4eb3-9d68-fb9129c0e7bf
  wan3 task 2d01d015-511e-4eb3-9d68-fb9129c0e7bf: RUNNING
  wan3 task 2d01d015-511e-4eb3-9d68-fb9129c0e7bf: SUCCEEDED
[HKa] done in 243.1s -> songs/a12-karadi-w3\out\HKa-seed30313-w3.mp4 (running list-price estimate $0.80)

SHOT       STATUS       WALL_S  FILE
HKa        done          243.1  songs/a12-karadi-w3\out\HKa-seed30313-w3.mp4

total GPU-minutes (done shots): 4.1
```
`out\HKa-seed30313-w3.mp4` 10,438,340 bytes; sidecar `out\HKa-seed30313-w3.json` 7,909 bytes; the runner's strip
`out\_qc\HKa-strip.png`. `shots.csv` HKa → `done` (the runner's own update). **Runner's final estimate: $0.80.**

## Step 5 — QC sheets (into `songs\a12-karadi-w3\out\_qc\`; ffmpeg with `-n`, nothing overwritten — none of these existed)
For each of HKa (240 frames) and O1 (210 frames):
- `<ID>-contact.png` — 5×2, 10 evenly spaced frames, each 384 wide (sheet 1920×432). The burned number is the tile index 0–9;
  the source frames are 0, 26, 53, 79, 106, 132, 159, 185, 212, 239 (HKa) and 0, 23, 46, 69, 92, 116, 139, 162, 185, 209 (O1).
- `<ID>-every4-all.png` — every 4th frame, source frame number burned in, 192 wide, 10 per row (HKa 1920×648, 60 tiles; O1 1920×648, 53 tiles).
- 100 % stills `<ID>-fNNN.png` (1280×720) for frames 000, 012, 024, 036, 048, 060, 072, 090, 120, 150, 180 and the last
  (`HKa-f239.png`, `O1-f209.png`).

## Step 6 — slot cuts with the music
Folder created: `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateA\`. Hard cut, 1920×1080, 30 fps, H.264 CRF 16
yuv420p, AAC 256k 48 kHz, command as in the item (with `-n` in place of `-y`; the folder was new).

| file | frames | duration | bytes |
|---|---|---|---|
| `_cuts\_gateA\HKa-TA-slot03.mp4` | 159 | 5.317 s | 6,224,820 |
| `_cuts\_gateA\HKa-EN-slot04.mp4` | 159 | 5.317 s | 6,228,735 |
| `_cuts\_gateA\O1-TA-slot27.mp4` | **158** | 5.294 s | 6,620,115 |
| `_cuts\_gateA\O1-EN-slot22.mp4` | 159 | 5.318 s | 6,664,965 |

**Note:** `O1-TA-slot27` has 158 frames, one under the item's 159–160. That is the slot length itself: 5.294 s × 30 fps = 158.8, and
ffmpeg keeps whole frames. Not re-cut.

Slot sheet: `_cuts\_gateA\gateA-slots.png` (2180×544) — one row per cut in the order above, 8 frames at 0.0, 0.67, 1.35, 2.02, 2.70,
3.37, 4.04, 4.72 s, each 240 wide, the file name burned in at the left (260 px label column). Intermediate row images were made in
CC's scratch folder, not in the song folder.

## Step 7 — commit
Message `Karadi rev 2.5 gate A (3rd issue): HKa rendered, sheets, slot cuts [skip ci]`, explicit paths: `comfy/wan3_api.py`,
`tests/test_wan3_retry_mock.py`, `songs/a12-karadi-w3/shots.csv`, `songs/a12-karadi-w3/batch_gateA.log`,
`songs/a12-karadi-w3/batch_gateA3.log`, `queue/2026-10-14-karadi-rev25-gateA3`, `queue/A12-WATCH.md`, `queue/A12-WATCH-LOG.md`.
`queue/2026-10-13-karadi-rev24-picnic-archive` had no changes (already committed in `5d9d8bb`). Nothing else under
`songs/a12-karadi-w3/` was changed (`out/` is git-ignored). The hash is in this folder's `LOG.md` and `item-01.done` (this report is
inside that commit). Not in the list and left uncommitted: `queue/2026-10-13-karadi-rev23-gateA2/LOG.md` and `item-01.report.md`
(CC's earlier time corrections), and an unrelated `songs/shorts-learning/REVIEW-learning-batch1-2026-09-29.md`.

## Spend
$0.80 list in this queue. A12: $16.10 + $0.80 = **$16.90 list** of the $29.50 cap.
