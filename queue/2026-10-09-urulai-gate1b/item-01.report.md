# item-01 — ZK1 rendered; ZO FAILED at submission (not re-run). Est $1.00 list.

**Result:** 1 of 2 clips. ZK1 is done with its sheets and stills. ZO failed before a task id was returned and was not re-run
(hard limit). The clips were not judged.

## Checks (all passed)
1. `git diff --stat comfy\batch_runner.py` → `1 file changed, 3 insertions(+), 1 deletion(-)`. The only hunk is in
   `write_qc_strip`: the `-vsync 0` pair is gone from the ffmpeg command and a 2-line comment was added. Nothing else changed.
2. `py tests\test_wan3_mock.py` on Beast (ffmpeg 9.0.2) →
   `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
3. Credentials: `credentials present: True`. No values were printed.
4. `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`;
   `py comfy\prompt_lint.py --song songs\l05-urulai-w3` → `LINT PASS: 17 shots, 0 fail, 0 warn`
5. Dry-run (`--only ZK1,ZO --hosts api --dry-run`), exit 0, 2 rows, case-sensitive grep for
   `MISSING|ERROR|OVER BUDGET|refused|Traceback`: 0 hits.
   - ZK1: `wan3.0-video 720P 16:9 10s audio=off, est $1.00 (list price); refs=3` — Baby Potato, Brinjal, the kitchen shelf set
   - ZO: `wan3.0-video 720P 16:9 10s audio=off, est $1.00 (list price); refs=10` — Baby Potato, Amma Potato, Brinjal, Okra,
     Tomato, Carrot, Radish, Cabbage, Beans, the kitchen shelf set
   - `engine=wan3 rows: estimated $2.00 at list price`

## Render
Command as written in the item (`--max-usd 2.10 --timeout-min 40`), log `songs\l05-urulai-w3\batch_gate1.log` (no URLs in it).
**Run window:** 17:55:19 → 18:01:10 UTC, 2026-10-09 (13:55:19 → 14:01:10 Toronto EDT). Runner exit code 0.

| Clip | Status | Task id | Wall s | Length | Frames | Refs | Est (list) |
|---|---|---|---|---|---|---|---|
| ZK1 | done | `2fd27534-90fa-4b8f-8abe-89aa0bec85c1` | 228.6 | 10.000 s, 1280×720, 30 fps, h264, no audio stream | 300 | 3 | $1.00 |
| ZO | **failed** | none logged | 120.7 | — | — | 10 | $0.00 (see below) |

**Total estimate: $1.00 list** (the runner's own running estimate after ZK1; ZO added nothing to it).

**Failure line, verbatim:**
```
[ZO] FAILED (wan3): <urlopen error The write operation timed out>
```
and in the summary table: `ZO         failed        120.7  <urlopen error The write operation timed out>`

What is known about it: the log has no `wan3 submitted task …` line for ZO, so the error came while the request (with its 10
reference images) was being sent, 120.7 s after the row started. `shots.csv` now has ZK1 = `done`, ZO = `failed`.
What is **not** known: whether the API received the request anyway and started (and billed) a task on its side. Nothing here
can confirm that; the $0.00 for ZO is the runner's figure, not a billing check.

## Sheets and stills — `songs\l05-urulai-w3\out\_qc\` (ZK1 only; `out\` is not committed)
- `ZK1-contact.png` — 5×2, frames 0, 33, 66, 100, 133, 166, 199, 233, 266, 299, 384 wide each
- `ZK1-every4-first2s.png` — frames 0, 4, 8, … 60 (16 frames), 4×4, 256 wide, frame number burned in
- `ZK1-every10.png` — frames 0, 10, … 290 (30 frames), 6×5, 256 wide, frame number burned in
- 100% stills (1280×720): `ZK1-f000.png`, `ZK1-f075.png`, `ZK1-f140.png`, `ZK1-f150.png`, `ZK1-f210.png`, `ZK1-f299.png` (last frame)
- `ZK1-strip.png` — the runner's own QC strip (made by the fixed `write_qc_strip`, so the fix works on ffmpeg 9)

The clip is `songs\l05-urulai-w3\out\ZK1-seed30313-w3.mp4` (7.3 MB) with its `.json` sidecar.
No ZO sheets — there is no ZO clip.

## Commit
See the last line of `LOG.md` for the hash (the report is part of that commit).
