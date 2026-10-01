# item-01 — checks and render 9 shots (≤ $4.00 list)

1. `python tests\test_wan3_mock.py` → must end with PASS.
2. Credentials check as in the Shorts queues → True.
2b. **Prompt lint (gate):** `python tests\test_prompt_lint.py` → PASS, then
    `python comfy\prompt_lint.py --song songs\rowboat --only V1b,V2a,V2b,V2c,V2d,X1b,V3a,V3b,V3c`
    → last line `LINT PASS` (WARN lines are fine). Any `FAIL` → **blocked** (paste the FAIL lines in the report).
3. Dry-run (no spend): `python comfy\batch_runner.py --song songs\rowboat --only V1b,V2a,V2b,V2c,V2d,X1b,V3a,V3b,V3c --hosts api --dry-run`
   → 9 rows, all `720P 16:9 audio=off`, "estimated $3.50", no MISSING/ERROR. Else → **blocked**.
4. Pack check: in `songs\rowboat\shots.csv` the `ref_labels` of V1b, V2a, V2b, V2d, V3a, V3c are
   `Appa|Appa|Mintu|Mintu|Minnu|Minnu` and V2c's is `Appa|Appa|Mintu|Mintu|Minnu|Minnu|Modhu`. Else → **blocked**.
5. Render:
   ```
   python comfy\batch_runner.py --song songs\rowboat --only V1b,V2a,V2b,V2c,V2d,X1b,V3a,V3b,V3c --hosts api,api,api --max-usd 4.00 --timeout-min 40 2>&1 | tee songs\rowboat\batch_w1fix_w2.log
   ```
**item-01.report.md:** mock result; dry-run total; run window UTC + Toronto; table per shot (status, task id, wall s, length,
refs, est); failure lines verbatim.
