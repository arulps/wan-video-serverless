# CC QUEUE — 2026-10-14 "Karadi rev 2.8 batch" (rebuilt for rev 2.3): the remaining 10 clips + ROUGH3 TA/EN cuts of the whole song

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

Arul approved the batch (14 Oct 16:54, "go ahead") and the rev 2.3 plan (17:52, "go ahead, but reduce the wastages"). Fable releases
this queue (writes READY) only after Gate B2 passed its review (`queue\2026-10-14-karadi-rev27b-gateB2\FABLE-VERDICT.md`). Renders
HKc, HKb, CAb, JOIN, V1Q, V2Q, V3Q, V4Q, O2, O3 (62 s — counted clips are 6 s since rev 2.3; CQb moved to Gate B2), then cuts the whole
song in both languages from `out\` — the first full cut of "the family trek".
**Spend: ≤ $6.30 list** (estimate $6.20). A12 stands at ≈$22.70 after Gate B2, cap $29.50.

## Hard limits
- **API spend ≤ $6.30 at list price. Only the 10 IDs above.** No pod, no GPU, no upscale. A failed row is reported, not re-run
  (the queue carries on with the other rows; the runner does that by itself).
- Never print `.env` values, keys, the workspace id or any URL (task ids are fine). Never touch RunPod. Commits carry `[skip ci]`;
  never commit `.env`, `out/`, `out_4k/`, `tools/`.
- **Move or rename, never delete or overwrite.** Old rev 1.x takes with the same name get `-v1-picnic` before rendering.
- Song folder: the builder writes its four files; CC writes only `_cuts\` new files (never overwrite ROUGH/ROUGH2) and `_cuts\_batch\`.
  **Do not run `song_cuts.py stage`** — the song folder still holds the picnic version's staged clips; cut straight from `out\` (`--src out`).
- Do not edit generated files or the runner (the runner's own status updates are fine).

## Protocol (markers in `queue\2026-10-14-karadi-rev28-batch\`)
As before; item-01 renders, item-02 cuts. After item-02: `QUEUE END <time> est $<x>`, tell Arul
"Karadi batch + ROUGH3 done — Fable will review queue\2026-10-14-karadi-rev28-batch".
