# item-01 — checks and render V1a (≤ $0.70 list)

1. `python tests\test_wan3_mock.py` → must end with PASS.
2. Credentials check as in the Shorts queues → True.
3. Dry-run all 29 (no spend): `python comfy\batch_runner.py --song songs\rowboat --hosts api --dry-run`
   → 29 rows, all `720P 16:9 audio=off`, "estimated $12.90", no MISSING/ERROR. Else → **blocked**.
4. Render the gate shot only:
   ```
   python comfy\batch_runner.py --song songs\rowboat --only V1a --hosts api --max-usd 0.70 --timeout-min 30 2>&1 | tee songs\rowboat\batch_gate.log
   ```
**item-01.report.md:** mock result; dry-run total; run window UTC + Toronto; task id, wall s, est; failure lines verbatim.
