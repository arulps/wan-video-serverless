# CC QUEUE — 2026-09-29 "Learning batch 1": 69 non-animal learning Shorts (incl. C1/F3 with the kids) on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Pilot (queue 2026-09-29-learning-pilot) passed Fable's check: all 5 templates + voice timing good. This queue renders every
remaining row in `songs\shorts-learning\shots.csv` (animals A1–A6 are not in the file yet). Dry-run by Fable: 69 rows, $34.50.
**Change 2026-09-29 09:15:** colours and fruits now keep Minnu/Mintu as in the runsheet (Arul); C1 and F3 are re-rendered with
the kids. The pilot's object-only C1/F3 files were renamed `*-objectonly` — keep them, do not delete or overwrite.

## Hard limits
- **API spend ≤ $36.00 at list price** (estimate $34.50; ~$24.15 with the 30% discount). No pod, no GPU, no upscale.
- Only these 69 rows; no extra seeds; failed rows are reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do not touch the `<ID>-metadata.md` files in `renders-learning`; only add files.

## Protocol (markers in `queue\2026-09-29-learning-batch1`)
As in `queue\2026-09-28-shorts-retakes1`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Learning batch 1 done — ask Fable to review queue\2026-09-29-learning-batch1".
