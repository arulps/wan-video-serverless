# CC QUEUE — 2026-10-01 "Rowboat final": 2 retakes + Tamil/English rough cuts — L04 Row Row Row Your Boat

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Fable reviewed queue 2026-10-01-rowboat-w2fix-w3w4: 15 of 17 pass. Two retakes:
- **T1** (sunset tail): "three small silhouettes" with no refs came back as three invented people in blue/pink → family refs
  + "Appa, Mintu and Minnu small in it, seen from behind, Appa rowing gently" + the only-Appa-rows line.
- **V5c** (squeak): the "mouse faces" came back worried, hands over mouths → big cheeky grins, hands never cover the mouth.
Old takes kept as `out\<ID>-seed30313-w3-v1-<reason>.mp4`. Est **$0.70** list (7 s).
Then item-03 builds the first full **rough cuts** (Tamil + English) from the chosen takes, with `comfy\song_cuts.py` ($0).
V2d's chosen take is Fable's hand-built `out\V2d-seed30313-w3-splice2.mp4` (in `cutplan.json`) — that is intended.

## Hard limits
- **API spend ≤ $1.00 at list price.** Only `T1,V5c`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- In `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\` write **only** inside `_cuts\` (item-03). Nothing else
  in that folder is touched.
- Do not delete, overwrite or re-render any clip whose status is `done` or any `*-v1-*` / `*-splice*` file.

## Protocol (markers in `queue\2026-10-01-rowboat-final\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-03: `QUEUE END <time> est $<x>`, tell Arul "Rowboat final done — rough cuts are in the song folder's _cuts; ask Fable to review queue\2026-10-01-rowboat-final".
