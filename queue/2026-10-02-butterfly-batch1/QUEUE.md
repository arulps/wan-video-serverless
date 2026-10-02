# CC QUEUE — 2026-10-02 "Butterfly batch 1": A07 Butterfly rev 3.5 — the remaining 27 clips on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Gate 3 (new relaxed Mintu/Minnu refs) passed: RA approved (all four kids the same height, mothers on the bench), V2b kept.
V5a showed a fifth (small yellow) butterfly but is kept (Arul, 2 Oct). Rev 3.5 fix in every butterfly prompt: an exact count
("exactly four butterflies… no extra butterflies anywhere") and the yellow one is "a little smaller and rounder" (no "baby").
Fable's checks: LINT PASS 33/0/0, plan test PASS. Done and kept: RA, RB, V1a, V2a (splice), V2b, V5a.
**27 clips, 139 s, $13.90 list** in two items (72 s + 67 s) (so a failure in one half doesn't hold up the other).

## Hard limits
- **API spend ≤ $14.50 at list price in total** (item-01 ≤ $7.50, item-02 ≤ $7.00). Only the IDs listed in each item.
  No pod, no GPU, no upscale. A failed clip is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`. Do not touch `songs\rowboat\`.
- Never delete or overwrite a take or a review image: rename first.

## Protocol (markers in `queue\2026-10-02-butterfly-batch1\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Butterfly batch 1 done — ask Fable to review queue\2026-10-02-butterfly-batch1".
