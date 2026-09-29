# CC QUEUE — 2026-09-29 "Learning batch 5": crow A6, one more try

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Arul OK (14:01). `A6_w3d`: first + last frame locked to `songs\shorts-learning\keyframes\A6-gate-empty.png` (as A6_w3c, which looped
perfectly but kept the crow tiny on the far swing); the prompt now lands a big crow on the middle of the gate, close to camera.
Dry-run by Fable: 1 row, $0.50.

## Hard limits
- **API spend ≤ $0.60 at list price.** No pod, no GPU, no upscale. Only this row; no extra seeds; a failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do not touch `<ID>-metadata.md`, `USE-CLIPS.md` or existing clips in `renders-learning\`; only add files.

## Protocol (markers in `queue\2026-09-29-learning-batch5\`)
As in `queue\2026-09-28-shorts-retakes1`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Learning batch 5 done — ask Fable to review queue\2026-09-29-learning-batch5".
