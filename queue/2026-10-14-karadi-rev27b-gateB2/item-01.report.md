# item-01 report — DONE: rev 2.3 rebuilt, failed CAa kept as `-v2-parentswap`, CAa + CQb rendered at 6 s ($1.20), no scene cuts found, sheets, six slot cuts

Run by CC (A12 watcher), 2026-10-14 21:02–21:13 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
The queue had READY at 17:58; CC held it from 18:02 because Arul had said "hold on" in chat, and started on Arul's "Go" at 21:02.
One render run, no retries. The clips were not judged.

## Step 0
`queue\2026-10-14-karadi-rev27-gateB\item-01.done` exists. OK.

## Step 1 — rebuild rev 2.3 (repo path quoted; no stray folder)
```
ok 21 clips 136 s $13.60 list $16.30 w/ reserve slots TA 29 EN 24 set image
SELFTEST OK: place, facing, word-action, pacing, camera rules all refuse a bad clip
```
- Lint → `LINT PASS: 21 shots, 0 fail, 0 warn`
- `make_cutplan.py` → `wrote songs\a12-karadi-w3\cutplan.json: TA 29 slots 154.800 s, EN 24 slots 128.000 s, 21 clips — all slots fit their clips, no gaps`
- **I1 slip in `cutplan.json`:** both I1 entries (`shots[0]`, `shots[29]`) have `"slip": {}` — no trim. OK.
- Status list: `done` = I1 CQ0 CQa HKa V1A V2A V3A V4A O1; `todo` = CQb HKc HKb JOIN CAa CAb V1Q V2Q V3Q V4Q O2 O3. Exactly as required.
- `git diff --stat songs/a12-karadi-w3/shots`:
  ```
  songs/a12-karadi-w3/shots/09_CAa.raw.txt | 4 ++--
  songs/a12-karadi-w3/shots/10_CAb.raw.txt | 4 ++--
  2 files changed, 4 insertions(+), 4 deletions(-)
  ```
- `shots.csv` durations: CQb 6, CAa 6, CAb 6, HKb 6, O2 6, O3 6. OK. (Full list: I1 7, CQ0 8, CQa 8, HKa 8, HKc 8, O1 7, all others 6.)

## Step 2 — renames (`mv -n`, nothing deleted or overwritten)
- `out\CAa-seed30313-w3.mp4` / `.json` → `out\CAa-seed30313-w3-v2-parentswap.mp4` / `.json`
- `out\_qc\` (11 files, `<name>.png` → `<name>-v2-parentswap.png`): `CAa-contact`, `CAa-every4-all`, `CAa-f000` `f030` `f060` `f090`
  `f120` `f150` `f180` `f239`, `CAa-strip`. (The `CAa-*-v1-picnic.png` files were left alone.)
- `out\CQb-seed30313-w3.mp4` did **not** exist (the rev 1.x take is in `out\_rev1x-2026-10-13\`), but its rev 1.x **sidecar
  `out\CQb-seed30313-w3.json` and 10 QC sheets** were still under the plain names and would have been overwritten. As in gate B, CC renamed
  them with `-v1-picnic`: `CQb-seed30313-w3.json` → `CQb-seed30313-w3-v1-picnic.json`; `out\_qc\CQb-contact`, `-every4-all`, `-f000`
  `f030` `f060` `f090` `f120` `f150` `f239`, `-strip` → `…-v1-picnic.png`. No collisions.

## Step 3
- `py tests\test_wan3_retry_mock.py` → `PASS test_wan3_retry_mock: 10 checks`
- Credentials check → `credentials present: True`

## Step 4 — dry-run
- **CQb** — `wan3: wan3.0-video 720P 16:9 6s audio=off, est $0.60 (list price); refs=7 labels=['Mintu', 'Minnu', 'Karadi Mama', 'Amma',
  'Appa', 'Appa', 'the upper hill path set']` — refs `01`, `02`, `03-karadi-mama`, `06`, `07`, `08b-appa-body-backpack`, `12-set-path-high`
- **CAa** — `wan3: wan3.0-video 720P 16:9 6s audio=off, est $0.60 (list price); refs=7 labels=[…, 'the lower forest path set']` —
  refs `01`, `02`, `03-karadi-mama`, `06`, `07`, `08b-appa-body-backpack`, `11-set-path-low`
- Total: `engine=wan3 rows: estimated $1.20 at list price`. No `ERROR` / `MISSING` / `OVER BUDGET` / `Traceback`.

## Step 5 — render: both DONE
Command as given, log `songs\a12-karadi-w3\batch_gateB2.log` (checked: no URL in it or in either sidecar).

**Run window:** 2026-10-15 01:05:53 – 01:11:54 UTC = 2026-10-14 21:05:53 – 21:11:54 Toronto (EDT).

| Clip | Status | Task id | Wall s | Length | Frames | Refs | Est |
|---|---|---|---|---|---|---|---|
| CQb | done | `53245f59-4305-4856-9dd9-6ff68d2fb2a6` | 180.0 | 6.000 s, 1280×720, 30 fps | 180 | 7 | $0.60 |
| CAa | done | `8fbc301e-3729-4f05-b437-b274a55c0f98` | 179.4 | 6.000 s, 1280×720, 30 fps | 180 | 7 | $0.60 |

No retry lines, no `NOT resubmitted` lines. The log, verbatim:
```
[CQb] -> wan3 wan3.0-video 720P 16:9 6s refs=7 first=False last=False est $0.60
  wan3 submitted task 53245f59-4305-4856-9dd9-6ff68d2fb2a6
  wan3 task 53245f59-4305-4856-9dd9-6ff68d2fb2a6: RUNNING
  wan3 task 53245f59-4305-4856-9dd9-6ff68d2fb2a6: SUCCEEDED
[CQb] done in 180.0s -> songs/a12-karadi-w3\out\CQb-seed30313-w3.mp4 (running list-price estimate $0.60)
[CAa] -> wan3 wan3.0-video 720P 16:9 6s refs=7 first=False last=False est $0.60
  wan3 submitted task 8fbc301e-3729-4f05-b437-b274a55c0f98
  wan3 task 8fbc301e-3729-4f05-b437-b274a55c0f98: RUNNING
  wan3 task 8fbc301e-3729-4f05-b437-b274a55c0f98: SUCCEEDED
[CAa] done in 179.4s -> songs/a12-karadi-w3\out\CAa-seed30313-w3.mp4 (running list-price estimate $1.20)

SHOT       STATUS       WALL_S  FILE
CQb        done          180.0  songs/a12-karadi-w3\out\CQb-seed30313-w3.mp4
CAa        done          179.4  songs/a12-karadi-w3\out\CAa-seed30313-w3.mp4

total GPU-minutes (done shots): 6.0
```
Bytes: CQb 7,144,034; CAa 7,557,565. `shots.csv`: both → `done` (runner's own update). **Runner's final estimate: $1.20.**

## Step 6 — QC sheets and the cut check
**Scene-cut check** (`select='gt(scene,0.35)',showinfo`): **CQb — none. CAa — none.**

In `songs\a12-karadi-w3\out\_qc\` (new files, ffmpeg `-n`), for CQb and CAa:
- `<ID>-contact.png` — 5×2, tiles 384 wide (1920×432); burned number = tile index 0–9; source frames 0, 19, 39, 59, 79, 99, 119, 139, 159, 179.
- `<ID>-every4-all.png` — every 4th frame, source number burned in, 192 wide, 10 per row (45 tiles, 1920×540).
- stills `<ID>-f000/f030/f060/f090/f120/f150.png` and the last, `<ID>-f179.png`.

## Step 7 — slot cuts with the music
All six slot ids checked against the rebuilt `karadi-shots.json` first — **all match** (CAa TA 4 / EN 3; CQb TA 8 / EN 7; CQa TA 14 / EN 12).
Folder created: `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateB2\`. Same form as the Gate B cuts (1920×1080, 30 fps,
H.264 CRF 16, AAC 256k 48 kHz, `-n`).

| file | take | slip | WAV start | length | frames |
|---|---|---|---|---|---|
| `CAa-TA-slot04.mp4` | CAa (new, 6 s) | 0.400 | 16.393 | 5.364 | 160 |
| `CAa-EN-slot03.mp4` | CAa (new, 6 s) | 0.400 | 11.076 | 5.294 | 158 |
| `CQb-TA-slot08.mp4` | CQb (new, 6 s) | 0.400 | 37.732 | 5.364 | 160 |
| `CQb-EN-slot07.mp4` | CQb (new, 6 s) | 0.400 | 32.299 | 5.341 | 160 |
| `CQa-TA-slot14.mp4` | CQa (gate B take) | **1.900** | 69.730 | 5.363 | 160 |
| `CQa-EN-slot12.mp4` | CQa (gate B take) | **1.900** | 58.909 | 5.341 | 160 |

Slot sheet: `_cuts\_gateB2\gateB2-slots.png` (2180×816) — one row per cut in the table order, 8 frames at 0.0, 0.67, 1.35, 2.02, 2.70,
3.37, 4.04, 4.72 s, each 240 wide, file name at the left. `_cuts\_gateB\` was not touched.

## Step 8 — commit
Message `Karadi rev 2.3 gate B2: CAa retake + CQb at 6 s, sheets, slot cuts [skip ci]`, explicit paths: `songs/a12-karadi-w3/shots.csv`,
`songs/a12-karadi-w3/shots/09_CAa.raw.txt`, `songs/a12-karadi-w3/shots/10_CAb.raw.txt`, `songs/a12-karadi-w3/cutplan.json`,
`songs/a12-karadi-w3/batch_gateB2.log` (the only changes under `songs/a12-karadi-w3/` outside `out/`),
`queue/2026-10-14-karadi-rev27-gateB` (its FABLE-VERDICT.md plus CC's done marker, LOG lines and report time fix),
`queue/2026-10-14-karadi-rev27b-gateB2`, `queue/A12-WATCH-LOG.md`. The hash is in this folder's `LOG.md` and `item-01.done`
(this report is inside that commit).

## Spend
$1.20 list in this queue. A12: $21.50 + $1.20 = **$22.70 list** of the $29.50 cap.
