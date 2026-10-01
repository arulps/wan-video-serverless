# item-01 — checks and render V1a + V1b (≤ $1.00 list)

1. `python tests\test_wan3_mock.py` → must end with PASS.
2. Credentials check as in the Shorts queues → True.
3. Dry-run (no spend): `python comfy\batch_runner.py --song songs\rowboat --only V1a,V1b --hosts api --dry-run`
   → 2 rows, both `720P 16:9 audio=off`, "estimated $0.90", no MISSING/ERROR. Else → **blocked**.
4. Check the prompts carry the new seating: `findstr /c:"two low wooden benches face each other" songs\rowboat\shots\03_V1a.raw.txt songs\rowboat\shots\04_V1b.raw.txt`
   → both files listed; `findstr /c:"side by side" songs\rowboat\shots\*.raw.txt` → no output. Else → **blocked**.
5. Render:
   ```
   python comfy\batch_runner.py --song songs\rowboat --only V1a,V1b --hosts api,api --max-usd 1.00 --timeout-min 30 2>&1 | tee songs\rowboat\batch_gate2.log
   ```
**item-01.report.md:** mock result; dry-run total; run window UTC + Toronto; per shot task id, wall s, est; failure lines verbatim.
