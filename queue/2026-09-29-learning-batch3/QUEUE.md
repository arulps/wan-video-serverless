# CC QUEUE — 2026-09-29 "Learning batch 3": cartoon-style retakes for the home sounds + 2 animals

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Arul: the cooker, bell and mixie look real, not animated. Fable: same for the clock and rain window; and batch 2's A3 hen and
A6 crow cut to a closer shot mid-clip. The generator now adds a strong cartoon-object style + "one continuous shot" to every
shot with no character. Retakes (seed 4242): `SN1_w3b SN2_w3b SN3_w3b SN4_w3b SN6_w3b A3_w3b A6_w3b`. Dry-run by Fable: 7 rows, $3.50.
Batch 2 review: A1, A2, A4, A5 and the MN1/MN3/VG3 retakes are good.

## Hard limits
- **API spend ≤ $4.00 at list price** (estimate $3.50; ~$2.45 with the 30% discount). No pod, no GPU, no upscale.
- Only these 7 rows; no extra seeds; failures are reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do not touch `<ID>-metadata.md` files or existing clips in `renders-learning\`; only add files.

## Protocol (markers in `queue\2026-09-29-learning-batch3\`)
As in `queue\2026-09-28-shorts-retakes1`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Learning batch 3 done — ask Fable to review queue\2026-09-29-learning-batch3".
