# item-01 — check and render (≤ $3.20 list)

1. `python -c "import sys; sys.path.insert(0,'comfy'); import wan3_api; print('credentials present:', wan3_api.credentials_present())"` → True.
2. Dry-runs (no spend):
   - `python comfy\batch_runner.py --song songs\shorts-learning --hosts api --dry-run --only C1_w3,F3_w3,FD1_w3,AC2_w3,V2_w3`
     → 5 rows, `audio=on`, 720P 9:16 5 s, C1/F3/V2 refs=0, FD1/AC2 refs=1, "estimated $2.50".
   - `python comfy\batch_runner.py --song songs\shorts-loops --hosts api --dry-run --only L04_w3d` → 1 row, "estimated $0.50".
   Any MISSING/ERROR/other total → **blocked**.
3. Render:
   ```
   python comfy\batch_runner.py --song songs\shorts-learning --only C1_w3,F3_w3,FD1_w3,AC2_w3,V2_w3 --hosts api,api,api --max-usd 2.60 --timeout-min 30 2>&1 | tee songs\shorts-learning\batch_pilot.log
   python comfy\batch_runner.py --song songs\shorts-loops --only L04_w3d --hosts api --max-usd 0.60 --timeout-min 30 2>&1 | tee songs\shorts-loops\batch_retakes3.log
   ```
**item-01.report.md:** credentials; dry-run totals; run windows UTC + Toronto; table of the 6 rows (status, task id, wall s, est); failures verbatim.
