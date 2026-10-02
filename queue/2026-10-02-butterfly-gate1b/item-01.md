# item-01 — keep old RA, checks, render RA + RB + V1a + V2a, sheets, commit (≤ $2.80 list)

1. Rename (not copy, not delete) in `songs\a07-butterfly\out\`: `RA-seed30313-w3.mp4` → `RA-seed30313-w3-v1-tall-priya.mp4` and
   `RA-seed30313-w3.json` → `RA-seed30313-w3-v1-tall-priya.json`. The `_qc\RA-*` files stay as they are.
2. `python tests\test_wan3_mock.py` → PASS.  3. Credentials check (as in the Shorts queues) → True.
4. **Gates:** `python tests\test_prompt_lint.py` → PASS; `python comfy\prompt_lint.py --song songs\a07-butterfly` →
   `LINT PASS: 33 shots, 0 fail, 0 warn`; `python tests\test_song_cuts_reuse.py --plan-only` → PASS. Any failure → **blocked**.
5. Dry-run: `python comfy\batch_runner.py --song songs\a07-butterfly --only RA,RB,V1a,V2a --hosts api --dry-run`
   → 4 rows, all `720P 16:9 audio=off`; RA 8 s refs=6, RB 8 s refs=4, V1a 5 s refs=3 (Mintu, Leo, the red butterfly),
   V2a 5 s refs=3 (Minnu, Priya, the yellow butterfly); "estimated $2.60"; no MISSING/ERROR. Else → **blocked**.
6. Render:
   ```
   python comfy\batch_runner.py --song songs\a07-butterfly --only RA,RB,V1a,V2a --hosts api --max-usd 2.80 --timeout-min 40 2>&1 | tee songs\a07-butterfly\batch_gate1b.log
   ```
7. For each of the 4 clips: contact sheet `songs\a07-butterfly\out\_qc\<ID>-contact.png` (5×2, 10 frames evenly spaced, 384 wide;
   RA's overwrites the old RA sheet — first rename the old one to `RA-contact-v1-tall-priya.png`) + 100% stills of the first,
   middle and last frame (`_qc\<ID>-f000.png`, `-fMID.png` with the real frame number, `-fLAST.png` likewise).
8. Commit with `[skip ci]` and push: `tests/test_song_cuts_reuse.py`, `songs/a07-butterfly/` (everything except `out/`),
   `queue/2026-10-02-butterfly-gate1b`. **Do not judge the clips.**
**item-01.report.md:** rename done; checks; dry-run rows + total; run window UTC + Toronto; per clip: task id, wall s, length,
frames, refs, est; failure lines verbatim; sheet/still paths; commit hash.
