# item-01 — ZK1 and ZO both rendered. Est $2.00 list. No failures.

The clips were not judged.

## Step 1 — old take kept (renamed, nothing copied or deleted)
14 files renamed with `-v1-awake` before the extension:
- `out\`: `ZK1-seed30313-w3.mp4` → `ZK1-seed30313-w3-v1-awake.mp4`, `ZK1-seed30313-w3.json` → `ZK1-seed30313-w3-v1-awake.json`
- `out\_qc\`: `FABLE-ZK1-action-f140-236.jpg`, `FABLE-ZK1-brinjal-eyes.jpg`, `ZK1-contact.png`, `ZK1-every10.png`,
  `ZK1-every4-first2s.png`, `ZK1-f000.png`, `ZK1-f075.png`, `ZK1-f140.png`, `ZK1-f150.png`, `ZK1-f210.png`, `ZK1-f299.png`,
  `ZK1-strip.png` — each now `<name>-v1-awake.<ext>`

**Status cells:** ZK1 and ZO were both already `todo` in `shots.csv`. No cell was reset; I did not edit `shots.csv`.

## Checks (all passed)
2. `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
3. Credentials: `credentials present: True`. No values were printed.
4. `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`;
   `py comfy\prompt_lint.py --song songs\l05-urulai-w3` → `LINT PASS: 17 shots, 0 fail, 0 warn`
5. Dry-run (`--only ZK1,ZO --hosts api --dry-run`), exit 0, 2 rows, case-sensitive grep for
   `MISSING|ERROR|OVER BUDGET|refused|Traceback`: 0 hits.
   - ZK1: `wan3.0-video 720P 16:9 10s audio=off, est $1.00 (list price); refs=3` —
     `refs/send/10-baby-potato.jpg`, `refs/send/12-brinjal-asleep.jpg`, `refs/send/20-kitchen-shelf-set.jpg` (0.50 MB)
   - ZO: `wan3.0-video 720P 16:9 10s audio=off, est $1.00 (list price); refs=10` — `refs/send/10-baby-potato.jpg`,
     `11-amma-potato.jpg`, `12-brinjal-asleep.jpg`, `13-okra-asleep.jpg`, `14-tomato-asleep.jpg`, `15-carrot-asleep.jpg`,
     `16-radish-asleep.jpg`, `17-cabbage-asleep.jpg`, `18-beans-asleep.jpg`, `20-kitchen-shelf-set.jpg`
   - **ZO ref bytes: 1,685,009 (1.69 MB)** for the 10 files (gate1b sent about 25 MB of PNG).
   - `engine=wan3 rows: estimated $2.00 at list price`

## Render
Command as written in the item (`--max-usd 2.10 --timeout-min 40`), log `songs\l05-urulai-w3\batch_gate1c.log` (no URLs in it).
**Run window:** 18:55:29 → 19:03:21 UTC, 2026-10-09 (14:55:29 → 15:03:21 Toronto EDT). Runner exit code 0.

| Clip | Status | Task id | Wall s | Length | Frames | Refs | Est (list) |
|---|---|---|---|---|---|---|---|
| ZK1 | done | `5a577418-fcb2-4978-8126-d7d0e658a5b3` | 211.4 | 10.000 s, 1280×720, 30 fps, h264, no audio stream | 300 | 3 | $1.00 |
| ZO | done | `9a7df501-8d4e-4a44-838f-bb8a32984eb2` | 259.1 | 10.000 s, 1280×720, 30 fps, h264, no audio stream | 300 | 10 | $1.00 |

**Total estimate: $2.00 list** (under the $2.10 cap). **Failure lines: none.**
Frames counted with ffprobe `-count_frames`. Sidecars have no URL or key in them.

## Sheets and stills — `songs\l05-urulai-w3\out\_qc\` (`out\` is not committed)
For each of `ZK1` and `ZO`:
- `<ID>-contact.png` — 5×2, frames 0, 33, 66, 100, 133, 166, 199, 233, 266, 299, 384 wide each
- `<ID>-every4-first2s.png` — frames 0, 4, 8, … 60 (16 frames), 4×4, 256 wide, frame number burned in
- `<ID>-every10.png` — frames 0, 10, … 290 (30 frames), 6×5, 256 wide, frame number burned in
- 100% stills (1280×720): `<ID>-f000.png`, `-f075.png`, `-f140.png`, `-f150.png`, `-f210.png`, `-f299.png` (last frame)
- `<ID>-strip.png` — the runner's own QC strip

Clips: `songs\l05-urulai-w3\out\ZK1-seed30313-w3.mp4` (8.7 MB) and `ZO-seed30313-w3.mp4` (9.9 MB), each with a `.json` sidecar.

## Commit
See the last line of `LOG.md` for the hash (this report is part of that commit).
Not in the commit, because the item does not list it: `queue\2026-10-09-urulai-gate1b\FABLE-VERDICT.md` (still untracked).
