# CC QUEUE — 2026-09-28 "Shorts retakes 2": L04 sneeze, hands-over-nose version (Wan 3.0)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Fable's frame check of retakes 1: L04_w3b still shows a white mark under Minnu's nose around 0.8–2.2 s. New approach:
she covers her nose and mouth with both hands for the sneeze. Fable wrote `shots/L04-w3c.txt` and the row `L04_w3c`
(seed 4242) in shots.csv. Dry-run checked by Fable: 1 row, `audio=on`, estimated $0.50.

## Hard limits
- **API spend ≤ $0.60 at list price.** No pod, no GPU, no upscaling. Only this row; no extra seeds; a failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore `shots.csv`. Commits carry `[skip ci]`.
- Do not touch `Lxx-metadata.md` files or any existing clip in `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L04\`.

## Protocol (markers in `queue\2026-09-28-shorts-retakes2\`)
Same as queue `2026-09-28-shorts-retakes1`: LOG.md line per item start/done, `item-N.report.md`, `item-N.done`,
`item-N.blocked` + stop on a failed check. After item-02: `QUEUE END <time> est $<x>` and tell Arul
"Shorts retakes 2 done — ask Fable to review queue\2026-09-28-shorts-retakes2".
