# CC QUEUE — 2026-10-02 "Butterfly cuts": stage numbered clips + Tamil and English rough cuts ($0, local ffmpeg)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (checks the cuts after).
All 33 clips are in. Instead of retakes, Arul chose splices (2 Oct evening); Fable built them with
`songs\a07-butterfly\_splices.py` → `out\<ID>-seed30313-w3-splice.mp4` for V2b, V2c, V3a, V6b, V1c (V2a's splice is from
earlier). Each was frame-checked and covers its longest slot; `cutplan.json` now points to them. V3c, V3d, V4d, V5a are kept
as rendered (Arul). Plan test PASS.

## Hard limits
- **No API spend.** No pod, no GPU, no upscale, no render.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`, or anything under `out/`.
- In `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\` write **only** the staged numbered clips (`NN_ID_slug.mp4`) and
  inside `_cuts\`. Do not touch `songs\rowboat\`.
- Never delete or overwrite any take in `songs\a07-butterfly\out\`.

## Protocol (markers in `queue\2026-10-02-butterfly-cuts\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-01: `QUEUE END <time>`, tell Arul "Butterfly rough cuts done — ask Fable to review queue\2026-10-02-butterfly-cuts".
