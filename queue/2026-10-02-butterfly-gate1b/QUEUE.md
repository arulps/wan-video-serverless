# CC QUEUE — 2026-10-02 "Butterfly gate 1b + 2": A07 Butterfly rev 3.2 — RA again (new Priya ref) + RB, V1a, V2a on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Gate 1 RA came out with Priya ~1.4× taller than Minnu — Wan copied the long-legged turnaround model's proportions. Arul made a
toddler-proportioned Priya; it is now `refs\08-priya-front.jpg` (song folder and repo; the old one is in the song folder's
`refs\_old\`). Prompts updated (dark-brown hair, yellow stars, freckles), runsheet rev 3.2. RA status cell cleared for the redo.
Fable's checks: `prompt_lint` LINT PASS 33/0/0, `test_song_cuts_reuse --plan-only` PASS.
Renders **RA (8 s), RB (8 s), V1a (5 s), V2a (5 s) = 26 s, $2.60 list.** V2a (Priya + Minnu) is the real height test.

## Hard limits
- **API spend ≤ $2.80 at list price.** Only `RA,RB,V1a,V2a`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`. Do not touch `songs\rowboat\`.
- Never delete or overwrite a take: the old RA is renamed first (step 1), not removed.

## Protocol (markers in `queue\2026-10-02-butterfly-gate1b\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $<x>`, tell Arul "Butterfly gate 1b done — ask Fable to review queue\2026-10-02-butterfly-gate1b".
