# item-01 — keep the gate1b take, checks, render ZK1 + ZO, sheets, commit (≤ $2.10 list)

1. **Keep the old take.** In `songs\l05-urulai-w3\out\` rename (not copy, not delete) `ZK1-seed30313-w3.mp4/.json` →
   `ZK1-seed30313-w3-v1-awake.mp4/.json`; in `out\_qc\` every `ZK1-*.png` / `ZK1-*.jpg` and `FABLE-ZK1-*` → same name with `-v1-awake`
   before the extension. In `shots.csv` the `status` cells of ZK1 (`done`) and ZO (`failed`) must be `todo` for the runner to render
   them: if they are not `todo`, set exactly those two cells to `todo` (the only edit allowed to `shots.csv`) and note it.
2. `py tests\test_wan3_mock.py` → PASS. 3. Credentials check → True (print only True/False).
4. **Gates:** `py tests\test_prompt_lint.py` → PASS; `py comfy\prompt_lint.py --song songs\l05-urulai-w3` →
   `LINT PASS: 17 shots, 0 fail, 0 warn`. Any failure → **blocked**.
5. Dry-run: `py comfy\batch_runner.py --song songs\l05-urulai-w3 --only ZK1,ZO --hosts api --dry-run`
   → 2 rows, `720P 16:9 audio=off`; ZK1 10 s refs=3 (`refs/send/10-baby-potato.jpg`, `12-brinjal-asleep.jpg`,
   `20-kitchen-shelf-set.jpg`); ZO 10 s refs=10 (baby, amma, and the seven `*-asleep.jpg`, set); "estimated $2.00";
   no MISSING/ERROR. Report the total size of the 10 ZO ref files (expect ≈ 2 MB). Else → **blocked**.
6. Render:
   ```
   py comfy\batch_runner.py --song songs\l05-urulai-w3 --only ZK1,ZO --hosts api --max-usd 2.10 --timeout-min 40 2>&1 | tee songs\l05-urulai-w3\batch_gate1c.log
   ```
7. For each clip into `songs\l05-urulai-w3\out\_qc\`: `<ID>-contact.png` (5×2, 10 frames evenly spaced, 384 wide),
   `<ID>-every4-first2s.png` (frames 0,4,…,60, frame number burned in, 256 wide, 4×4), `<ID>-every10.png` (every 10th frame, 256 wide,
   6×5, frame number burned in), and 100% stills of frames 0, 75, 140, 150, 210 and the last frame (`<ID>-fNNN.png`).
8. Commit with `[skip ci]` and push: `songs/l05-urulai-w3/` except `out/` (`git add -f songs/l05-urulai-w3/refs` — `refs/` is
   git-ignored by pattern), `queue/2026-10-09-urulai-gate1c`, `queue/L05-WATCH-LOG.md`. **Do not judge the clips.**

**item-01.report.md:** renames; any status cells reset; checks; dry-run rows + total + ZO ref bytes; run window UTC + Toronto; per clip:
task id, wall s, length, frames, refs, est; failure lines verbatim; sheet/still paths; commit hash.
