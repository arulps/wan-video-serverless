# CC QUEUE — 2026-10-02 "Butterfly gate 2b": A07 Butterfly rev 3.3 — retake V2a on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Gate 1b review (Fable): RA approved; RB usable (it opens on ~0.5 s of empty park → its trim points now start at ≥ 1.0 s);
V1a kept (Arul, 2 Oct: no retake). V2a needs a retake:
- V2a: opened on 1.5 s of empty park before the girls appeared; Priya still ~20% taller than Minnu.
Fixes in rev 3.3 (all 33 prompts): every child is in frame from the first frame (except I1, where they run in); a butterfly
never looks bigger than a child's head; Priya/Minnu height stated as "top of Priya's head level with the top of Minnu's head";
V1a rewritten (hovers above the roses, framing never changes). Fable's checks: LINT PASS 33/0/0, plan test PASS.
Renders **V2a only (5 s), $0.50 list.** V2a status cell cleared for the redo; V1a stays `done` (its prompt file now holds the
rev 3.3 wording, the kept take was made from the rev 3.2 wording — its sidecar has the exact prompt).

## Hard limits
- **API spend ≤ $0.60 at list price.** Only `V2a`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`. Do not touch `songs\rowboat\`.
- Never delete or overwrite a take or a review image: rename first (step 1).

## Protocol (markers in `queue\2026-10-02-butterfly-gate2b\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $<x>`, tell Arul "Butterfly gate 2b done — ask Fable to review queue\2026-10-02-butterfly-gate2b".
