# item-01 — checks + first half: I1,I2,CH3,CH4,V1b,V1c,V1d,V2c,V2d,V3a,V3b,V3c,V3d,BRKb (72 s, ≤ $7.50 list)

1. (No renames: V5a is kept as rendered in gate 3 and is NOT in this queue.)
2. `python tests\test_wan3_mock.py` → PASS.  3. Credentials check (as in the Shorts queues) → True.
4. **Gates:** `python tests\test_prompt_lint.py` → PASS; `python comfy\prompt_lint.py --song songs\a07-butterfly` →
   `LINT PASS: 33 shots, 0 fail, 0 warn`; `python tests\test_song_cuts_reuse.py --plan-only` → PASS. Any failure → **blocked**.
5. Dry-run all 27: `python comfy\batch_runner.py --song songs\a07-butterfly --only I1,I2,CH3,CH4,V1b,V1c,V1d,V2c,V2d,V3a,V3b,V3c,V3d,BRKb,V4a,V4b,V4c,V4d,V5b,V5c,V5d,V6a,V6b,V6c,V6d,O3,O4 --hosts api --dry-run`
   → 27 rows, all `720P 16:9 audio=off`; I1 and O4 7 s, the rest 5 s; "estimated $13.90"; no MISSING/ERROR. Else → **blocked**.
6. Render the first half:
   ```
   python comfy\batch_runner.py --song songs\a07-butterfly --only I1,I2,CH3,CH4,V1b,V1c,V1d,V2c,V2d,V3a,V3b,V3c,V3d,BRKb --hosts api --max-usd 7.50 --timeout-min 90 2>&1 | tee songs\a07-butterfly\batch1a.log
   ```
7. For each rendered clip: `_qc\<ID>-every10.png` (every 10th frame, 256 wide, tiled 5×3; I1: 7×3) and 100% stills of the first,
   middle and last frame (`_qc\<ID>-f000.png`, `-fMID`, `-fLAST` with real numbers).
**item-01.report.md:** renames; checks; dry-run total; run window UTC + Toronto; table per clip (status, task id, wall s, length,
frames, refs, est); failure lines verbatim; sheet paths.
