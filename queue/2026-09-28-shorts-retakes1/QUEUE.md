# CC QUEUE — 2026-09-28 "Shorts retakes 1": L03 yawn, L04 sneeze, L10 raindrop on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Source: Fable's review `songs\shorts-loops\REVIEW-shorts-batch1-2026-09-28.md` + Arul's notes. Fable wrote
`shots/L03-w3b.txt` (stronger loop wording, seed 4242), `shots/L04-w3b.txt` (clean nose, no white mark),
`shots/L10-w3b.txt` + `world-garden-rain.txt` (outdoors in the garden rain, under a colocasia leaf) and 3 rows in shots.csv
(`L03_w3b`, `L04_w3b`, `L10_w3b`). Dry-run already checked by Fable: 3 rows, `audio=on`, estimated $1.60.

## Hard limits
- **API spend ≤ $1.80 at list price** (estimate $1.60, ~$1.12 with the 30% discount). No pod, no GPU, no upscaling.
- Only these 3 rows. No extra seeds / "one more try". Failed rows are reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore `shots.csv` (the runner edits status cells). Commits carry `[skip ci]`.
- Do not touch the `Lxx-metadata.md` files in `C:\Channel Contents\MinMiniKids\YT Shorts\renders\Lxx\` and do not delete the
  first-batch clips there — the retakes are added next to them.

## Protocol (markers in `queue\2026-09-28-shorts-retakes1\`)
Items run back to back. For item N: append `[<time>] item-N start` to LOG.md → do it → write `item-N.report.md` → create
`item-N.done`. On a failed check: `item-N.blocked`, a line in LOG.md, stop. After item-02: `QUEUE END <time> est $<x>` in
LOG.md and tell Arul "Shorts retakes 1 done — ask Fable to review queue\2026-09-28-shorts-retakes1".
