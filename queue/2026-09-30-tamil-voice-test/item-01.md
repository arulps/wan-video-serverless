# item-01 — check and render 2 rows (≤ $1.20 list)

1. Credentials check as in the pilot → True.
2. Dry-run: `python comfy\batch_runner.py --song songs\shorts-learning --hosts api --dry-run --only C1_w3ta,C1_w3tr`
   → 2 rows, `audio=on`, refs=1 (Minnu), "estimated $1.00", no MISSING/ERROR. Else → **blocked**.
3. Render, 2 in parallel:
   ```
   python comfy\batch_runner.py --song songs\shorts-learning --only C1_w3ta,C1_w3tr --hosts api,api --max-usd 1.20 --timeout-min 30 2>&1 | tee songs\shorts-learning\batch_tamil_test.log
   ```
**item-01.report.md:** dry-run total; run window UTC + Toronto; status, task id, wall s, est per row; failures verbatim.
