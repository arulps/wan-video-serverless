# item-01 — all six clips rendered (K3, ZK2, ZK4, ZK7, ZO, I1). Est $5.70 list. No failures.

The clips were not judged. The keepers were not touched: `out\ZK1-seed30313-w3.mp4` (14:59, 8,654,715 bytes) and
`out\CA-seed30313-w3.mp4` (15:37, 7,784,079 bytes) are as they were.

## Step 1 — old ZO and I1 takes kept (renamed, nothing copied or deleted)
**ZO → `-v1b-twocabbage`** (12 files):
- `out\`: `ZO-seed30313-w3.mp4` → `ZO-seed30313-w3-v1b-twocabbage.mp4`, `ZO-seed30313-w3.json` → `ZO-seed30313-w3-v1b-twocabbage.json`
- `out\_qc\`: `ZO-contact.png`, `ZO-every10.png`, `ZO-every4-first2s.png`, `ZO-f000.png`, `ZO-f075.png`, `ZO-f140.png`,
  `ZO-f150.png`, `ZO-f210.png`, `ZO-f299.png`, `ZO-strip.png` — each now `<name>-v1b-twocabbage.png`
  (the earlier `-v1-twobrinjal` files were left alone)

**I1 → `-v1-onshelf`** (12 files):
- `out\`: `I1-seed30313-w3.mp4` → `I1-seed30313-w3-v1-onshelf.mp4`, `I1-seed30313-w3.json` → `I1-seed30313-w3-v1-onshelf.json`
- `out\_qc\`: `I1-contact.png`, `I1-every10.png`, `I1-every4-first2s.png`, `I1-f000.png`, `I1-f075.png`, `I1-f140.png`,
  `I1-f150.png`, `I1-f210.png`, `I1-f329.png`, `I1-strip.png` — each now `<name>-v1-onshelf.png`

**Status cells reset: two.** In `shots.csv`, I1 and ZO were `done` (set by the gate2 run) → each set to `todo`. Those are the
only cells changed (git diff: 2 lines, only those cells differ). K3, ZK2, ZK4 and ZK7 were already `todo`.

## Checks (all passed)
2. `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
3. Credentials: `credentials present: True`. No values were printed.
4. `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`;
   `py comfy\prompt_lint.py --song songs\l05-urulai-w3` → `LINT PASS: 17 shots, 0 fail, 0 warn`
5. Rev 2.5 prompts: `shots\14_ZO.raw.txt` contains "no cabbage in the back row" exactly once;
   `shots\01_I1.raw.txt` contains "never stand, sit or climb on the shelf" exactly once.
6. Dry-run (`--only K3,ZK2,ZK4,ZK7,ZO,I1 --hosts api --dry-run`), exit 0, 6 rows, all `wan3.0-video 720P 16:9 audio=off`,
   case-sensitive grep for `MISSING|ERROR|OVER BUDGET|refused|Traceback`: 0 hits. All refs are from `refs/send/`.
   - I1: 11 s, est $1.10, refs=6 — `01-mintu-front.jpg`, `02-minnu-front.jpg`, `03-minmini-front.jpg`, `10-baby-potato.jpg`,
     `11-amma-potato.jpg`, `20-kitchen-shelf-set.jpg`
   - ZK2: 10 s, est $1.00, refs=3 — `10-baby-potato.jpg`, `13-okra-asleep.jpg`, `20-kitchen-shelf-set.jpg`
   - ZK4: 10 s, est $1.00, refs=3 — `10-baby-potato.jpg`, `15-carrot-asleep.jpg`, `20-kitchen-shelf-set.jpg`
   - ZK7: 10 s, est $1.00, refs=3 — `10-baby-potato.jpg`, `18-beans-asleep.jpg`, `20-kitchen-shelf-set.jpg`
   - K3: 6 s, est $0.60, refs=3 — `10-baby-potato.jpg`, `14-tomato-asleep.jpg`, `20-kitchen-shelf-set.jpg`
   - ZO: 10 s, est $1.00, refs=10 — baby, amma, the seven `*-asleep.jpg` (brinjal, okra, tomato, carrot, radish, cabbage,
     beans), set
   - `engine=wan3 rows: estimated $5.70 at list price`

## Render
Command as written in the item (`--max-usd 5.80 --timeout-min 70`), log `songs\l05-urulai-w3\batch_gate3.log` (no URLs in it).
**Run window:** 19:45:25 → 20:08:12 UTC, 2026-10-09 (15:45:25 → 16:08:12 Toronto EDT). Runner exit code 0.
The runner rendered in `shots.csv` order: I1, ZK2, ZK4, ZK7, K3, ZO.

| Clip | Status | Task id | Wall s | Length | Frames | Refs | Est (list) |
|---|---|---|---|---|---|---|---|
| I1 | done | `07cff5bb-2196-407c-b53c-8ce8e77e096f` | 260.4 | 11.000 s | 330 | 6 | $1.10 |
| ZK2 | done | `a4b310e2-6be0-4579-9f52-328598db4645` | 210.9 | 10.000 s | 300 | 3 | $1.00 |
| ZK4 | done | `73a1b162-3ea1-43ce-9ff7-ae06e427ec79` | 211.6 | 10.000 s | 300 | 3 | $1.00 |
| ZK7 | done | `f661991f-3f6a-4815-8968-7e4a00892ac9` | 211.1 | 10.000 s | 300 | 3 | $1.00 |
| K3 | done | `b3cb22d3-a5e0-4f2a-8491-b9bcd4b3472b` | 146.9 | 6.000 s | 180 | 3 | $0.60 |
| ZO | done | `c8a0be3e-f97f-4045-aa34-5db9dc84db65` | 322.3 | 10.000 s | 300 | 10 | $1.00 |

All six: 1280×720, 30 fps, h264, no audio stream. Frames counted with ffprobe `-count_frames`.
**Total estimate: $5.70 list** (under the $5.80 cap). **Failure lines: none.** Sidecars have no URL or key in them.

## Sheets and stills — `songs\l05-urulai-w3\out\_qc\` (`out\` is not committed)
For each of `I1`, `ZK2`, `ZK4`, `ZK7`, `K3`, `ZO`:
- `<ID>-contact.png` — 5×2, 10 frames evenly spaced, 384 wide each
  (330-frame clip: 0, 37, 73, 110, 146, 183, 219, 256, 292, 329 · 300-frame clips: 0, 33, 66, 100, 133, 166, 199, 233, 266, 299 ·
  K3: 0, 20, 40, 60, 80, 99, 119, 139, 159, 179)
- `<ID>-every4-first2s.png` — frames 0, 4, … 60 (16 frames), 4×4, 256 wide, frame number burned in
- `<ID>-every10.png` — every 10th frame, 6 columns, 256 wide, frame number burned in
  (I1: 33 frames, 6 rows, last row half empty · ZK2, ZK4, ZK7, ZO: 30 frames, 5 rows · K3: 18 frames, 3 rows)
- 100% stills (1280×720): `<ID>-f000.png`, `-f075.png`, `-f140.png`, `-f150.png`, `-f210.png`, and the last frame:
  `I1-f329.png`, `ZK2-f299.png`, `ZK4-f299.png`, `ZK7-f299.png`, `K3-f179.png`, `ZO-f299.png`
  - **K3 has no `-f210.png`**: the clip is 180 frames (6 s), so frame 210 does not exist. Its stills are f000, f075, f140,
    f150 and f179.
- `<ID>-strip.png` — the runner's own QC strip

Clips in `out\`: `I1-seed30313-w3.mp4` (10.6 MB), `ZK2-…` (8.6 MB), `ZK4-…` (8.2 MB), `ZK7-…` (8.3 MB), `K3-…` (5.0 MB),
`ZO-…` (11.3 MB), each with a `.json` sidecar.

## Commit
See the last line of `LOG.md` for the hash (this report is part of that commit).
