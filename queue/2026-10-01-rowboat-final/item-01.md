# item-01 — checks and render T1 + V5c (≤ $1.00 list)

1. `python tests\test_wan3_mock.py` → PASS.  2. Credentials check → True.
3. **Prompt lint (gate):** `python tests\test_prompt_lint.py` → PASS, then
   `python comfy\prompt_lint.py --song songs\rowboat --only T1,V5c` → last line `LINT PASS`. Any `FAIL` → **blocked**.
4. Dry-run: `python comfy\batch_runner.py --song songs\rowboat --only T1,V5c --hosts api --dry-run`
   → 2 rows, `720P 16:9 audio=off`, "estimated $0.70", no MISSING/ERROR. Else → **blocked**.
5. Pack check: T1's and V5c's `ref_labels` in `songs\rowboat\shots.csv` are both `Appa|Appa|Mintu|Mintu|Minnu|Minnu`. Else → **blocked**.
6. Render:
   ```
   python comfy\batch_runner.py --song songs\rowboat --only T1,V5c --hosts api,api --max-usd 1.00 --timeout-min 30 2>&1 | tee songs\rowboat\batch_final.log
   ```
**item-01.report.md:** lint + dry-run results; run window UTC + Toronto; per shot status, task id, wall s, length, refs, est.
