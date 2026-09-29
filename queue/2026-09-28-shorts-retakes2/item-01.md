# item-01 — check and render L04_w3c (≤ $0.60 list)

1. `python -c "import sys; sys.path.insert(0,'comfy'); import wan3_api; print('credentials present:', wan3_api.credentials_present())"` → True.
2. Dry-run: `python comfy\batch_runner.py --song songs\shorts-loops --hosts api --dry-run --only L04_w3c`
   → 1 row, `audio=on`, 5 s, seed 4242, no MISSING/ERROR, "estimated $0.50". Anything else → **blocked**.
3. Render:
   ```
   python comfy\batch_runner.py --song songs\shorts-loops --only L04_w3c --hosts api --max-usd 0.60 --timeout-min 30 2>&1 | tee songs\shorts-loops\batch_retakes2.log
   ```
**item-01.report.md:** credentials True; dry-run total; run window UTC + Toronto; status, task id, wall s, estimate; failure lines verbatim.
