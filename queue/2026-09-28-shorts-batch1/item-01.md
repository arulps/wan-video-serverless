# item-01 — check and render the 19 Shorts (≤ $10.50 list)

1. `python -c "import sys; sys.path.insert(0,'comfy'); import wan3_api; print('credentials present:', wan3_api.credentials_present())"` → must be True.
2. Dry-run (no spend): `python comfy\batch_runner.py --song songs\shorts-loops --hosts api --dry-run --only L02_w3,L03_w3,L04_w3,L05_w3,L06_w3,L07_w3,L08_w3,L09_w3,L10_w3,L11_w3,L12_w3,L13_w3,L14_w3,L15_w3,L16_w3,L17_w3,L18_w3,L19_w3,L20_w3`
   → 19 rows, all `audio=on`, no MISSING/ERROR, total "estimated $9.70". Anything else → **blocked**.
3. Render, 3 tasks in parallel:
   ```
   python comfy\batch_runner.py --song songs\shorts-loops --only L02_w3,L03_w3,L04_w3,L05_w3,L06_w3,L07_w3,L08_w3,L09_w3,L10_w3,L11_w3,L12_w3,L13_w3,L14_w3,L15_w3,L16_w3,L17_w3,L18_w3,L19_w3,L20_w3 --hosts api,api,api --max-usd 10.50 --timeout-min 30 2>&1 | tee songs\shorts-loops\batch_shorts1.log
   ```
   If the first tasks fail on auth/region/model/quota: stop (Ctrl-C), **blocked**, copy the `code: message` line. A row that
   fails on content (e.g. moderation) is recorded and skipped — no retry.

**item-01.report.md:** credentials True; dry-run total; run window UTC + Toronto; a table of all 19 rows: status, task id,
wall s, list estimate; total estimate; any failure lines verbatim.
