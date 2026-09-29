# item-01 — check and render A6_w3d (≤ $0.60 list)

1. Credentials check as in the pilot → True.
2. Dry-run: `python comfy\batch_runner.py --song songs\shorts-learning --hosts api --dry-run --only A6_w3d`
   → 1 row, `audio=on`, refs=0, first= and last= the keyframe, "estimated $0.50", no MISSING/ERROR. Else → **blocked**.
3. Render:
   ```
   python comfy\batch_runner.py --song songs\shorts-learning --only A6_w3d --hosts api --max-usd 0.60 --timeout-min 30 2>&1 | tee songs\shorts-learning\batch_learning5.log
   ```
**item-01.report.md:** dry-run total; run window UTC + Toronto; status, task id, wall s, est; failures verbatim.
