# item-01 — ZO, CA and I1 all rendered. Est $2.90 list. No failures.

The clips were not judged. ZK1 was not touched (`out\ZK1-seed30313-w3.mp4` still dated 14:59, 8,654,715 bytes).

## Step 1 — old ZO take kept (renamed, nothing copied or deleted)
12 files renamed with `-v1-twobrinjal` before the extension:
- `out\`: `ZO-seed30313-w3.mp4` → `ZO-seed30313-w3-v1-twobrinjal.mp4`, `ZO-seed30313-w3.json` → `ZO-seed30313-w3-v1-twobrinjal.json`
- `out\_qc\`: `ZO-contact.png`, `ZO-every10.png`, `ZO-every4-first2s.png`, `ZO-f000.png`, `ZO-f075.png`, `ZO-f140.png`,
  `ZO-f150.png`, `ZO-f210.png`, `ZO-f299.png`, `ZO-strip.png` — each now `<name>-v1-twobrinjal.png`

**Status cells reset: one.** In `shots.csv`, ZO's `status` was `done` (set by the gate1c run) → set to `todo`. That is the only
cell changed (git diff: 1 line, only that cell differs). CA and I1 were already `todo`. ZK1's status was left as `done`.

## Checks (all passed)
2. `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
3. Credentials: `credentials present: True`. No values were printed.
4. `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`;
   `py comfy\prompt_lint.py --song songs\l05-urulai-w3` → `LINT PASS: 17 shots, 0 fail, 0 warn`
5. ZO prompt is rev 2.4: `shots\14_ZO.raw.txt` has exactly one line containing "no brinjals at all"
   ("… but no brinjals at all: Brinjal, the character, is the only pu…"). Checked with grep, not `findstr`; same test.
6. Dry-run (`--only ZO,CA,I1 --hosts api --dry-run`), exit 0, 3 rows, case-sensitive grep for
   `MISSING|ERROR|OVER BUDGET|refused|Traceback`: 0 hits. All refs are from `refs/send/`.
   - I1: `wan3.0-video 720P 16:9 11s audio=off, est $1.10 (list price); refs=6` — `01-mintu-front.jpg`, `02-minnu-front.jpg`,
     `03-minmini-front.jpg`, `10-baby-potato.jpg`, `11-amma-potato.jpg`, `20-kitchen-shelf-set.jpg`
   - ZO: `wan3.0-video 720P 16:9 10s audio=off, est $1.00 (list price); refs=10` — `10-baby-potato.jpg`, `11-amma-potato.jpg`,
     `12-brinjal-asleep.jpg`, `13-okra-asleep.jpg`, `14-tomato-asleep.jpg`, `15-carrot-asleep.jpg`, `16-radish-asleep.jpg`,
     `17-cabbage-asleep.jpg`, `18-beans-asleep.jpg`, `20-kitchen-shelf-set.jpg`
   - CA: `wan3.0-video 720P 16:9 8s audio=off, est $0.80 (list price); refs=3` — `10-baby-potato.jpg`, `11-amma-potato.jpg`,
     `20-kitchen-shelf-set.jpg`
   - `engine=wan3 rows: estimated $2.90 at list price`

## Render
Command as written in the item (`--max-usd 3.00 --timeout-min 45`), log `songs\l05-urulai-w3\batch_gate2.log` (no URLs in it).
**Run window:** 19:25:38 → 19:37:12 UTC, 2026-10-09 (15:25:38 → 15:37:12 Toronto EDT). Runner exit code 0.
The runner rendered in `shots.csv` order: I1, ZO, CA.

| Clip | Status | Task id | Wall s | Length | Frames | Refs | Est (list) |
|---|---|---|---|---|---|---|---|
| I1 | done | `3d070981-d0e7-459f-9771-622937be8baf` | 244.7 | 11.000 s | 330 | 6 | $1.10 |
| ZO | done | `4a74ec37-9e72-41a2-8ee5-723896d92bc4` | 268.7 | 10.000 s | 300 | 10 | $1.00 |
| CA | done | `3e722f0b-cb55-49aa-8a09-9078fd117c1e` | 179.0 | 8.000 s | 240 | 3 | $0.80 |

All three: 1280×720, 30 fps, h264, no audio stream. Frames counted with ffprobe `-count_frames`.
**Total estimate: $2.90 list** (under the $3.00 cap). **Failure lines: none.** Sidecars have no URL or key in them.

## Sheets and stills — `songs\l05-urulai-w3\out\_qc\` (`out\` is not committed)
For each of `I1`, `ZO`, `CA`:
- `<ID>-contact.png` — 5×2, 10 frames evenly spaced, 384 wide each
  (I1: 0, 37, 73, 110, 146, 183, 219, 256, 292, 329 · ZO: 0, 33, 66, 100, 133, 166, 199, 233, 266, 299 ·
  CA: 0, 27, 53, 80, 106, 133, 159, 186, 212, 239)
- `<ID>-every4-first2s.png` — frames 0, 4, … 60 (16 frames), 4×4, 256 wide, frame number burned in
- `<ID>-every10.png` — every 10th frame, 6 columns, 256 wide, frame number burned in
  (I1: 33 frames, 6 rows, last row half empty · ZO: 30 frames, 5 rows · CA: 24 frames, 4 rows)
- 100% stills (1280×720): `<ID>-f000.png`, `-f075.png`, `-f140.png`, `-f150.png`, `-f210.png`, and the last frame:
  `I1-f329.png`, `ZO-f299.png`, `CA-f239.png`
- `<ID>-strip.png` — the runner's own QC strip

Clips: `out\I1-seed30313-w3.mp4` (10.9 MB), `out\ZO-seed30313-w3.mp4` (10.5 MB), `out\CA-seed30313-w3.mp4` (7.8 MB), each
with a `.json` sidecar.

## Commit
See the last line of `LOG.md` for the hash (this report is part of that commit).
