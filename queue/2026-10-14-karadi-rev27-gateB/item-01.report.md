# item-01 report — DONE: CQ0, CQa, CAa, I1 rendered ($3.10), no scene cuts found, sheets, slot cuts — **one slot mapping to check (CQa)**

Run by CC (A12 watcher), 2026-10-14 16:41–17:05 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
One render run, no retries. The clips were not judged.

## Step 1 — rebuild (path quoted this time; no stray folder)
```
ok 21 clips 146 s $14.60 list $17.50 w/ reserve slots TA 29 EN 24 set image
SELFTEST OK: place, facing, word-action, pacing, camera rules all refuse a bad clip
```
- Lint → `LINT PASS: 21 shots, 0 fail, 0 warn`
- `make_cutplan.py songs\a12-karadi-w3` → `wrote songs\a12-karadi-w3\cutplan.json: TA 29 slots 154.800 s, EN 24 slots 128.000 s, 21 clips — all slots fit their clips, no gaps`
  (`cutplan.json` changed: 4 lines, +4 −4 — the HKa trim / O1 key window). No `shots\*.raw.txt` changed.
- Status list: `I1=todo CQ0=todo CQa=todo CQb=todo HKa=done HKc=todo HKb=todo JOIN=todo CAa=todo CAb=todo V1Q=todo V1A=done V2Q=todo
  V2A=done V3Q=todo V3A=done V4Q=todo V4A=done O1=done O2=todo O3=todo` — HKa, O1, V1A–V4A `done`; CQ0, CQa, CAa, I1 `todo`. OK.

## Step 2 — rev 1.x leftovers renamed (`mv -n`, nothing deleted)
The rev 1.x `.mp4` takes for CQa, CAa and I1 were already in `out\_rev1x-2026-10-13\` (moved by the rev 2.1 queue), so no `.mp4` was at
the top of `out\`. Their **sidecars were** (the 12 stale sidecars flagged earlier):
- `CQa-seed30313-w3.json` → `CQa-seed30313-w3-v1-picnic.json`; same for `CAa` and `I1`.

**Extra, beyond the item's wording:** their rev 1.x QC sheets were still under the plain names in `out\_qc\` and step 6 would have hit
them, so CC renamed those too (30 files, `<name>.png` → `<name>-v1-picnic.png`, no collisions): `CAa-` and `CQa-` `contact`,
`every4-all`, `every4-first2s`, `f000` `f030` `f060` `f120` `f180` `f239`, `strip`; `I1-` `contact`, `every4-all`, `f000` `f030` `f060`
`f090` `f120` `f150` `f209`, `strip`.

## Step 3
- `py tests\test_wan3_retry_mock.py` → `PASS test_wan3_retry_mock: 10 checks`
- Credentials check → `credentials present: True`

## Step 4 — dry-run
4 rows (runner order I1, CQ0, CQa, CAa), all `720P 16:9 audio=off`:
- **I1** 7 s, est $0.70, refs=5: `01-mintu-front`, `02-minnu-front`, `06-amma-front`, `07-appa-face`, `08b-appa-body-backpack` (no set plate)
- **CQ0**, **CQa**, **CAa** — each 8 s, est $0.80, refs=7: `01`, `02`, `03-karadi-mama`, `06`, `07`, `08b-appa-body-backpack`, `11-set-path-low`;
  labels `['Mintu', 'Minnu', 'Karadi Mama', 'Amma', 'Appa', 'Appa', 'the lower forest path set']`
- Total: `engine=wan3 rows: estimated $3.10 at list price`. No `ERROR` / `MISSING` / `OVER BUDGET` / `Traceback`.

## Step 5 — render: all four DONE
Command as given, log `songs\a12-karadi-w3\batch_gateB.log` (checked: no URL in it or in any of the four sidecars).

**Run window:** 2026-10-14 20:42:26 – 20:55:15 UTC = 16:42:26 – 16:55:15 Toronto (EDT).

| Clip | Status | Task id | Wall s | Length | Frames | Refs | Est |
|---|---|---|---|---|---|---|---|
| I1 | done | `82d8f4d3-c155-47ea-99ef-78c43a7d6b57` | 163.7 | 7.000 s, 1280×720, 30 fps | 210 | 5 | $0.70 |
| CQ0 | done | `d42d2c15-61b3-424a-9702-78df7392825e` | 212.5 | 8.000 s, 1280×720, 30 fps | 240 | 7 | $0.80 |
| CQa | done | `56555e97-bbc8-42be-839d-5d7690fa09b0` | 195.4 | 8.000 s, 1280×720, 30 fps | 240 | 7 | $0.80 |
| CAa | done | `0e4b5c28-30d0-4ca7-b083-d7088b398e6f` | 195.1 | 8.000 s, 1280×720, 30 fps | 240 | 7 | $0.80 |

No retry lines, no `NOT resubmitted` lines; every task went submitted → RUNNING → SUCCEEDED. The runner's table:
```
SHOT       STATUS       WALL_S  FILE
I1         done          163.7  songs/a12-karadi-w3\out\I1-seed30313-w3.mp4
CQ0        done          212.5  songs/a12-karadi-w3\out\CQ0-seed30313-w3.mp4
CQa        done          195.4  songs/a12-karadi-w3\out\CQa-seed30313-w3.mp4
CAa        done          195.1  songs/a12-karadi-w3\out\CAa-seed30313-w3.mp4

total GPU-minutes (done shots): 12.8
```
Bytes: I1 11,499,459; CQ0 9,400,429; CQa 8,435,445; CAa 9,371,976. `shots.csv`: the four → `done` (runner's own update).
**Runner's final estimate: $3.10.**

## Step 6 — QC sheets and the cut check
**Scene-cut check** (`select='gt(scene,0.35)',showinfo`): **I1 — none. CQ0 — none. CQa — none. CAa — none.**

In `songs\a12-karadi-w3\out\_qc\` (new files, ffmpeg `-n`):
- `<ID>-contact.png` (5×2, each tile 384 wide, 1920×432; burned number = tile index 0–9, source frames evenly spaced first → last)
- `<ID>-every4-all.png` (every 4th frame, source frame number burned in, 192 wide, 10 per row; 1920×648 each — I1 53 tiles, the others 60)
- stills `<ID>-f000/f030/f060/f090/f120/f150/f180.png` + last (`I1-f209.png`; `CQ0-`, `CQa-`, `CAa-f239.png`)
for ID = I1, CQ0, CQa, CAa.

## Step 7 — slot cuts with the music
Folder created: `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateB\`. Same form as the gate A cuts (1920×1080, 30 fps,
H.264 CRF 16, AAC 256k 48 kHz, `-n`). Slips/starts/lengths read from the rebuilt `karadi-shots.json` `cutplan.ta` / `cutplan.en`.

| file | take | slip | WAV start | length | frames |
|---|---|---|---|---|---|
| `CQ0-TA-slot02.mp4` | CQ0 | 0.400 | 5.735 | 5.341 | 160 |
| `CQ0-EN-slot02.mp4` | CQ0 | 0.400 | 5.759 | 5.317 | 159 |
| `CQa-TA-slot08.mp4` | CQa | 0.400 | 37.732 | 5.364 | 160 |
| `CQa-EN-slot07.mp4` | CQa | 0.400 | 32.299 | 5.341 | 160 |
| `CAa-TA-slot04.mp4` | CAa | 0.400 | 16.393 | 5.364 | 160 |
| `CAa-EN-slot03.mp4` | CAa | 0.400 | 11.076 | 5.294 | 158 |
| `I1-TA-slot01.mp4` | I1 | 0.000 | 0.000 | 5.735 | 172 |
| `I1-EN-slot01.mp4` | I1 | 0.000 | 0.000 | 5.759 | 172 |
| `CQa-TA-slot14.mp4` *(extra)* | CQa | 0.400 | 69.730 | 5.363 | 160 |
| `CQa-EN-slot12.mp4` *(extra)* | CQa | 0.400 | 58.909 | 5.341 | 160 |

### CQa slot mapping — please check
The item maps **CQa → TA slot 8 and EN slot 7**. In the rebuilt cut plan those two slots belong to **CQb** (C2 question:
`TA 8 clip=CQb`, `EN 7 clip=CQb`). **CQa's own slots are TA 14 and EN 12** (C3 question). All slots for these clips in the plan:
```
TA 1 I1 · TA 2 CQ0 · TA 4 CAa · TA 8 CQb · TA 14 CQa · TA 16 CAa · TA 20 CQb · TA 26 CQb
EN 1 I1 · EN 2 CQ0 · EN 3 CAa · EN 7 CQb · EN 12 CQa · EN 13 CAa · EN 17 CQb
```
CC cut the CQa take into the slots the item names (`CQa-TA-slot08`, `CQa-EN-slot07`, with those slots' timings), **and** — as $0 extras
in the same folder — into CQa's own slots (`CQa-TA-slot14`, `CQa-EN-slot12`). Fable can keep whichever pair was meant.

Slot sheet: `_cuts\_gateB\gateB-slots.png` (2180×1360) — one row per cut in the table order (the two extras last, labelled "(extra)"),
8 frames at 0.0, 0.67, 1.35, 2.02, 2.70, 3.37, 4.04, 4.72 s, each 240 wide, the file name at the left.

## Step 8 — commit
Message `Karadi rev 2.7 gate B: CQ0, CQa, CAa, I1 rendered, sheets, slot cuts [skip ci]`, explicit paths:
`songs/a12-karadi-w3/shots.csv`, `songs/a12-karadi-w3/cutplan.json`, `songs/a12-karadi-w3/batch_gateB.log` (the only changes under
`songs/a12-karadi-w3/` outside `out/`), `queue/2026-10-14-karadi-rev26-gateA-retake` (its FABLE-VERDICT.md plus CC's done marker,
LOG lines and report time fix), `queue/2026-10-14-karadi-rev27-gateB`, `queue/A12-WATCH-LOG.md`. The hash is in this folder's `LOG.md`
and `item-01.done` (this report is inside that commit).

## Spend
$3.10 list in this queue. A12: $18.40 + $3.10 = **$21.50 list** of the $29.50 cap.
