# item-01 — check and render 9 rows (≤ $5.00 list)

1. Credentials check as in the pilot → True.
2. Dry-run: `python comfy\batch_runner.py --song songs\shorts-learning --hosts api --dry-run --only A1_w3,A2_w3,A3_w3,A4_w3,A5_w3,A6_w3,MN1_w3b,MN3_w3b,VG3_w3b`
   → 9 rows, all `audio=on`, A1–A6 refs=0, retakes refs=1, "estimated $4.50", no MISSING/ERROR. Else → **blocked**.
3. Render, 3 in parallel:
   ```
   python comfy\batch_runner.py --song songs\shorts-learning --only A1_w3,A2_w3,A3_w3,A4_w3,A5_w3,A6_w3,MN1_w3b,MN3_w3b,VG3_w3b --hosts api,api,api --max-usd 5.00 --timeout-min 30 2>&1 | tee songs\shorts-learning\batch_learning2.log
   ```
**item-01.report.md:** dry-run total; run window UTC + Toronto; table of the 9 rows (status, task id, wall s, est); failures verbatim.
