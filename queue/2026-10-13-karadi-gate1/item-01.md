# item-01 — checks, render CAa + CQa, sheets, commit (≤ $1.70 list)

0. **Prerequisite.** `queue\2026-10-13-karadi-1-scale-rule\item-01.done` must exist (second re-issue of the blocked
   `2026-10-10-scale-rule`) (the scale-rule code — `comfy\scale_line.py`,
   `comfy\character_scale.json`, lint R9/R10 — is committed by that queue; the watcher runs it first). If it is missing → **blocked**
   ("run queue\2026-10-13-karadi-1-scale-rule first"), $0.00 spent.
1. **Rev 1.2 is in place** (Fable wrote the files on 13 Oct; verify, don't edit): in `songs\a12-karadi-w3\shots.csv` the `duration_s`
   of `CQa, CQb, CAa, CAb, HKa, HKb` is `8` and of every other row `6` or `7`; `shots\09_V1A.raw.txt` contains
   "the basket never leaves his left paw"; 18 rows, 18 `shots\NN_ID.raw.txt`, 10 files in `refs\send\`. Any mismatch → **blocked**.
2. `py tests\test_wan3_mock.py` → PASS.  3. Credentials check (as in the Shorts queues) → True (print only True/False).
4. **Gates:** `py tests\test_prompt_lint.py` → PASS; `py comfy\prompt_lint.py --song songs\a12-karadi-w3` →
   `LINT PASS: 18 shots, 0 fail, 0 warn`. Any failure → **blocked**.
5. Dry-run: `py comfy\batch_runner.py --song songs\a12-karadi-w3 --only CAa,CQa --hosts api --dry-run`
   → 2 rows, `720P 16:9 audio=off`; CAa 8 s refs=2 (`refs/send/03-karadi-mama.jpg`, `10-forest-picnic-set.jpg`); CQa 8 s refs=8
   (`01-mintu-front`, `02-minnu-front`, `04-rabbit`, `05-squirrel`, `06-amma-front`, `07-appa-face`, `08-appa-body`,
   `10-forest-picnic-set`); "estimated $1.60"; no MISSING/ERROR/OVER BUDGET/refused/Traceback. Report the total bytes of CQa's 8 ref
   files (expect ≈ 1.5 MB). Else → **blocked**.
6. Render:
   ```
   py comfy\batch_runner.py --song songs\a12-karadi-w3 --only CAa,CQa --hosts api --max-usd 1.70 --timeout-min 40 2>&1 | tee songs\a12-karadi-w3\batch_gate1.log
   ```
7. For each clip into `songs\a12-karadi-w3\out\_qc\` (8 s = 240 frames at 30 fps):
   - `<ID>-contact.png` — 5×2, 10 frames evenly spaced, 384 wide;
   - `<ID>-every4-first2s.png` — frames 0, 4, 8, … 60, frame number burned in, 256 wide, 4×4;
   - `<ID>-every4-all.png` — frames 0, 4, 8, … 236 (60 frames), frame number burned in, 192 wide, 10×6 (the spin and the dance
     need every 4th frame through the whole clip, not just the opening);
   - 100 % stills (1280×720) of frames 0, 30, 60, 120, 180 and 239 (`<ID>-fNNN.png`).
8. Commit with `[skip ci]` and push: `songs/a12-karadi-w3/` except `out/` (`git add -f songs/a12-karadi-w3/refs` — `refs/` is
   git-ignored by pattern), `queue/2026-10-13-karadi-gate1`, `queue/A12-WATCH.md`, `queue/L05-DONE`, `queue/L05-WATCH-LOG.md`.
   `git add` by explicit path only. **Do not judge the clips.**

**item-01.report.md:** prerequisite + rev 1.2 checks; checks 2–4 output lines; dry-run rows + total + CQa ref bytes; run window UTC +
Toronto; per clip: task id, wall s, length, frames (ffprobe `-count_frames`), refs, est; failure lines verbatim; sheet/still paths;
commit hash.
