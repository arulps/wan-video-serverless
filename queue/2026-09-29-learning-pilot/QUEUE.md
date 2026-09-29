# CC QUEUE — 2026-09-29 "Learning pilot": 5 learning Shorts + L04 elbow sneeze on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Arul's decisions 2026-09-29: learning set without animals first; colours and fruits object-only (no ref); vegetables keep the
kids; audio on = soft music + off-screen English voice at the runsheet marks; pilot of 5; L04 sneeze into the elbow.
Fable wrote `songs\shorts-learning\` (generator `_make_shots.py`, 72 shot files, worlds, characters.txt, refs, shots.csv) and
`songs\shorts-loops\shots\L04-w3d.txt` + row `L04_w3d`.

Pilot rows: `C1_w3` (red ball, object only), `F3_w3` (apple, object only), `FD1_w3` (Mintu idli), `AC2_w3` (Minnu clap),
`V2_w3` (auto rickshaw, new street world) — plus `L04_w3d` in shorts-loops.

## Hard limits
- **API spend ≤ $3.20 at list price** (estimate $3.00: 6 × 5 s × $0.10). No pod, no GPU, no upscale.
- Only these 6 rows; no extra seeds; failures are reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do not touch the `<ID>-metadata.md` files in `renders-learning\` or anything in `renders\L04\` except adding new files.

## Protocol (markers in `queue\2026-09-29-learning-pilot\`)
As in `queue\2026-09-28-shorts-retakes1`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Learning pilot done — ask Fable to review queue\2026-09-29-learning-pilot".
