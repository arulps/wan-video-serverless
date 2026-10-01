# item-01 — checks and render world 1 (≤ $5.00 list)

1. `python tests\test_wan3_mock.py` → must end with PASS.
2. Credentials check as in the Shorts queues → True.
3. Dry-run (no spend):
   `python comfy\batch_runner.py --song songs\rowboat --only I1,I2,V1b,V1c,V2a,V2b,V2c,V2d,X1a,X1b --hosts api --dry-run`
   → 10 rows, all `720P 16:9 audio=off`, "estimated $4.50", no MISSING/ERROR. Else → **blocked**.
4. Seating check: `findstr /c:"on the low wooden bench at the other end of the boat" songs\rowboat\shots\04_V1b.raw.txt`
   → listed; `findstr /m /c:"face to face" songs\rowboat\shots\*.raw.txt` → no output. Else → **blocked**.
5. Render:
   ```
   python comfy\batch_runner.py --song songs\rowboat --only I1,I2,V1b,V1c,V2a,V2b,V2c,V2d,X1a,X1b --hosts api,api,api --max-usd 5.00 --timeout-min 40 2>&1 | tee songs\rowboat\batch_w1.log
   ```
**item-01.report.md:** mock result; dry-run total; run window UTC + Toronto; table per shot (status, task id, wall s, length,
est); failure lines verbatim.
