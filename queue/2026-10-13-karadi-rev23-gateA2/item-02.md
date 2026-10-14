# item-02 — render HKa (+ O1 only if not recovered), QC sheets, slot cuts with the music, commit (≤ $1.60 list)

0. Read item-01's outcome: `ONLY=HKa` if "O1 recovered", else `ONLY=HKa,O1`. Credentials check → True (print only True/False).
1. Checks (verify, don't edit): `shots\05_HKa.raw.txt` contains "the children do their own quick full turn beside him" and
   "Image 7 is the lower forest path set"; `shots.csv` has HKa `todo` (and O1 `todo` only if not recovered); `out\` has no
   `HKa-seed30313-w3.mp4` at the top level. `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`.
   Any mismatch → **blocked**.
2. Dry-run: `py comfy\batch_runner.py --song songs\a12-karadi-w3 --only %ONLY% --hosts api --dry-run` → 1 or 2 rows,
   `720P 16:9 audio=off`, HKa 8 s refs = 7 (`01-mintu-front`, `02-minnu-front`, `03-karadi-mama`, `06-amma-front`, `07-appa-face`,
   `08b-appa-body-backpack`, `11-set-path-low`), "estimated $0.80" (or $1.50 with O1); no `ERROR`/`MISSING`/`OVER BUDGET`/`Traceback`.
3. Render:
   ```
   py comfy\batch_runner.py --song songs\a12-karadi-w3 --only %ONLY% --hosts api --max-usd 1.60 --timeout-min 40 2>&1 | tee songs\a12-karadi-w3\batch_gateA2.log
   ```
   If the client logs `connection error … retry`, that is the new behaviour — let it run. If a row still fails after the retries,
   report the lines verbatim and **block**; do not re-run.
4. QC sheets for each clip rendered or recovered (HKa = 240 frames, O1 = 210) into `out\_qc\`: `<ID>-contact.png` (5×2, 384 wide);
   `<ID>-every4-all.png` (every 4th frame, number burned in, 192 wide, 10 per row); 100 % stills of frames 0, 12, 24, 36, 48, 60, 72,
   90, 120, 150, 180 and the last frame.
5. Slot cuts with the music into `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateA\` (create it), exactly as
   `2026-10-13-karadi-rev22-gateA\item-01.md` step 7 specifies (same four files, same slips, starts and lengths, same ffmpeg form),
   and the per-slot sheet `gateA-slots.png` (8 frames per row at the beats 0.0, 0.67, 1.35, 2.02, 2.70, 3.37, 4.04, 4.72 s).
6. Commit with `[skip ci]` and push: `songs/a12-karadi-w3/` except `out/`, `queue/2026-10-13-karadi-rev23-gateA2`,
   `queue/A12-WATCH-LOG.md`. **Do not judge the clips.**

**item-02.report.md:** ONLY used; checks; dry-run rows + total; run window UTC + Toronto; per clip: task id, wall s, length,
frames, refs, est, any retry lines; failure lines verbatim; sheet/still paths; the four slot-cut paths with frame counts
(159–160 each) and the sheet path; the runner's final estimate; the commit hash.
