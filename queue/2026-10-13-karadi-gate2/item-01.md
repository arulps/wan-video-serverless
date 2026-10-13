# item-01 — checks, render O3 + V3Q + V2A + V4A, sheets, commit (≤ $2.60 list)

0. **Prerequisite.** `queue\2026-10-13-karadi-gate1b\item-01.done` and `queue\2026-10-13-karadi-gate1b\FABLE-VERDICT.md` must exist.
   Otherwise → **blocked**, $0.00 spent.
1. `py tests\test_wan3_mock.py` → PASS.  2. Credentials check (as in the Shorts queues) → True (print only True/False).
3. **Gates:** `py tests\test_prompt_lint.py` → PASS; `py comfy\prompt_lint.py --song songs\a12-karadi-w3` →
   `LINT PASS: 18 shots, 0 fail, 0 warn`. Any failure → **blocked**.
4. Dry-run: `py comfy\batch_runner.py --song songs\a12-karadi-w3 --only O3,V3Q,V2A,V4A --hosts api --dry-run`
   → 4 rows, all `720P 16:9 audio=off`: O3 7 s refs=10; V3Q 6 s refs=6; V2A 6 s refs=2; V4A 6 s refs=6; "estimated $2.50";
   no `ERROR`, `unknown cast`, `MISSING`, `OVER BUDGET`, `refused` or `Traceback`. Report O3's 10 ref files' total bytes. Else → **blocked**.
5. Render:
   ```
   py comfy\batch_runner.py --song songs\a12-karadi-w3 --only O3,V3Q,V2A,V4A --hosts api --max-usd 2.60 --timeout-min 50 2>&1 | tee songs\a12-karadi-w3\batch_gate2.log
   ```
6. For each clip into `songs\a12-karadi-w3\out\_qc\` (30 fps; 6 s = 180 frames, 7 s = 210):
   - `<ID>-contact.png` — 5×2, 10 frames evenly spaced, 384 wide;
   - `<ID>-every4-first2s.png` — frames 0, 4, … 60, frame number burned in, 256 wide, 4×4;
   - `<ID>-every4-all.png` — every 4th frame of the whole clip, frame number burned in, 192 wide, 10 per row;
   - 100 % stills (1280×720) of frames 0, 30, 60, 90, 120, 150 and the last frame (`<ID>-fNNN.png`).
7. Commit with `[skip ci]` and push: `songs/a12-karadi-w3/` except `out/` (the batch log and `shots.csv` status cells),
   `queue/2026-10-13-karadi-gate1b/FABLE-VERDICT.md`, `queue/2026-10-13-karadi-gate2`, `queue/A12-WATCH-LOG.md`.
   `git add` by explicit path only. **Do not judge the clips.**

**item-01.report.md:** prerequisite; checks 1–3 output lines; dry-run rows + total + O3 ref bytes; run window UTC + Toronto; per clip:
task id, wall s, length, frames (ffprobe `-count_frames`), refs, est; failure lines verbatim; sheet/still paths; commit hash.
