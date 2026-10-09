# item-01 — all nine clips rendered (SA, SB, Z3, Z5, Z6, K5, K6, CB, O2). Est $5.80 list. No failures.

The clips were not judged. The keepers (ZK1, ZK2, ZK4, ZK7, K3, CA, I1) and every ZO file were not touched — their `out\` files
keep their earlier times (14:59 to 16:08). All 17 `shots.csv` rows now read `done`.

**Start note:** this queue was held for four watch cycles (16:15–16:44) because the total would pass the original $17.00 cap.
Arul confirmed the $18.00 cap in the CC chat, and the queue started at 16:46.

## Step 1 — `shots.csv` cells changed: exactly two
- SA `duration_s`: `8` → `7`
- SB `duration_s`: `8` → `7`

The `status` cells of Z3, Z5, Z6, K5, K6, SA, SB, CB and O2 were all already `todo`; none was reset. Nothing else in
`shots.csv` was changed by hand (git diff before the render: 2 lines, only those two cells differ). The runner then set the
nine status cells to `done`.

## Checks (all passed)
2. `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
3. Credentials: `credentials present: True`. No values were printed.
4. `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`;
   `py comfy\prompt_lint.py --song songs\l05-urulai-w3` → `LINT PASS: 17 shots, 0 fail, 0 warn`
5. `shots\17_O2.raw.txt` contains "standing on the kitchen floor in front of the rack" exactly once.
6. Dry-run (`--only Z3,Z5,Z6,K5,K6,SA,SB,CB,O2 --hosts api --dry-run`), exit 0, 9 rows, all `wan3.0-video 720P 16:9 audio=off`,
   case-sensitive grep for `MISSING|ERROR|OVER BUDGET|refused|Traceback`: 0 hits. All refs are from `refs/send/`.
   - SA: 7 s, est $0.70, refs=2 — `11-amma-potato.jpg`, `20-kitchen-shelf-set.jpg`
   - SB: 7 s, est $0.70, refs=2 — `11-amma-potato.jpg`, `20-kitchen-shelf-set.jpg`
   - Z3: 6 s, est $0.60, refs=3 — `10-baby-potato.jpg`, `14-tomato-asleep.jpg`, `20-kitchen-shelf-set.jpg`
   - Z5: 6 s, est $0.60, refs=3 — `10-baby-potato.jpg`, `16-radish-asleep.jpg`, `20-kitchen-shelf-set.jpg`
   - Z6: 6 s, est $0.60, refs=3 — `10-baby-potato.jpg`, `17-cabbage-asleep.jpg`, `20-kitchen-shelf-set.jpg`
   - K5: 6 s, est $0.60, refs=3 — `10-baby-potato.jpg`, `16-radish-asleep.jpg`, `20-kitchen-shelf-set.jpg`
   - K6: 6 s, est $0.60, refs=3 — `10-baby-potato.jpg`, `17-cabbage-asleep.jpg`, `20-kitchen-shelf-set.jpg`
   - CB: 8 s, est $0.80, refs=3 — `10-baby-potato.jpg`, `11-amma-potato.jpg`, `20-kitchen-shelf-set.jpg`
   - O2: 6 s, est $0.60, refs=4 — `01-mintu-front.jpg`, `02-minnu-front.jpg`, `03-minmini-front.jpg`, `20-kitchen-shelf-set.jpg`
   - `engine=wan3 rows: estimated $5.80 at list price`

## Render
Command as written in the item (`--max-usd 5.90 --timeout-min 80`), log `songs\l05-urulai-w3\batch_gate4.log` (no URLs in it).
**Run window:** 20:46:22 → 21:09:19 UTC, 2026-10-09 (16:46:22 → 17:09:19 Toronto EDT). Runner exit code 0.
The runner rendered in `shots.csv` order: SA, SB, Z3, Z5, Z6, K5, K6, CB, O2.

| Clip | Status | Task id | Wall s | Length | Frames | Refs | Est (list) |
|---|---|---|---|---|---|---|---|
| SA | done | `4d0ba2aa-ba86-45bf-b725-11dbbe7b7a2d` | 147.8 | 7.000 s | 210 | 2 | $0.70 |
| SB | done | `de03132f-4bc7-4a7f-8097-d3c412073fdb` | 163.4 | 7.000 s | 210 | 2 | $0.70 |
| Z3 | done | `0733a573-1ae6-4d4a-a92d-32eabab260c3` | 147.2 | 6.000 s | 180 | 3 | $0.60 |
| Z5 | done | `bddcf8b0-a211-42ec-9e2e-5b32fdb8c74d` | 147.4 | 6.000 s | 180 | 3 | $0.60 |
| Z6 | done | `bb37889a-74e1-4f8c-a32a-01a1b46891b5` | 147.0 | 6.000 s | 180 | 3 | $0.60 |
| K5 | done | `4e33fda8-1215-47e1-8161-f23e8eeaa799` | 146.8 | 6.000 s | 180 | 3 | $0.60 |
| K6 | done | `e4a449d3-58d6-4d96-81e7-597d6b5dce73` | 147.0 | 6.000 s | 180 | 3 | $0.60 |
| CB | done | `0b934fc0-90a3-4020-ac15-922c47722090` | 178.6 | 8.000 s | 240 | 3 | $0.80 |
| O2 | done | `ce551886-bac6-4c94-986b-b3dc32781878` | 146.5 | 6.000 s | 180 | 4 | $0.60 |

All nine: 1280×720, 30 fps, h264, no audio stream. Frames counted with ffprobe `-count_frames`.
**Total estimate: $5.80 list** (under the $5.90 cap). **Failure lines: none.** Sidecars have no URL or key in them.
**L05 total so far: $17.40 list of $18.00** ($1.00 + $2.00 + $2.90 + $5.70 + $5.80).

## Sheets and stills — `songs\l05-urulai-w3\out\_qc\` (`out\` is not committed)
For each of the nine IDs:
- `<ID>-contact.png` — 5×2, 10 frames evenly spaced, 384 wide each
  (180-frame clips: 0, 20, 40, 60, 80, 99, 119, 139, 159, 179 · SA, SB: 0, 23, 46, 70, 93, 116, 139, 163, 186, 209 ·
  CB: 0, 27, 53, 80, 106, 133, 159, 186, 212, 239)
- `<ID>-every4-first2s.png` — frames 0, 4, … 60 (16 frames), 4×4, 256 wide, frame number burned in
- `<ID>-every10.png` — every 10th frame, 6 columns, 256 wide, frame number burned in
  (180-frame clips: 18 frames, 3 rows · SA, SB: 21 frames, 4 rows, last row half empty · CB: 24 frames, 4 rows)
- 100% stills (1280×720): `<ID>-f000.png`, `-f075.png`, `-f140.png`, `-f150.png` for every clip, plus the last frame:
  - Z3, Z5, Z6, K5, K6, O2 (180 frames): `-f179.png`. No f210 (the clip does not have it).
  - SA, SB (210 frames): `-f209.png`. No f210 (the last frame is 209).
  - CB (240 frames): `-f210.png` and `-f239.png`.
- `<ID>-strip.png` — the runner's own QC strip

Clips in `out\`: `SA-seed30313-w3.mp4` (6.8 MB), `SB-…` (8.0 MB), `Z3-…` (5.1 MB), `Z5-…` (5.0 MB), `Z6-…` (5.6 MB),
`K5-…` (5.2 MB), `K6-…` (5.3 MB), `CB-…` (9.0 MB), `O2-…` (6.3 MB), each with a `.json` sidecar.

## Commit
See the last line of `LOG.md` for the hash (this report is part of that commit).
