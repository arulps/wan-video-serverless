# CC QUEUE — 2026-10-01 "Rowboat V5c": one retake + rebuild both rough cuts — L04 Row Row Row Your Boat

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Arul spotted it in the rough cut: in V5c ("squeak") Minnu has a pink mouse nose and drawn-on whiskers — "pretend to be tiny
cheeky mice" put the animal's features on her face. Fable rewrote the beat (mouse pose with the hands only; "faces stay
exactly their own: no whiskers, no animal nose, no face paint") and added a lint warning for this pattern.
Old take kept as `out\V5c-seed30313-w3-v2-mouse-nose.mp4`. Est **$0.40** list (4 s). Then both rough cuts are rebuilt ($0).

## Hard limits
- **API spend ≤ $0.50 at list price.** Only `V5c`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- In `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\` write **only** inside `_cuts\`.
- Do not delete, overwrite or re-render any clip whose status is `done` or any `*-v1-*` / `*-v2-*` / `*-splice*` file.

## Protocol (markers in `queue\2026-10-01-rowboat-v5c\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Rowboat V5c done — rough cuts rebuilt; ask Fable to review queue\2026-10-01-rowboat-v5c".
