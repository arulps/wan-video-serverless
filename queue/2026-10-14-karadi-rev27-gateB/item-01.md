# item-01 — rebuild, render CQ0 + CQa + CAa + I1, sheets, cut check, slot cuts with the music, commit (≤ $3.20 list)

1. Rebuild: `py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\build_karadi_runsheet.py" "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama" --repo songs\a12-karadi-w3 --selftest`
   → `ok 21 clips 146 s … set image` + `SELFTEST OK`. Lint → `LINT PASS: 21 shots, 0 fail, 0 warn`. `py "…\_gen\make_cutplan.py" songs\a12-karadi-w3`
   → `… no gaps`. Status list: **HKa, O1, V1A–V4A `done`; CQ0, CQa, CAa, I1 `todo`.** Any mismatch → **blocked**.
2. If `out\` has `CQa-`, `CAa-` or `I1-seed30313-w3.mp4` (rev 1.x leftovers), rename each with `-v1-picnic` (and its `.json`); report.
3. `py tests\test_wan3_retry_mock.py` → PASS; credentials check → True.
4. Dry-run: `py comfy\batch_runner.py --song songs\a12-karadi-w3 --only CQ0,CQa,CAa,I1 --hosts api --dry-run` → 4 rows, `720P 16:9 audio=off`;
   CQ0/CQa/CAa 8 s refs = 7 (… `08b-appa-body-backpack`, `11-set-path-low`), I1 7 s refs = 5 (no set plate); "estimated $3.10";
   no `ERROR`/`MISSING`/`OVER BUDGET`/`Traceback`.
5. Render:
   ```
   py comfy\batch_runner.py --song songs\a12-karadi-w3 --only CQ0,CQa,CAa,I1 --hosts api --max-usd 3.20 --timeout-min 50 2>&1 | tee songs\a12-karadi-w3\batch_gateB.log
   ```
   On a failure: report verbatim; if a task id was printed but the download failed, `py comfy\wan3_api.py fetch <id> songs\a12-karadi-w3\out\<ID>-seed30313-w3.mp4 --timeout-min 15` once ($0).
6. For each rendered clip into `out\_qc\`: `<ID>-contact.png`, `<ID>-every4-all.png` (every 4th frame, number burned in, 192 wide, 10 per
   row), 100 % stills of frames 0, 30, 60, 90, 120, 150, 180 and the last; **cut check** `ffmpeg -i out\<ID>-seed30313-w3.mp4 -vf
   "select='gt(scene,0.35)',showinfo" -f null -` → report every frame number printed.
7. Slot cuts with the music into `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateB\` (create it), same form as the
   gate A cuts, using the slips/starts/lengths **from the rebuilt `karadi-shots.json`** (`cutplan.ta` / `cutplan.en`) for these slots:
   CQ0 → TA slot 2 and EN slot 2; CQa → TA slot 8 and EN slot 7; CAa → TA slot 4 and EN slot 3; I1 → TA slot 1 and EN slot 1.
   Name them `<ID>-<TA|EN>-slotNN.mp4`. Then `gateB-slots.png`: one row per cut, 8 frames at 0.0, 0.67, 1.35, 2.02, 2.70, 3.37, 4.04, 4.72 s.
   Report each cut's slip, start, length and frame count.
8. Commit with `[skip ci]` and push: `songs/a12-karadi-w3/` except `out/`, `queue/2026-10-14-karadi-rev26-gateA-retake` (with its
   FABLE-VERDICT.md), `queue/2026-10-14-karadi-rev27-gateB`, `queue/A12-WATCH-LOG.md`. **Do not judge the clips.**

**item-01.report.md:** step outputs; renames; dry-run rows + total; run window; per clip task id / wall s / frames / est / retry lines;
scene-cut frames per clip; failure lines verbatim; sheet paths; the eight slot cuts with slip/start/length/frames; final estimate; commit hash.
