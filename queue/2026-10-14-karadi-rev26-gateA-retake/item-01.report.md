# item-01 report — DONE: rev 2.2 rebuilt, Gate A takes kept as `-v1-multishot`, HKa + O1 re-rendered ($1.50), no scene cuts found, sheets, slot cuts

Run by CC (A12 watcher), 2026-10-14 16:11–16:24 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
One render run, no retries. The clips were not judged.

## Step 1 — rebuild
**CC's own slip first (corrected, $0):** CC's first builder call passed `--repo songs\a12-karadi-w3` unquoted in bash, which ate the
backslash; the builder ran and wrote its repo layout into a stray folder `songsa12-karadi-w3\` at the repo root (38 files) and left
`songs\a12-karadi-w3\` untouched — so the first checks showed the old rev 2.1 prompts and HKa/O1 `done`. Nothing was rendered on that
state. CC moved the stray folder out of the repo (`mv -n`, not deleted; it is now in CC's scratch folder, never committed) and ran the
item's command again with the path quoted. The song-folder files (`karadi-shots.json`, `KARADI-MAMA-WAN3-RUNSHEET.md`) were written by
both runs from the same inputs.

The run that counts:
```
ok 21 clips 146 s $14.60 list $17.50 w/ reserve slots TA 29 EN 24 set image
SELFTEST OK: place, facing, word-action, pacing, camera rules all refuse a bad clip
```
- `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`
- `shots\05_HKa.raw.txt`: line 2 starts `Generate single shot. One continuous shot from the first frame to the last: no cuts throughout, …`;
  "dance his happy dance TOGETHER" — 1 match; "to 1.1 seconds" — 0 matches (and no `seconds,` anywhere in the HKa/O1 dry-run prompts).
- 17 `shots\*.raw.txt` changed (`git diff --stat`: 17 files, +57 −40); the four verse answers `12_V1A`, `14_V2A`, `16_V3A`, `18_V4A`
  unchanged. `lint.json`, `scale.json`, `world.txt`, `characters.txt`, `cutplan.json` and `refs\send\` were rewritten byte-identical
  (no git change).
- Status list after the rebuild: `I1=todo CQ0=todo CQa=todo CQb=todo HKa=todo HKc=todo HKb=todo JOIN=todo CAa=todo CAb=todo V1Q=todo
  V1A=done V2Q=todo V2A=done V3Q=todo V3A=done V4Q=todo V4A=done O1=todo O2=todo O3=todo` — HKa and O1 `todo`, V1A–V4A `done`, the
  other 15 `todo`. OK.

## Step 2 — Gate A takes kept (renamed with `mv -n`, nothing deleted or overwritten)
In `songs\a12-karadi-w3\out\`:
- `HKa-seed30313-w3.mp4` / `.json` → `HKa-seed30313-w3-v1-multishot.mp4` / `.json`
- `O1-seed30313-w3.mp4` / `.json` → `O1-seed30313-w3-v1-multishot.mp4` / `.json`

In `out\_qc\` (30 files, each `<name>.png` → `<name>-v1-multishot.png`):
`HKa-contact`, `HKa-every4-all`, `HKa-f000` `f012` `f024` `f036` `f048` `f060` `f072` `f090` `f120` `f150` `f180` `f239`, `HKa-strip`;
`O1-contact`, `O1-every4-all`, `O1-f000` `f012` `f024` `f036` `f048` `f060` `f072` `f090` `f120` `f150` `f180` `f209`, `O1-strip`.
(The older `_qc\_rev1x-2026-10-13\` and `*-v1-picnic*` files were left as they were.)

## Step 3
- `py tests\test_wan3_retry_mock.py` → `PASS test_wan3_retry_mock: 10 checks`
- Credentials check → `credentials present: True`

## Step 4 — dry-run
- **HKa** — `wan3: wan3.0-video 720P 16:9 8s audio=off, est $0.80 (list price); refs=7 labels=['Mintu', 'Minnu', 'Karadi Mama', 'Amma',
  'Appa', 'Appa', 'the lower forest path set']` (… `08b-appa-body-backpack`, `11-set-path-low`)
- **O1** — `wan3: wan3.0-video 720P 16:9 7s audio=off, est $0.70 (list price); refs=9 labels=['Mintu', 'Minnu', 'Karadi Mama', 'the rabbit',
  'the squirrel', 'Amma', 'Appa', 'Appa', "Karadi Mama's home set"]` (… `08b-appa-body-backpack`, `13-set-home`)
- Total: `engine=wan3 rows: estimated $1.50 at list price`. No `ERROR` / `MISSING` / `OVER BUDGET` / `Traceback`.

## Step 5 — render: both DONE
Command as given, log `songs\a12-karadi-w3\batch_gateA4.log` (checked: no URL in it or in either sidecar).

**Run window:** 2026-10-14 20:13:22 – 20:20:26 UTC = 16:13:22 – 16:20:26 Toronto (EDT).

| Clip | Status | Task id | Wall s | Length | Frames | Refs | Est |
|---|---|---|---|---|---|---|---|
| HKa | done | `357f8474-dfe4-4080-aaae-edb2359a2cae` | 211.8 | 8.000 s, 1280×720, 30 fps | 240 | 7 | $0.80 |
| O1 | done | `1d3be573-3532-4d01-b1f3-5add02ccfdba` | 211.3 | 7.000 s, 1280×720, 30 fps | 210 | 9 | $0.70 |

No retry lines, no `NOT resubmitted` lines. The log, verbatim:
```
[HKa] -> wan3 wan3.0-video 720P 16:9 8s refs=7 first=False last=False est $0.80
  wan3 submitted task 357f8474-dfe4-4080-aaae-edb2359a2cae
  wan3 task 357f8474-dfe4-4080-aaae-edb2359a2cae: RUNNING
  wan3 task 357f8474-dfe4-4080-aaae-edb2359a2cae: SUCCEEDED
[HKa] done in 211.8s -> songs/a12-karadi-w3\out\HKa-seed30313-w3.mp4 (running list-price estimate $0.80)
[O1] -> wan3 wan3.0-video 720P 16:9 7s refs=9 first=False last=False est $0.70
  wan3 submitted task 1d3be573-3532-4d01-b1f3-5add02ccfdba
  wan3 task 1d3be573-3532-4d01-b1f3-5add02ccfdba: RUNNING
  wan3 task 1d3be573-3532-4d01-b1f3-5add02ccfdba: SUCCEEDED
[O1] done in 211.3s -> songs/a12-karadi-w3\out\O1-seed30313-w3.mp4 (running list-price estimate $1.50)

SHOT       STATUS       WALL_S  FILE
HKa        done          211.8  songs/a12-karadi-w3\out\HKa-seed30313-w3.mp4
O1         done          211.3  songs/a12-karadi-w3\out\O1-seed30313-w3.mp4

total GPU-minutes (done shots): 7.1
```
`out\HKa-seed30313-w3.mp4` 10,077,542 bytes; `out\O1-seed30313-w3.mp4` 9,838,044 bytes; sidecars beside them; the runner's strips
`out\_qc\HKa-strip.png`, `out\_qc\O1-strip.png`. `shots.csv`: HKa and O1 → `done` (the runner's own update).
**Runner's final estimate: $1.50.**

## Step 6 — QC sheets and the cut check
**Scene-cut check** (`ffmpeg -i out\<ID>-seed30313-w3.mp4 -vf "select='gt(scene,0.35)',showinfo" -f null -`):
- **HKa: no frames printed.**
- **O1: no frames printed.**

Sheets in `songs\a12-karadi-w3\out\_qc\` (new files; ffmpeg with `-n`):
- `HKa-contact.png`, `O1-contact.png` — 5×2, 10 evenly spaced frames, each 384 wide (1920×432). The burned number is the tile index
  0–9; source frames 0, 26, 53, 79, 106, 132, 159, 185, 212, 239 (HKa) and 0, 23, 46, 69, 92, 116, 139, 162, 185, 209 (O1).
- `HKa-every4-all.png` (60 tiles), `O1-every4-all.png` (53 tiles) — every 4th frame, source frame number burned in, 192 wide, 10 per
  row (both 1920×648).
- 100 % stills (1280×720): `HKa-f000/f012/f024/f036/f048/f060/f072/f090/f120/f150/f180/f239.png` and
  `O1-f000/…/f180/f209.png`.

## Step 7 — slot cuts with the music
Folder created: `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateA2\`. Same files, slips, starts, lengths and ffmpeg
form as gate A3 step 6 (`-n` in place of `-y`; the folder was new). All 1920×1080, 30 fps, H.264 CRF 16, AAC 48 kHz.

| file | frames | duration | bytes |
|---|---|---|---|
| `_cuts\_gateA2\HKa-TA-slot03.mp4` | 159 | 5.317 s | 5,791,269 |
| `_cuts\_gateA2\HKa-EN-slot04.mp4` | 159 | 5.317 s | 5,795,184 |
| `_cuts\_gateA2\O1-TA-slot27.mp4` | 158 | 5.294 s | 6,113,587 |
| `_cuts\_gateA2\O1-EN-slot22.mp4` | 159 | 5.318 s | 6,155,342 |

(`O1-TA-slot27` is 158 frames for the same reason as in gate A3: 5.294 s × 30 = 158.8.)

Slot sheet: `_cuts\_gateA2\gateA2-slots.png` (2180×544) — one row per cut in the order above, 8 frames at 0.0, 0.67, 1.35, 2.02, 2.70,
3.37, 4.04, 4.72 s, each 240 wide, file name burned in at the left. `_cuts\_gateA\` was not touched.

## Step 8 — commit
Message `Karadi rev 2.6 gate A retake: rev 2.2 single-shot prompts, HKa + O1 re-rendered, sheets, slot cuts [skip ci]`, explicit paths:
`songs/a12-karadi-w3/shots.csv`, `songs/a12-karadi-w3/shots`, `songs/a12-karadi-w3/lint.json`, `scale.json`, `world.txt`,
`characters.txt`, `cutplan.json`, `songs/a12-karadi-w3/refs/send` (`-f`), `songs/a12-karadi-w3/batch_gateA4.log`,
`queue/2026-10-14-karadi-rev25-gateA3` (its FABLE-VERDICT.md, plus CC's done marker, LOG lines and report time fix from that queue),
`queue/2026-10-14-karadi-rev26-gateA-retake`, `queue/A12-WATCH-LOG.md`. The hash is in this folder's `LOG.md` and `item-01.done`
(this report is inside that commit).

## Spend
$1.50 list in this queue. A12: $16.90 + $1.50 = **$18.40 list** of the $29.50 cap.
