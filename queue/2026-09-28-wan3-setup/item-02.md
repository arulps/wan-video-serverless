# item-02 — render through the Wan 3.0 API (≤ $2.10 list; ~$1.40 with the current 30% discount)

Dispatch 6e Part C:
```
python comfy\batch_runner.py --song songs\_ab7-2026-09-28-wan3 --hosts api,api,api --max-usd 1.60 --timeout-min 30 2>&1 | tee songs\_ab7-2026-09-28-wan3\batch_6e.log
```
and, only if item-01 fitted the L01 keyframe:
```
python comfy\batch_runner.py --song songs\shorts-loops --only L01_w3 --hosts api --max-usd 0.55 --timeout-min 30 2>&1 | tee songs\shorts-loops\batch_6e.log
```
- Log each submitted task id (not URLs) to `LOG.md` with the running list-price estimate.
- If the **first** task fails with an auth / region / model / quota error: **blocked** — copy the runner's
  `code: message` line into the report (it never contains the key); do not retry, do not change settings.
- If one row fails for content reasons and the others succeed, record it and continue (no retry).

**item-02.report.md:** start/end time of the run in UTC and Toronto time (for the console bill); per row: task id,
status, wall s, the sidecar `usage` block, list-price estimate; total estimate; full Windows paths of every mp4, json
and `_qc` strip.
