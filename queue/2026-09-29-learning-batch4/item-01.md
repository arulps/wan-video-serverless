# item-01 — check and render 5 rows (≤ $3.00 list)

1. Credentials check as in the pilot → True.
2. Dry-run: `python comfy\batch_runner.py --song songs\shorts-learning --hosts api --dry-run --only SN1_w3c,SN2_w3c,SN3_w3c,SN6_w3c,A6_w3c`
   → 5 rows, all `audio=on`; SN rows refs=1, A6_w3c refs=0 with first= and last= the keyframe; "estimated $2.50"; no MISSING/ERROR.
   Else → **blocked**.
3. Render, 3 in parallel:
   ```
   python comfy\batch_runner.py --song songs\shorts-learning --only SN1_w3c,SN2_w3c,SN3_w3c,SN6_w3c,A6_w3c --hosts api,api,api --max-usd 3.00 --timeout-min 30 2>&1 | tee songs\shorts-learning\batch_learning4.log
   ```
**item-01.report.md:** dry-run total; run window UTC + Toronto; table of the 5 rows (status, task id, wall s, est); failures verbatim.
