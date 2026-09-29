# CC QUEUE — 2026-09-29 "Learning batch 2": animals A1–A6 + 3 retakes on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Fable reviewed learning batch 1 (`songs\shorts-learning\REVIEW-learning-batch1-2026-09-29.md`): 66/69 good.
This queue renders the last 6 learning Shorts (animals at the garden gate, object only, new world `world-garden-gate.txt`)
and 3 retakes (`MN1_w3b`, `MN3_w3b` arms-down start/end, `VG3_w3b` a real drumstick), seed 4242 for retakes.
Dry-run by Fable: 9 rows, $4.50.

## Hard limits
- **API spend ≤ $5.00 at list price** (estimate $4.50; ~$3.15 with the 30% discount). No pod, no GPU, no upscale.
- Only these 9 rows; no extra seeds; failures are reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do not touch `<ID>-metadata.md` files or existing clips in `renders-learning\`; only add files.

## Protocol (markers in `queue\2026-09-29-learning-batch2\`)
As in `queue\2026-09-28-shorts-retakes1`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Learning batch 2 done — ask Fable to review queue\2026-09-29-learning-batch2".
