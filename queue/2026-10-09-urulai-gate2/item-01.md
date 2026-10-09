# item-01 — keep the gate1c ZO take, checks, render ZO + CA + I1, sheets, commit (≤ $3.00 list)

1. **Keep the old ZO take.** In `songs\l05-urulai-w3\out\` rename (not copy, not delete) `ZO-seed30313-w3.mp4/.json` →
   `ZO-seed30313-w3-v1-twobrinjal.mp4/.json`. In `out\_qc\`, rename every `ZO-*.png` to the same name with `-v1-twobrinjal` before the
   extension. In `shots.csv` the `status` cells of ZO, CA and I1 must be `todo` for the runner to render them. If any of those is not
   `todo`, set exactly that cell to `todo` and note it; this is the only edit allowed to `shots.csv`. Leave ZK1's status as it is.
2. `py tests\test_wan3_mock.py` → PASS. 3. Credentials check → True (print only True/False).
4. **Gates:** `py tests\test_prompt_lint.py` → PASS; `py comfy\prompt_lint.py --song songs\l05-urulai-w3` →
   `LINT PASS: 17 shots, 0 fail, 0 warn`. Any failure → **blocked**.
5. **Check the ZO prompt is rev 2.4:** `findstr /C:"no brinjals at all" songs\l05-urulai-w3\shots\14_ZO.raw.txt` must print one line.
   No line → **blocked**.
6. Dry-run: `py comfy\batch_runner.py --song songs\l05-urulai-w3 --only ZO,CA,I1 --hosts api --dry-run`. Expect:
   - 3 rows, all `720P 16:9 audio=off`;
   - ZO 10 s refs=10 (baby, amma, the seven `*-asleep.jpg`, set);
   - CA 8 s refs=3 (baby, amma, set);
   - I1 11 s refs=6 (Mintu, Minnu, Minmini, baby, amma, set);
   - "estimated $2.90" and no MISSING or ERROR.

   Anything else → **blocked**.
7. Render:
   ```
   py comfy\batch_runner.py --song songs\l05-urulai-w3 --only ZO,CA,I1 --hosts api --max-usd 3.00 --timeout-min 45 2>&1 | tee songs\l05-urulai-w3\batch_gate2.log
   ```
8. For each clip, write into `songs\l05-urulai-w3\out\_qc\`:
   - `<ID>-contact.png`: 5×2, 10 frames evenly spaced, 384 wide;
   - `<ID>-every4-first2s.png`: frames 0, 4, …, 60, frame number burned in, 256 wide, 4×4;
   - `<ID>-every10.png`: every 10th frame, 256 wide, frame number burned in, 6 columns, as many rows as needed;
   - 100% stills of frames 0, 75, 140, 150, 210 and the last frame (`<ID>-fNNN.png`).
9. Commit with `[skip ci]` and push:
   - `songs/l05-urulai-w3/` except `out/`;
   - `queue/2026-10-09-urulai-gate2`;
   - `queue/2026-10-09-urulai-gate1b/FABLE-VERDICT.md` and `queue/2026-10-09-urulai-gate1c/FABLE-VERDICT.md` (both untracked);
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
