# item-02 — second half: V4a,V4b,V4c,V4d,V5b,V5c,V5d,V6a,V6b,V6c,V6d,O3,O4 (67 s, ≤ $7.00 list), sheets, commit

1. Render the second half:
   ```
   python comfy\batch_runner.py --song songs\a07-butterfly --only V4a,V4b,V4c,V4d,V5b,V5c,V5d,V6a,V6b,V6c,V6d,O3,O4 --hosts api --max-usd 7.00 --timeout-min 90 2>&1 | tee songs\a07-butterfly\batch1b.log
   ```
2. Sheets and stills as in item-01 step 7 (O4: 7×3).
3. `python tests\test_song_cuts_reuse.py` (full stand-in test, $0) → PASS line.
4. Commit with `[skip ci]` and push: `songs/a07-butterfly/` (everything except `out/`), `queue/2026-10-02-butterfly-batch1`.
   **Do not judge the clips.**
**item-02.report.md:** run window; table per clip as in item-01; failure lines verbatim; total est for the queue; stand-in test
PASS line; commit hash; a list of any ID whose status is not `done`.
