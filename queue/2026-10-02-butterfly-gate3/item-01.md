# item-01 — keep old RA, checks, render RA + V2b + V5a, sheets, commit (≤ $2.00 list)

1. In `songs\a07-butterfly\out\` rename (not copy, not delete): `RA-seed30313-w3.mp4/.json` → `RA-seed30313-w3-v2-oldrefs.mp4/.json`;
   in `out\_qc\` every `RA-*.png` that has no `-v1-`/`-v2-` in its name (contact, f000/f119/f239, strip) → same name with
   `-v2-oldrefs` before `.png`. (V2b and V5a have no earlier takes.)
2. `python tests\test_wan3_mock.py` → PASS.  3. Credentials check (as in the Shorts queues) → True.
4. **Gates:** `python tests\test_prompt_lint.py` → PASS; `python comfy\prompt_lint.py --song songs\a07-butterfly` →
   `LINT PASS: 33 shots, 0 fail, 0 warn`; `python tests\test_song_cuts_reuse.py --plan-only` → PASS. Any failure → **blocked**.
5. Dry-run: `python comfy\batch_runner.py --song songs\a07-butterfly --only RA,V2b,V5a --hosts api --dry-run`
   → 3 rows, `720P 16:9 audio=off`; RA 8 s refs=6, V2b 5 s refs=3 (Minnu, Priya, the yellow butterfly), V5a 5 s refs=8;
   "estimated $1.80"; no MISSING/ERROR. Else → **blocked**.
6. Render:
   ```
   python comfy\batch_runner.py --song songs\a07-butterfly --only RA,V2b,V5a --hosts api --max-usd 2.00 --timeout-min 40 2>&1 | tee songs\a07-butterfly\batch_gate3.log
   ```
7. For each: `_qc\<ID>-contact.png` (5×2, 10 frames evenly spaced, 384 wide), `_qc\<ID>-every10.png` (every 10th frame, 256 wide,
   tiled 5×3; RA: 6×4), and 100% stills of the first, middle and last frame (`_qc\<ID>-f000.png`, `-fMID`, `-fLAST` with real numbers).
8. Commit with `[skip ci]` and push: `songs/a07-butterfly/` (everything except `out/`; includes the new `refs/01`, `refs/02`),
   `queue/2026-10-02-butterfly-gate3`. **Do not judge the clips.**
**item-01.report.md:** renames; checks; dry-run rows + total; run window UTC + Toronto; per clip: task id, wall s, length, frames,
refs, est; failure lines verbatim; sheet/still paths; commit hash.
