# CC QUEUE — 2026-09-28 "Shorts batch 1": YT loop Shorts L02–L20 on Wan 3.0 (one version each)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks when Arul asks).
Source: `C:\Channel Contents\MinMiniKids\YT Shorts\LOOP-SHORTS-RUNSHEET.md` (scenes) → `songs/shorts-loops/` (Fable wrote the
19 shot files `shots/Lxx-w3.txt`, 5 world files, Amma/Thatha/Paati lock lines, 4 new 9:16 refs, 19 rows `Lxx_w3` in shots.csv).
Arul's decisions: Wan 3.0 only, **720p, no upscale** for Shorts, **one version** per Short (English sound: SFX, at most a
short word, soft xylophone/ukulele music; Arul re-voices other languages in CapCut).

## Hard limits
- **API spend ≤ $10.50 at list price** for the whole queue (estimate $9.70 list, ~$6.80 with the 30% discount). No pod, no GPU, no upscaling.
- No retakes / extra seeds / "one more try" — only the 19 rows. Failed rows are reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv` (the runner edits status cells). Commits carry `[skip ci]`.

## Protocol (markers in `queue\2026-09-28-shorts-batch1\`)
Items run back to back. For item N: append `[<time>] item-N start` to LOG.md → do it → write `item-N.report.md` → create
`item-N.done`. On a failed check: `item-N.blocked`, a line in LOG.md, stop. After item-02: `QUEUE END <time> est $<x>` in
LOG.md and tell Arul "Shorts batch 1 done — ask Fable to review queue\2026-09-28-shorts-batch1".
