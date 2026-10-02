# CC QUEUE — 2026-10-02 "Butterfly gate 1": A07 Butterfly rev 3.1, clip RA only (the refrain look-lock) on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Source: `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\BUTTERFLY-WAN3-RUNSHEET.md` rev 3.1 (33 clips, 175 s; one sunny park,
Mintu + Minnu + Leo + Priya, the two mothers on a bench far behind). Fable built `songs\a07-butterfly\` from the runsheet's
`butterfly-shots.json` (`_make_butterfly.py`: 10 refs, 33 verbatim prompts `shots\NN_ID.raw.txt`, `shots.csv` 1280x720 audio off,
`cutplan.json` = 47 Tamil / 48 English slots, re-used clips RA/RB/CH3 with their own trim points, hard cuts) and `lint.json`.
`comfy\song_cuts.py` now sorts slots per language and stages a re-used clip once; new test `tests\test_song_cuts_reuse.py`.
Fable's checks: `prompt_lint` LINT PASS 33/0/0, `test_prompt_lint` PASS, `test_song_cuts_reuse --plan-only` PASS.
This queue renders only the gate clip **RA** (8 s, 6 refs); the rest waits for Fable's check.

## Hard limits
- **API spend ≤ $0.90 at list price.** Only `RA`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\` (the stand-in test only reads its WAVs).
- Do not touch `songs\rowboat\` (read-only use by the regression test).

## Protocol (markers in `queue\2026-10-02-butterfly-gate1\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Butterfly gate 1 done — ask Fable to review queue\2026-10-02-butterfly-gate1".
