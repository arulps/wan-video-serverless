# CC QUEUE — 2026-10-06 "Butterfly cuts 3": Tamil timing fix — re-stage O3 + ROUGH3 cuts ($0, local ffmpeg)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (checks the cuts after).
Arul heard ROUGH2-TA ~2 s behind the audio (English was in sync). Fable re-measured the Tamil refrains by matching the English
refrain melody against the Tamil track: all 8 Tamil anchors were 2.15 s late. Builder rev 3.6 has the corrected anchors
(9.15 … 200.16); `cutplan.json` regenerated. The Tamil last line (O3) is now 6.7 s, so O3 is a 1.36x slow-down splice
(`out\O3-seed30313-w3-splice.mp4`, 204 frames). Plan test PASS, lint PASS 33/0/0.

## Hard limits
- **No API spend.** No pod, no GPU, no upscale, no render.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`, or anything under `out/`.
- In `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\` write **only** `32_O3_they-land-and-fall-asleep.mp4` and inside
  `_cuts\`. ROUGH and ROUGH2 cuts stay as they are. Do not touch `songs\rowboat\`.
- Never delete or overwrite any take in `songs\a07-butterfly\out\`.

## Protocol (markers in `queue\2026-10-06-butterfly-cuts3\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-01: `QUEUE END <time>`, tell Arul "Butterfly ROUGH3 cuts done — ask Fable to review queue\2026-10-06-butterfly-cuts3".
