# item-01 — SA/SB to 7 s, checks, render the last nine clips, sheets, commit (≤ $5.90 list)

1. **`shots.csv` cells.**
   - Set the `duration_s` cell of row **SA** to `7` and of row **SB** to `7`; both are `8` now.
   - The `status` cells of Z3, Z5, Z6, K5, K6, SA, SB, CB and O2 must be `todo`. If any is not, set exactly that cell to `todo`.
   - Report every cell you changed (expect exactly the two duration cells). Change nothing else in `shots.csv`.
2. `py tests\test_wan3_mock.py` → PASS. 3. Credentials check → True (print only True/False).
4. **Gates:** `py tests\test_prompt_lint.py` → PASS; `py comfy\prompt_lint.py --song songs\l05-urulai-w3` →
   `LINT PASS: 17 shots, 0 fail, 0 warn`. Any failure → **blocked**.
5. **Prompt check:** `songs\l05-urulai-w3\shots\17_O2.raw.txt` must contain "standing on the kitchen floor in front of the rack"
   exactly once. If not → **blocked**.
6. Dry-run: `py comfy\batch_runner.py --song songs\l05-urulai-w3 --only Z3,Z5,Z6,K5,K6,SA,SB,CB,O2 --hosts api --dry-run`. Expect:
   - 9 rows, all `720P 16:9 audio=off`;
   - Z3, Z5, Z6, K5, K6: 6 s, refs=3 each (baby, the owner's `*-asleep.jpg`, set);
   - SA and SB: **7 s**, refs=2 (amma, set);
   - CB: 8 s, refs=3 (baby, amma, set);
   - O2: 6 s, refs=4 (Mintu, Minnu, Minmini, set);
   - "estimated $5.80" and no MISSING or ERROR.

   Anything else → **blocked**.
7. Render:
   ```
   py comfy\batch_runner.py --song songs\l05-urulai-w3 --only Z3,Z5,Z6,K5,K6,SA,SB,CB,O2 --hosts api --max-usd 5.90 --timeout-min 80 2>&1 | tee songs\l05-urulai-w3\batch_gate4.log
   ```
8. For each clip, write into `songs\l05-urulai-w3\out\_qc\`:
   - `<ID>-contact.png`: 5×2, 10 frames evenly spaced, 384 wide;
   - `<ID>-every4-first2s.png`: frames 0, 4, …, 60, frame number burned in, 256 wide, 4×4;
   - `<ID>-every10.png`: every 10th frame, 256 wide, frame number burned in, 6 columns;
   - 100% stills of frames 0, 75, 140 and the last frame (`<ID>-fNNN.png`), plus 150 and 210 where the clip has them.
9. Commit with `[skip ci]` and push:
   - `songs/l05-urulai-w3/` except `out/`;
   - `queue/2026-10-09-urulai-gate4`;
   - `queue/2026-10-09-urulai-gate3/FABLE-VERDICT.md`;
   - `queue/L05-WATCH.md`;
   - `queue/L05-WATCH-LOG.md`.

   **Do not judge the clips.**

**item-01.report.md** must cover:
- `shots.csv` cells changed;
- checks;
- dry-run rows and total;
- run window in UTC and Toronto time;
- per clip: task id, wall s, length, frames, refs, est;
- failure lines verbatim;
- sheet and still paths;
- commit hash.
