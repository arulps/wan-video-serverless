# CC QUEUE — 2026-10-01 "Rowboat W2 retakes + W3–W6 (all remaining shots)": L04 Row Row Row Your Boat on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Fable reviewed queue 2026-10-01-rowboat-w1fix-w2: V1b, V2a, V2b, V2c, V2d, X1b, V3c pass. Two retakes:
V3a (the lion in the grass was an invented lion, not Singa → now gets Singa's ref, pack FAM+LION, mane stays hidden) and
V3b ("toward the boat just off-screen" drew an empty sailboat → gaze described instead; same fix pre-applied to V4b, V5b, V6a).
Prompt lint extended (animal aliases, off-screen-object warning). Old takes kept as `out\<ID>-seed30313-w3-v1-<reason>.mp4`.
This queue renders **V3a,V3b,X2a,X2b,V4a,V4b,V4c,X3a,X3b,V5a,V5b,V5c,V6a,V6b,V6c,V6d,T1** — 2 retakes (9 s) + the rowing dance, splash/spin, the snow world with Pani Karadi, and the
animal friends' wave (37 s) + the secret channel with Chiku and the sunset finale (28 s) — every remaining
shot of the song. Est **$7.40** list (74 s).

## Hard limits
- **API spend ≤ $8.00 at list price.** Only the 17 shots above. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\`.
- Do not delete, overwrite or re-render any clip whose status is `done` or any `*-v1-*` file.

## Protocol (markers in `queue\2026-10-01-rowboat-w2fix-w3w4\`)
As in `queue\2026-10-01-rowboat-w1fix-w2`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Rowboat all remaining shots done — ask Fable to review queue\2026-10-01-rowboat-w2fix-w3w4".
