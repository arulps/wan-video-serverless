# item-01 — render V5c, sheet, commit (≤ $0.50 list)

1. `python tests\test_wan3_mock.py` → PASS.  2. Credentials check → True.
3. **Prompt lint (gate):** `python tests\test_prompt_lint.py` → PASS, then
   `python comfy\prompt_lint.py --song songs\rowboat --only V5c` → last line `LINT PASS`. Any `FAIL` → **blocked**.
4. Dry-run: `python comfy\batch_runner.py --song songs\rowboat --only V5c --hosts api --dry-run` → 1 row, `720P 16:9 audio=off`,
   "estimated $0.40", no MISSING/ERROR. Else → **blocked**.
5. Render: `python comfy\batch_runner.py --song songs\rowboat --only V5c --hosts api --max-usd 0.50 --timeout-min 30 2>&1 | tee songs\rowboat\batch_v5c.log`
6. Contact sheet `songs\rowboat\out\_qc\V5c-contact.png` (5×2, 10 frames evenly spaced, 384 wide) + 100% stills of frames
   12, 60, 114 (`_qc\V5c-f012.png` etc.).
7. Commit with `[skip ci]` and push: `comfy/prompt_lint.py`, `songs/rowboat/_make_rowboat.py`, `songs/rowboat/shots/`,
   `songs/rowboat/shots.csv`, `songs/rowboat/cutplan.json`, `queue/2026-10-01-rowboat-v5c` (not `out/`). **Do not judge the clip.**
**item-01.report.md:** lint + dry-run; run window UTC + Toronto; task id, wall s, length, refs, est; failure lines verbatim.
