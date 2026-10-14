# item-01 — rebuild rev 2.2, keep the multi-shot takes, render HKa + O1, sheets, slot cuts, commit (≤ $1.60 list)

1. **Rebuild** (from the repo root):
   ```
   py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\build_karadi_runsheet.py" "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama" --repo songs\a12-karadi-w3 --selftest
   ```
   Expect `ok 21 clips 146 s $14.60 list $17.50 w/ reserve slots TA 29 EN 24 set image` and `SELFTEST OK: ...`. Then:
   - `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`;
   - `shots\05_HKa.raw.txt`: line 2 starts `Generate single shot.`; contains "dance his happy dance TOGETHER"; contains **no**
     "seconds," time range (`findstr /C:"to 1.1 seconds"` finds nothing);
   - status list: **HKa `todo`, O1 `todo`** (their prompts changed), V1A–V4A `done`, the other 15 `todo`.
   Any mismatch → **blocked**, verbatim.
2. **Keep the Gate A takes** (rename, never delete): in `songs\a12-karadi-w3\out\`, `HKa-seed30313-w3.mp4/.json` →
   `HKa-seed30313-w3-v1-multishot.mp4/.json`, and the same for O1; in `out\_qc\`, every `HKa-*` and `O1-*` file → the same name with
   `-v1-multishot` before the extension. Report the renamed files.
3. `py tests\test_wan3_retry_mock.py` → `PASS … 10 checks`; credentials check → True (print only True/False).
4. Dry-run: `py comfy\batch_runner.py --song songs\a12-karadi-w3 --only HKa,O1 --hosts api --dry-run` → 2 rows, `720P 16:9 audio=off`,
   HKa 8 s refs = 7 (… `11-set-path-low`), O1 7 s refs = 9 (… `13-set-home`), "estimated $1.50"; no `ERROR`/`MISSING`/`OVER BUDGET`/`Traceback`.
5. Render:
   ```
   py comfy\batch_runner.py --song songs\a12-karadi-w3 --only HKa,O1 --hosts api --max-usd 1.60 --timeout-min 40 2>&1 | tee songs\a12-karadi-w3\batch_gateA4.log
   ```
   On a failure: report every line verbatim; if a task id was printed but the download failed, run
   `py comfy\wan3_api.py fetch <id> songs\a12-karadi-w3\out\<ID>-seed30313-w3.mp4 --timeout-min 15` once ($0), then block if still missing.
6. QC sheets for HKa (240 frames) and O1 (210) into `out\_qc\`: `<ID>-contact.png`, `<ID>-every4-all.png` (every 4th frame, number
   burned in, 192 wide, 10 per row), 100 % stills of frames 0, 12, 24, 36, 48, 60, 72, 90, 120, 150, 180 and the last.
   **Plus a cut check:** `ffmpeg -i out\<ID>-seed30313-w3.mp4 -vf "select='gt(scene,0.35)',showinfo" -f null -` → report every frame
   number it prints (Fable expects none — that is the single-shot check).
7. Slot cuts with the music into `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateA2\` (create it) — the same four
   files, slips, starts and lengths, and the same ffmpeg form as `queue\2026-10-14-karadi-rev25-gateA3\item-01.md` step 6, plus
   `gateA2-slots.png` (8 frames per row at the beats).
8. Commit with `[skip ci]` and push: `songs/a12-karadi-w3/` except `out/` (shots.csv, shots/, lint.json, scale.json, world.txt,
   characters.txt, cutplan.json, refs/send/ with `-f`, `batch_gateA4.log`), `queue/2026-10-14-karadi-rev25-gateA3` (its FABLE-VERDICT.md),
   `queue/2026-10-14-karadi-rev26-gateA-retake`, `queue/A12-WATCH-LOG.md`. **Do not judge the clips.**

**item-01.report.md:** step 1 outputs + status list; the renames; dry-run rows + total; run window UTC + Toronto; per clip: task id,
wall s, frames, est, retry lines; the scene-cut frame numbers per clip; failure lines verbatim; sheet/still paths; the four slot cuts
with frame counts and the sheet path; the runner's final estimate; the commit hash.
