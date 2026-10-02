# item-01 — checks, render RA, sheet, commit (≤ $0.90 list)

1. `python tests\test_wan3_mock.py` → PASS.  2. Credentials check (as in the Shorts queues) → True.
3. **Prompt lint (gate):** `python tests\test_prompt_lint.py` → PASS, then
   `python comfy\prompt_lint.py --song songs\a07-butterfly` → last line `LINT PASS: 33 shots, 0 fail, 0 warn`. Any `FAIL` → **blocked**.
4. `python tests\test_song_cuts_reuse.py --plan-only` → PASS. Else → **blocked**.
5. Dry-run all 33 (no spend): `python comfy\batch_runner.py --song songs\a07-butterfly --hosts api --dry-run`
   → 33 rows, all `720P 16:9 audio=off`, RA = 8 s with refs=6 (`Mintu, Minnu, Leo, Priya, Amma, Mrs Meena`), max refs 8 on any row,
   "estimated $17.50", no MISSING/ERROR. Else → **blocked**.
6. Render the gate clip only:
   ```
   python comfy\batch_runner.py --song songs\a07-butterfly --only RA --hosts api --max-usd 0.90 --timeout-min 30 2>&1 | tee songs\a07-butterfly\batch_gate1.log
   ```
7. Contact sheet `songs\a07-butterfly\out\_qc\RA-contact.png` (5×2, 10 frames evenly spaced, 384 wide) + 100% stills of frames
   0, 60, 120, 180, 239 (`_qc\RA-f000.png` etc.).
8. Commit with `[skip ci]` and push: `comfy/song_cuts.py`, `tests/test_song_cuts_reuse.py`, `songs/a07-butterfly/` (everything
   except `out/`), `queue/2026-10-02-butterfly-gate1`. **Do not judge the clip.**
**item-01.report.md:** mock, lint, plan test, dry-run total + RA row; run window UTC + Toronto; task id, wall s, length, frames,
refs, est; failure lines verbatim; sheet/still paths.
