# CC QUEUE — 2026-10-01 "Rowboat W1": L04 Row Row Row Your Boat, world 1 (river morning + Modhu) on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Arul approved gate-2 **V1a** (`songs\rowboat\out\V1a-seed30313-w3.mp4`) as the look-lock: both kids side by side on one bench
facing Appa, sitting inside the boat. Fable rewrote the seating override in `songs\rowboat\_make_rowboat.py` to that layout
(bench / inside the boat / no rim / nobody stands; kid two-shots start already seated) and regenerated `shots\*.raw.txt`;
the master runsheet and builder are untouched. Gate-2 V1b (kids standing at the start) kept as
`out\V1b-seed30313-w3-v1-standing.mp4` (+ `_qc\V1b-v1-standing-*.png`); V1b status cell blanked.
This queue renders the rest of world 1: **I1, I2, V1b, V1c, V2a, V2b, V2c, V2d, X1a, X1b** (45 s). Est **$4.50** list.

## Hard limits
- **API spend ≤ $5.00 at list price.** Only the 10 shots above. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\`.
- Do not delete, overwrite or re-render `V1a-seed30313-w3.mp4` or any `*-v1-*` file.

## Protocol (markers in `queue\2026-10-01-rowboat-w1\`)
As in `queue\2026-10-01-rowboat-gate2`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Rowboat W1 done — ask Fable to review queue\2026-10-01-rowboat-w1".
