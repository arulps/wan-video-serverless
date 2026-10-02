# item-01 — keep old V2a, checks, render V2a, sheets, commit (≤ $0.60 list)

1. In `songs\a07-butterfly\out\` rename (not copy, not delete), for ID = V2a only (V1a is kept as is):
   `<ID>-seed30313-w3.mp4/.json` → `<ID>-seed30313-w3-v1.mp4/.json`; and in `out\_qc\` every `<ID>-*.png`
   (contact, f000/f074/f149, strip, every10) → same name with `-v1` before `.png`. The runner rewrites `<ID>-strip.png`, so it
   must be renamed before the render.
2. `python tests\test_wan3_mock.py` → PASS.  3. Credentials check (as in the Shorts queues) → True.
4. **Gates:** `python tests\test_prompt_lint.py` → PASS; `python comfy\prompt_lint.py --song songs\a07-butterfly` →
   `LINT PASS: 33 shots, 0 fail, 0 warn`; `python tests\test_song_cuts_reuse.py --plan-only` → PASS. Any failure → **blocked**.
5. Dry-run: `python comfy\batch_runner.py --song songs\a07-butterfly --only V2a --hosts api --dry-run`
   → 1 row, `720P 16:9 audio=off`, 5 s, refs=3 (Minnu, Priya, the yellow butterfly), "estimated $0.50", no MISSING/ERROR. Else → **blocked**.
6. Render:
   ```
   python comfy\batch_runner.py --song songs\a07-butterfly --only V2a --hosts api --max-usd 0.60 --timeout-min 30 2>&1 | tee songs\a07-butterfly\batch_gate2b.log
   ```
7. For V2a: `_qc\<ID>-contact.png` (5×2, 10 frames evenly spaced, 384 wide), `_qc\<ID>-every10.png` (every 10th frame,
   256 wide, tiled 5×3), and 100% stills `_qc\<ID>-f000.png`, `-f074.png`, `-f149.png`.
8. Commit with `[skip ci]` and push: `songs/a07-butterfly/` (everything except `out/`), `queue/2026-10-02-butterfly-gate2b`.
   **Do not judge the clips.**
**item-01.report.md:** renames; checks; dry-run; run window UTC + Toronto; per clip: task id, wall s, length, frames, refs, est;
failure lines verbatim; sheet/still paths; commit hash.
