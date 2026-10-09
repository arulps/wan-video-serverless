# item-01 — checks, render ZK1 + ZO, sheets, commit (≤ $2.10 list)

1. `git diff --stat comfy\batch_runner.py` → only `write_qc_strip` changed (the `-vsync` removal, 3 lines). Anything else → **blocked**.
2. `py tests\test_wan3_mock.py` → PASS (must now pass on Beast's ffmpeg 9). FAIL → **blocked** (report the lines verbatim).
3. Credentials check (as in the Shorts queues) → True (print only True/False).
4. **Gates:** `py tests\test_prompt_lint.py` → PASS; `py comfy\prompt_lint.py --song songs\l05-urulai-w3` →
   `LINT PASS: 17 shots, 0 fail, 0 warn`. Any failure → **blocked**.
5. Dry-run: `py comfy\batch_runner.py --song songs\l05-urulai-w3 --only ZK1,ZO --hosts api --dry-run`
   → 2 rows, `720P 16:9 audio=off`; ZK1 10 s refs=3 (Baby Potato, Brinjal, the kitchen shelf set); ZO 10 s refs=10 (Baby Potato,
   Amma Potato, Brinjal, Okra, Tomato, Carrot, Radish, Cabbage, Beans, the kitchen shelf set); "estimated $2.00"; no MISSING/ERROR.
   Else → **blocked**.
6. Render:
   ```
   py comfy\batch_runner.py --song songs\l05-urulai-w3 --only ZK1,ZO --hosts api --max-usd 2.10 --timeout-min 40 2>&1 | tee songs\l05-urulai-w3\batch_gate1.log
   ```
7. For each clip into `songs\l05-urulai-w3\out\_qc\`: `<ID>-contact.png` (5×2, 10 frames evenly spaced, 384 wide),
   `<ID>-every4-first2s.png` (frames 0,4,8,…,60 with the frame number burned in, 256 wide, tiled 4×4),
   `<ID>-every10.png` (every 10th frame, 256 wide, tiled 6×5, frame number burned in), and 100% stills of frames 0, 75, 140, 150,
   210 and the last frame (`<ID>-fNNN.png`).
8. Commit with `[skip ci]` and push: `comfy/batch_runner.py`, `songs/l05-urulai-w3/` (everything except `out/`; `refs/` is matched by a
   `.gitignore` line, so add it with `git add -f songs/l05-urulai-w3/refs`), `queue/2026-10-09-urulai-gate1`, `queue/2026-10-09-urulai-gate1b`,
   `queue/L05-WATCH.md`, `queue/L05-WATCH-LOG.md`. **Do not judge the clips.**

**item-01.report.md:** checks; dry-run rows + total; run window UTC + Toronto; per clip: task id, wall s, length, frames, refs, est;
failure lines verbatim; sheet/still paths; commit hash.
