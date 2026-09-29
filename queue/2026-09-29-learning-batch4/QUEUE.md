# CC QUEUE — 2026-09-29 "Learning batch 4": home sounds with a kid + crow with locked frames

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Batch 3 review: object-only SN1/SN2/SN6 still looked real; SN3 clock hands turned (loop jump); A6 crow still punched in; A3 hen good.
Arul approved (13:29): put Minnu/Mintu in the home-sound shots to anchor the cartoon style (`SN1_w3c` cooker + Mintu covering ears,
`SN2_w3c` Minnu rings the bell, `SN3_w3c` Mintu's head follows the pendulum, `SN6_w3c` mixie + Minnu covering ears), and the crow
`A6_w3c` with first + last frame locked to the empty gate (`songs\shorts-learning\keyframes\A6-gate-empty.png`, frame 0 of A6_w3).
SN4 keeps its first render. Dry-run by Fable: 5 rows, $2.50.

## Hard limits
- **API spend ≤ $3.00 at list price** (estimate $2.50; ~$1.75 with the 30% discount). No pod, no GPU, no upscale.
- Only these 5 rows; no extra seeds; failures are reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do not touch `<ID>-metadata.md` files or existing clips in `renders-learning\`; only add files.

## Protocol (markers in `queue\2026-09-29-learning-batch4\`)
As in `queue\2026-09-28-shorts-retakes1`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Learning batch 4 done — ask Fable to review queue\2026-09-29-learning-batch4".
