# item-01 — checks and render 17 shots (≤ $8.00 list)

1. `python tests\test_wan3_mock.py` → must end with PASS.
2. Credentials check as in the Shorts queues → True.
3. **Prompt lint (gate):** `python tests\test_prompt_lint.py` → PASS, then
   `python comfy\prompt_lint.py --song songs\rowboat --only V3a,V3b,X2a,X2b,V4a,V4b,V4c,X3a,X3b,V5a,V5b,V5c,V6a,V6b,V6c,V6d,T1`
   → last line `LINT PASS` (WARN lines are fine). Any `FAIL` → **blocked** (paste the FAIL lines in the report).
4. Dry-run (no spend): `python comfy\batch_runner.py --song songs\rowboat --only V3a,V3b,X2a,X2b,V4a,V4b,V4c,X3a,X3b,V5a,V5b,V5c,V6a,V6b,V6c,V6d,T1 --hosts api --dry-run`
   → 17 rows, all `720P 16:9 audio=off`, "estimated $7.40", no MISSING/ERROR. Else → **blocked**.
5. Pack check: in `songs\rowboat\shots.csv` V3a's `ref_labels` is `Appa|Appa|Mintu|Mintu|Minnu|Minnu|Singa`, V4c's is
   `Appa|Appa|Mintu|Mintu|Minnu|Minnu`, X3a's is `Modhu|Singa|Pani Karadi`. Else → **blocked**.
6. Render:
   ```
   python comfy\batch_runner.py --song songs\rowboat --only V3a,V3b,X2a,X2b,V4a,V4b,V4c,X3a,X3b,V5a,V5b,V5c,V6a,V6b,V6c,V6d,T1 --hosts api,api,api --max-usd 8.00 --timeout-min 60 2>&1 | tee songs\rowboat\batch_w2fix_w3w4.log
   ```
**item-01.report.md:** mock + lint results; dry-run total; run window UTC + Toronto; table per shot (status, task id, wall s,
length, refs, est); failure lines verbatim.
