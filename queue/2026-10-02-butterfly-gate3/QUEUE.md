# CC QUEUE — 2026-10-02 "Butterfly gate 3": A07 Butterfly rev 3.4 — new relaxed Mintu/Minnu refs: RA again + V2b + V5a

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Arul made relaxed-arms refs for Mintu and Minnu (the T-pose refs leaked: V2a frame 0 was Minnu's ref pose pasted in).
`refs\01-mintu-front.jpg` and `refs\02-minnu-front.jpg` are replaced (song folder + repo; old ones in the song folder's
`refs\_old\`). Rev 3.4 prompt review (Row Row + gate learnings): new Mintu/Minnu lines; no camera move that can drop the kids out
of frame (I2, V1d, V3a, V6c, V6d); "framing never changes" on every still shot; background kids "clearly visible"; mothers on
the bench from frame 0 in I1. Fable's checks: LINT PASS 33/0/0, plan test PASS, checklist 33/33.
This gate checks the new refs before the 29-clip batch: **RA (8 s, 4 kids + mothers), V2b (5 s, Minnu + Priya close),
V5a (5 s, all 4 kids + 4 butterflies = 8 refs) = 18 s, $1.80 list.** RA status cell cleared for the redo.

## Hard limits
- **API spend ≤ $2.00 at list price.** Only `RA,V2b,V5a`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`. Do not touch `songs\rowboat\`.
- Never delete or overwrite a take or a review image: rename first (step 1).

## Protocol (markers in `queue\2026-10-02-butterfly-gate3\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $<x>`, tell Arul "Butterfly gate 3 done — ask Fable to review queue\2026-10-02-butterfly-gate3".
