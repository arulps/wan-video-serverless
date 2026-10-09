# item-01 — tidy, checks, render ZK1 + ZO, sheets, commit (≤ $2.10 list)

1. **Tidy old shot files.** `songs\l05-urulai-w3\shots\` still has rev 1.9 files that `shots.csv` no longer names (e.g. `04_Z1.raw.txt`,
   `12_K1.raw.txt`, `21_O1.raw.txt`). Move every `shots\*.raw.txt` that is **not** referenced in `shots.csv` to
   `_to_delete\l05-urulai-w3-shots-rev19\` (repo root `_to_delete\` is git-ignored). Report the moved names; 17 must remain, one per
   `shots.csv` row.
2. **Beast Python packages (first API render on this machine).** `py -c "import comfy.batch_runner"` is not enough — instead run the
   mock test in step 3; if it fails only on a missing module, install just that module with `py -m pip install <module>` (local, $0),
   note it in the report, and re-run. Do **not** install the rest of `requirements.txt`.
3. `py tests\test_wan3_mock.py` → PASS.  4. Credentials check (as in the Shorts queues) → True (print only True/False).
5. **Gates:** `py tests\test_prompt_lint.py` → PASS; `py comfy\prompt_lint.py --song songs\l05-urulai-w3` →
   `LINT PASS: 17 shots, 0 fail, 0 warn`. Any failure → **blocked**.
6. Dry-run: `py comfy\batch_runner.py --song songs\l05-urulai-w3 --only ZK1,ZO --hosts api --dry-run`
   → 2 rows, `720P 16:9 audio=off`; ZK1 10 s refs=3 (Baby Potato, Brinjal, the kitchen shelf set); ZO 10 s refs=10 (Baby Potato,
   Amma Potato, Brinjal, Okra, Tomato, Carrot, Radish, Cabbage, Beans, the kitchen shelf set); "estimated $2.00"; no MISSING/ERROR.
   Else → **blocked**.
7. Render:
   ```
   py comfy\batch_runner.py --song songs\l05-urulai-w3 --only ZK1,ZO --hosts api --max-usd 2.10 --timeout-min 40 2>&1 | tee songs\l05-urulai-w3\batch_gate1.log
   ```
8. For each clip into `songs\l05-urulai-w3\out\_qc\`: `<ID>-contact.png` (5×2, 10 frames evenly spaced, 384 wide),
   `<ID>-every4-first2s.png` (frames 0,4,8,…,60 with the frame number burned in, 256 wide, tiled 4×4),
   `<ID>-every10.png` (every 10th frame, 256 wide, tiled 6×5, frame number burned in), and 100% stills of frames 0, 75, 140, 150,
   210 and the last frame (`<ID>-fNNN.png`).
9. Commit with `[skip ci]` and push: `songs/l05-urulai-w3/` (everything except `out/`; includes `refs/`), `queue/2026-10-09-urulai-gate1`.
   **Do not judge the clips.**

**item-01.report.md:** moved files; any module installed; checks; dry-run rows + total; run window UTC + Toronto; per clip: task id,
wall s, length, frames, refs, est; failure lines verbatim; sheet/still paths; commit hash.
