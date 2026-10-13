# item-01 — checks, render the 13 remaining clips, sheets, commit (≤ $9.00 list)

IDs: `I1,HKa,HKb,CQb,CAb,V1Q,V1A,V2Q,V2A,V3A,V4Q,O1,O2`

0. **Prerequisite.** `queue\2026-10-13-karadi-gate2\item-01.done` and `queue\2026-10-13-karadi-gate2\FABLE-VERDICT.md` must exist.
   Otherwise → **blocked**, $0.00 spent.
1. **Rev 1.4 is in place** (Fable wrote the files; verify, don't edit):
   - `shots\11_V2A.raw.txt` starts with "Image 1 is Mintu, Image 2 is Karadi Mama";
   - V2A's `shots.csv` row has cast `Mintu+Karadi-Mama`, status `todo` and 3 refs;
   - CAa, CQa, V3Q, V4A and O3 have status `done`.

   Any mismatch → **blocked**.
2. `py tests\test_wan3_mock.py` → PASS.  3. Credentials check → True (print only True/False).
4. **Gates:** `py tests\test_prompt_lint.py` → PASS; `py comfy\prompt_lint.py --song songs\a12-karadi-w3` →
   `LINT PASS: 18 shots, 0 fail, 0 warn`. Any failure → **blocked**.
5. Dry-run: `py comfy\batch_runner.py --song songs\a12-karadi-w3 --only <IDs> --hosts api --dry-run`. It must show:
   - 13 rows, all `720P 16:9 audio=off`, with "estimated $8.90";
   - durations: I1, O1 and O2 7 s; HKa, HKb, CQb and CAb 8 s; the six verse rows 6 s;
   - no `ERROR`, `unknown cast`, `MISSING`, `OVER BUDGET`, `refused` or `Traceback`.

   Otherwise → **blocked**.
6. Render:
   ```
   py comfy\batch_runner.py --song songs\a12-karadi-w3 --only I1,HKa,HKb,CQb,CAb,V1Q,V1A,V2Q,V2A,V3A,V4Q,O1,O2 --hosts api --max-usd 9.00 --timeout-min 50 2>&1 | tee songs\a12-karadi-w3\batch_batch1.log
   ```
7. For each rendered clip, write into `songs\a12-karadi-w3\out\_qc\`:
   - `<ID>-contact.png`;
   - `<ID>-every4-all.png` (every 4th frame, frame number burned in, 192 wide, 10 per row);
   - 100 % stills of frames 0, 30, 60, 90, 120, 150 and the last frame.

   Same tools as gate 2.
8. Commit with `[skip ci]` and push:
   - `songs/a12-karadi-w3/` except `out/`;
   - `queue/2026-10-13-karadi-gate2/FABLE-VERDICT.md`;
   - `queue/2026-10-13-karadi-batch1`;
   - `queue/A12-WATCH-LOG.md`.

   `git add` by explicit path only. **Do not judge the clips.**

**item-01.report.md** must cover:
- the prerequisite and the rev 1.4 checks;
- the check output lines;
- the dry-run rows and total;
- the run window, UTC and Toronto;
- a table with one row per clip: task id, status, wall s, length, frames (ffprobe `-count_frames`), est;
- every failure line verbatim;
- the runner's final estimate;
- the commit hash.
