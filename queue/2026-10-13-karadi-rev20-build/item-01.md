# item-01 — build rev 2.0 on Beast, lint, dry-run, cut plan, tidy, commit ($0.00)

0. Tidy: rename `queue\2026-10-13-karadi-pacing` → `queue\2026-10-13-karadi-pacing-SUPERSEDED` (it never had a READY file; Arul
   dropped the reference download). Rename only.
1. Build (from the repo root):
   ```
   py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\build_karadi_runsheet.py" "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama" --repo songs\a12-karadi-w3 --selftest
   ```
   - Expect the last two lines: `ok 21 clips 146 s $14.60 list $17.50 w/ reserve slots TA 29 EN 24 no set image` (or `set image`
     if Arul has already dropped all three plates into `refs\`) and `SELFTEST OK: place, facing, word-action, pacing, camera rules all refuse a bad clip`.
   - Any traceback or AssertionError → **blocked**, verbatim.
2. `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → expect `LINT PASS: 21 shots, 0 fail, 0 warn`. Anything else → **blocked**, verbatim.
3. `py comfy\batch_runner.py --song songs\a12-karadi-w3 --hosts http://x --dry-run` → expect the final line
   `engine=wan3 rows: estimated $12.20 at list price ...` and no `REF MISSING` / `OVER BUDGET`. Report the final line.
4. Status check: `py -c "import csv;print([(r['shot_id'],r['status']) for r in csv.DictReader(open('songs/a12-karadi-w3/shots.csv',encoding='utf-8'))])"`
   → expect V1A, V2A, V3A, V4A = `done`, all 17 others = `todo`. Anything else → **blocked**.
5. `py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\make_cutplan.py" songs\a12-karadi-w3` → expect
   `... TA 29 slots 154.800 s, EN 24 slots 128.000 s, 21 clips — all slots fit their clips, no gaps`.
6. Commit with `[skip ci]` and push:
   - `songs/a12-karadi-w3/` (shots.csv, shots/, lint.json, scale.json, world.txt, characters.txt, cutplan.json, refs/send/);
   - `queue/2026-10-13-karadi-rev20-build`, `queue/2026-10-13-karadi-pacing-SUPERSEDED`, `queue/A12-WATCH-LOG.md`.
   Message: `a12 rev 2.0: the family trek — 17 new clips planned (encounter, two trek stops, quick spin-and-skip in the hook, word-actions, home finale), 4 verse answers kept; lint 21/0/0, dry-run $12.20 [skip ci]`

   **Do not judge the prompts.**

**item-01.report.md** must cover: each step's output verbatim (steps 1–5), the status list, `git status --short` before the add,
the commit hash.
