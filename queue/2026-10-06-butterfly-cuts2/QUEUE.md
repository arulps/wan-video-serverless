# CC QUEUE — 2026-10-06 "Butterfly cuts 2": re-stage 3 spliced clips + Tamil and English ROUGH2 cuts ($0, local ffmpeg)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (checks the cuts after).
Arul's review of ROUGH-TA (6 Oct): at 0:35 (V1b) and 2:05 (V4b) two butterflies fly in and merge into one; at ~2:00 (V4a) the
big leaf floats in mid-air. Fable spliced all three (no renders): `songs\a07-butterfly\out\V1b|V4a|V4b-seed30313-w3-splice.mp4`,
recipes in `_splices.py`, frame-checked, each covers its longest slot; `cutplan.json` points to them. Learnings §10 updated.

## Hard limits
- **No API spend.** No pod, no GPU, no upscale, no render.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`, or anything under `out/`.
- In `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\` write **only** the three re-staged numbered clips and inside `_cuts\`.
  The ROUGH (v1) cuts stay as they are. Do not touch `songs\rowboat\`.
- Never delete or overwrite any take in `songs\a07-butterfly\out\`.

## Protocol (markers in `queue\2026-10-06-butterfly-cuts2\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-01: `QUEUE END <time>`, tell Arul "Butterfly ROUGH2 cuts done — ask Fable to review queue\2026-10-06-butterfly-cuts2".
