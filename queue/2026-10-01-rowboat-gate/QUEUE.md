# CC QUEUE — 2026-10-01 "Rowboat gate": L04 Row Row Row Your Boat, shot V1a only (look-lock) on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Source: `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\ROWBOAT-WAN3-RUNSHEET.md` rev 2 (29 shots).
Fable built `songs\rowboat\` from the runsheet's own builder data (`_make_rowboat.py`: refs, 29 verbatim prompts
`shots\NN_ID.raw.txt`, `shots.csv` 1280x720 audio off, `cutplan.json`), added verbatim-prompt support to the runner
(`comfy\batch_runner.py`: a `*.raw.txt` shot file is sent as-is) and the cut builder `comfy\song_cuts.py` (tested with stand-in
clips: both cuts land every shot in its slot, lengths 123.760 / 96.920 s). Mock test `tests\test_wan3_mock.py` PASS.
This queue renders only the gate shot **V1a** (6 s); the rest waits for Fable's check. Dry-run by Fable: V1a $0.60.

## Hard limits
- **API spend ≤ $0.70 at list price.** Only `V1a`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\` (master copy stays untouched
  until the staging step later).

## Protocol (markers in `queue\2026-10-01-rowboat-gate\`)
As in `queue\2026-09-28-shorts-retakes1`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Rowboat gate done — ask Fable to review queue\2026-10-01-rowboat-gate".
