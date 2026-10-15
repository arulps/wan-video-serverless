# item-01 — rebuild rev 2.3, rename the failed CAa, render CAa + CQb at 6 s, sheets, cut check, slot cuts, commit (≤ $1.20 list)

0. `queue\2026-10-14-karadi-rev27-gateB\item-01.done` exists → else **blocked**.
1. Rebuild: `py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\build_karadi_runsheet.py" "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama" --repo songs\a12-karadi-w3 --selftest`
   → `ok 21 clips 136 s $13.60 list $16.30 w/ reserve slots TA 29 EN 24 set image` + `SELFTEST OK`.
   Lint `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`.
   `py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\make_cutplan.py" songs\a12-karadi-w3` → `… TA 29 slots 154.800 s, EN 24 slots 128.000 s, 21 clips — all slots fit their clips, no gaps`.
   (make_cutplan.py was replaced today: the old copy added stale rev 1.x trims for I1 and HKb. Report `cutplan.json`'s I1 slip, which must be absent or 0.)
   **Status list must be exactly:** `done` = I1, CQ0, CQa, HKa, O1, V1A, V2A, V3A, V4A; `todo` = everything else (CAa is `todo` again because its
   prompt changed). **Only `shots\09_CAa.raw.txt` and `shots\10_CAb.raw.txt` may differ from the last commit** (`git diff --stat songs/a12-karadi-w3/shots`);
   `shots.csv` durations: CQb, CAa, CAb, HKb, O2, O3 = 6. Any mismatch → **blocked**.
2. Rename (`move -n`, never overwrite), report each:
   - `out\CAa-seed30313-w3.mp4` → `out\CAa-seed30313-w3-v2-parentswap.mp4`, and its `.json` the same way.
   - every `out\_qc\CAa-*.png` that has no `-v1-picnic` in its name → `<name>-v2-parentswap.png`.
   - If `out\CQb-seed30313-w3.mp4` exists (rev 1.x leftover), → `-v1-picnic` (and its `.json`).
3. `py tests\test_wan3_retry_mock.py` → PASS; credentials check → True.
4. Dry-run: `py comfy\batch_runner.py --song songs\a12-karadi-w3 --only CAa,CQb --hosts api --dry-run` → 2 rows, `720P 16:9 audio=off`,
   each **6 s**, refs = 7 (CAa ends `11-set-path-low`, CQb ends `12-set-path-high`); "estimated $1.20"; no `ERROR`/`MISSING`/`OVER BUDGET`/`Traceback`.
5. Render:
   ```
   py comfy\batch_runner.py --song songs\a12-karadi-w3 --only CAa,CQb --hosts api --max-usd 1.20 --timeout-min 40 2>&1 | tee songs\a12-karadi-w3\batch_gateB2.log
   ```
   If a task id was printed but the download failed: `py comfy\wan3_api.py fetch <id> songs\a12-karadi-w3\out\<ID>-seed30313-w3.mp4 --timeout-min 15` once ($0).
6. For each of CAa, CQb into `out\_qc\`: `<ID>-contact.png`, `<ID>-every4-all.png` (every 4th frame, number burned in, 192 wide, 10 per row),
   stills of frames 0, 30, 60, 90, 120, 150 and the last; **cut check** `ffmpeg -i out\<ID>-seed30313-w3.mp4 -vf "select='gt(scene,0.35)',showinfo" -f null -`
   → every frame number printed.
7. Slot cuts with the music into `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateB2\` (create it), same form as the Gate B
   cuts, slips/starts/lengths **from the rebuilt `karadi-shots.json`**: **CAa → TA slot 4, EN slot 3; CQb → TA slot 8, EN slot 7;
   CQa → TA slot 14, EN slot 12** (CQa is not re-rendered; its slip is now 1.9 s — this checks the trim). Name them `<ID>-<TA|EN>-slotNN.mp4`.
   Check each slot's clip id in the json matches the list above; if not, stop and report (do not cut other slots).
   Then `gateB2-slots.png`: one row per cut, 8 frames at 0.0, 0.67, 1.35, 2.02, 2.70, 3.37, 4.04, 4.72 s. Report each cut's slip, start, length, frames.
8. Commit with `[skip ci]` and push: `songs/a12-karadi-w3/` except `out/`, `queue/2026-10-14-karadi-rev27-gateB` (its FABLE-VERDICT.md),
   `queue/2026-10-14-karadi-rev27b-gateB2`, `queue/A12-WATCH-LOG.md`. **Do not judge the clips.**

**item-01.report.md:** step outputs; status list; git diff stat of `shots/`; renames; dry-run rows + total; run window; per clip task id /
wall s / length / frames / est / retry lines; scene-cut frames; failure lines verbatim; sheet paths; the six slot cuts with slip/start/length/frames;
final estimate; commit hash.
