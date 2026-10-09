# item-01 — keep the gate2 ZO take, checks, render K3 + ZK2 + ZK4 + ZK7 + ZO + I1, sheets, commit (≤ $5.80 list)

1. **Keep the old ZO and I1 takes.** In `songs\l05-urulai-w3\out\` rename (not copy, not delete) `ZO-seed30313-w3.mp4/.json` →
   `ZO-seed30313-w3-v1b-twocabbage.mp4/.json`. In `out\_qc\`, rename every `ZO-*.png` that has no `-v1` in its name to the same name
   with `-v1b-twocabbage` before the extension. Do the same for I1: `I1-seed30313-w3.mp4/.json` and every `I1-*.png` → `-v1-onshelf`
   before the extension. In `shots.csv` the `status` cells of K3, ZK2, ZK4, ZK7, ZO and I1 must be `todo`. If any
   is not `todo`, set exactly that cell to `todo` and note it; this is the only edit allowed to `shots.csv`.
2. `py tests\test_wan3_mock.py` → PASS. 3. Credentials check → True (print only True/False).
4. **Gates:** `py tests\test_prompt_lint.py` → PASS; `py comfy\prompt_lint.py --song songs\l05-urulai-w3` →
   `LINT PASS: 17 shots, 0 fail, 0 warn`. Any failure → **blocked**.
5. **Check the ZO prompt is rev 2.5:** `songs\l05-urulai-w3\shots\14_ZO.raw.txt` must contain the text "no cabbage in the back row"
   exactly once, and `shots\01_I1.raw.txt` must contain "never stand, sit or climb on the shelf" exactly once.
   If not → **blocked**.
6. Dry-run: `py comfy\batch_runner.py --song songs\l05-urulai-w3 --only K3,ZK2,ZK4,ZK7,ZO,I1 --hosts api --dry-run`. Expect:
   - 6 rows, all `720P 16:9 audio=off`;
   - ZK2, ZK4 and ZK7: 10 s, refs=3 each (baby, `13-okra-asleep` / `15-carrot-asleep` / `18-beans-asleep`, set);
   - K3: 6 s, refs=3 (baby, `14-tomato-asleep`, set);
   - ZO: 10 s, refs=10;
   - I1: 11 s, refs=6 (Mintu, Minnu, Minmini, baby, amma, set);
   - "estimated $5.70" and no MISSING or ERROR.

   Anything else → **blocked**.
7. Render:
   ```
   py comfy\batch_runner.py --song songs\l05-urulai-w3 --only K3,ZK2,ZK4,ZK7,ZO,I1 --hosts api --max-usd 5.80 --timeout-min 70 2>&1 | tee songs\l05-urulai-w3\batch_gate3.log
   ```
8. For each clip, write into `songs\l05-urulai-w3\out\_qc\`:
   - `<ID>-contact.png`: 5×2, 10 frames evenly spaced, 384 wide;
   - `<ID>-every4-first2s.png`: frames 0, 4, …, 60, frame number burned in, 256 wide, 4×4;
   - `<ID>-every10.png`: every 10th frame, 256 wide, frame number burned in, 6 columns;
   - 100% stills of frames 0, 75, 140, 150, 210 and the last frame (`<ID>-fNNN.png`).
9. Commit with `[skip ci]` and push:
   - `songs/l05-urulai-w3/` except `out/`;
   - `queue/2026-10-09-urulai-gate3`;
   - `queue/2026-10-09-urulai-gate2/FABLE-VERDICT.md`;
   - `queue/L05-WATCH-LOG.md`.

   **Do not judge the clips.**

**item-01.report.md** must cover:
- renames;
- any status cells reset;
- checks;
- dry-run rows and total;
- run window in UTC and Toronto time;
- per clip: task id, wall s, length, frames, refs, est;
- failure lines verbatim;
- sheet and still paths;
- commit hash.
