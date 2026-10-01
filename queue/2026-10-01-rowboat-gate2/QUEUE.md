# CC QUEUE — 2026-10-01 "Rowboat gate 2": L04 Row Row Row Your Boat, new seating — V1a retake + V1b on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Gate 1 (V1a) passed on look, but the kids read as perched on the boat's rim. Arul's seating call: both kids in the back half
of the boat on two low benches **facing each other**, Appa rowing in the front half facing them; the kid two-shots become a
side-on shot of both. Fable applied this as an override in `songs\rowboat\_make_rowboat.py` (`SEAT_ALL` / `SEAT_SHOT`, with
asserts) and regenerated `shots\*.raw.txt`; the master runsheet and builder are untouched. Old V1a kept as
`songs\rowboat\out\V1a-seed30313-w3-v1-rimseat.mp4` (+ `_qc\V1a-v1-rimseat-*.png`); V1a status cell blanked.
This queue re-renders **V1a** (6 s, wide, look-lock) and **V1b** (3 s, first kid two-shot) to check the new seating.
Est: $0.60 + $0.30 = **$0.90** list.

## Hard limits
- **API spend ≤ $1.00 at list price.** Only `V1a,V1b`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\`.
- Do not delete or overwrite the `*-v1-rimseat*` files.

## Protocol (markers in `queue\2026-10-01-rowboat-gate2\`)
As in `queue\2026-10-01-rowboat-gate`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Rowboat gate 2 done — ask Fable to review queue\2026-10-01-rowboat-gate2".
