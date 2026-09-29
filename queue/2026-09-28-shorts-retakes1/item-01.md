# item-01 — check and render the 3 retakes (≤ $1.80 list)

1. `python -c "import sys; sys.path.insert(0,'comfy'); import wan3_api; print('credentials present:', wan3_api.credentials_present())"` → must be True.
2. Dry-run (no spend): `python comfy\batch_runner.py --song songs\shorts-loops --hosts api --dry-run --only L03_w3b,L04_w3b,L10_w3b`
   → 3 rows, all `audio=on`, L03_w3b 6 s seed 4242, L04_w3b and L10_w3b 5 s seed 30313, no MISSING/ERROR,
   total "estimated $1.60". Anything else → **blocked**.
3. Render, 3 tasks in parallel:
   ```
   python comfy\batch_runner.py --song songs\shorts-loops --only L03_w3b,L04_w3b,L10_w3b --hosts api,api,api --max-usd 1.80 --timeout-min 30 2>&1 | tee songs\shorts-loops\batch_retakes1.log
   ```
   Auth/region/model/quota failure → stop, **blocked**, copy the `code: message` line. A content failure (e.g. moderation)
   is recorded and skipped — no retry.

**item-01.report.md:** credentials True; dry-run total; run window UTC + Toronto; table of the 3 rows: status, task id,
wall s, length, list estimate; total; any failure lines verbatim.
