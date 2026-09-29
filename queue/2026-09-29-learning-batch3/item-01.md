# item-01 — check and render 7 rows (≤ $4.00 list)

1. Credentials check as in the pilot → True.
2. Dry-run: `python comfy\batch_runner.py --song songs\shorts-learning --hosts api --dry-run --only SN1_w3b,SN2_w3b,SN3_w3b,SN4_w3b,SN6_w3b,A3_w3b,A6_w3b`
   → 7 rows, all `audio=on`, refs=0, "estimated $3.50", no MISSING/ERROR. Else → **blocked**.
3. Render, 3 in parallel:
   ```
   python comfy\batch_runner.py --song songs\shorts-learning --only SN1_w3b,SN2_w3b,SN3_w3b,SN4_w3b,SN6_w3b,A3_w3b,A6_w3b --hosts api,api,api --max-usd 4.00 --timeout-min 30 2>&1 | tee songs\shorts-learning\batch_learning3.log
   ```
**item-01.report.md:** dry-run total; run window UTC + Toronto; table of the 7 rows (status, task id, wall s, est); failures verbatim.
