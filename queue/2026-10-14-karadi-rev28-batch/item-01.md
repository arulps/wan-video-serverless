# item-01 — rebuild, render the 10 batch clips, sheets, cut check (≤ $6.30 list)

0. `queue\2026-10-14-karadi-rev27b-gateB2\item-01.done` exists → else **blocked**.

1. Rebuild: `py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\build_karadi_runsheet.py" "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama" --repo songs\a12-karadi-w3 --selftest`
   → `ok 21 clips 136 s … set image` + `SELFTEST OK`; lint `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`.
   Status list: the 11 gate/kept clips (I1, CQ0, CQa, CQb, CAa, HKa, O1, V1A–V4A) `done`; the 10 batch IDs `todo`. `git diff --stat
   songs/a12-karadi-w3/shots` → **only `shots\10_CAb.raw.txt`** changed (rev 2.3.1: CAb opens with the question lead; CAb is still `todo`).
   `out\CAa-seed30313-w3-splice.mp4` exists (Fable's $0 splice, 180 frames, 6.000 s). Any other mismatch → **blocked**.
2. For each batch ID, if `out\<ID>-seed30313-w3.mp4` exists (rev 1.x leftover), rename it and its `.json` with `-v1-picnic`; report.
3. `py tests\test_wan3_retry_mock.py` → PASS; credentials check → True.
4. Dry-run: `py comfy\batch_runner.py --song songs\a12-karadi-w3 --only HKc,HKb,CAb,JOIN,V1Q,V2Q,V3Q,V4Q,O2,O3 --hosts api --dry-run`
   → 10 rows, all `720P 16:9 audio=off`, HKc 8 s and the other nine 6 s, "estimated $6.20", no `ERROR`/`MISSING`/`OVER BUDGET`/`Traceback`; report each row's length and ref count.
5. Render:
   ```
   py comfy\batch_runner.py --song songs\a12-karadi-w3 --only HKc,HKb,CAb,JOIN,V1Q,V2Q,V3Q,V4Q,O2,O3 --hosts api --max-usd 6.30 --timeout-min 90 2>&1 | tee songs\a12-karadi-w3\batch_main.log
   ```
   For any row that printed `submitted task <id>` but did not download: `py comfy\wan3_api.py fetch <id> songs\a12-karadi-w3\out\<ID>-seed30313-w3.mp4 --timeout-min 15` once ($0).
6. For each rendered clip into `out\_qc\`: `<ID>-contact.png`, `<ID>-every4-all.png` (every 4th frame, number burned in, 192 wide, 10 per
   row), 100 % stills of frames 0, 60, 120, 180 and the last; **cut check** `ffmpeg -i out\<ID>-seed30313-w3.mp4 -vf
   "select='gt(scene,0.35)',showinfo" -f null -` → every frame number printed, per clip.

**item-01.report.md:** step outputs; renames; dry-run rows; run window; a table per clip: task id, status, wall s, frames, est, retry lines,
scene-cut frames; failure lines verbatim; the runner's final estimate.
