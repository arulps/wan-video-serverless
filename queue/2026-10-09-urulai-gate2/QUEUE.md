# CC QUEUE — 2026-10-09 "Urulai gate 2": L05 rev 2.4 — ZO retake + CA + I1

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast (`arulps-beast`) · **Executor:** CC (Sonnet is fine) ·
**Manager:** Fable (frame-checks after).
Gate 1c verdict (`queue\2026-10-09-urulai-gate1c\FABLE-VERDICT.md`): **ZK1 PASS, keep.** ZO failed because two Brinjals had faces.
Builder rev 2.4 changes only `shots\14_ZO.raw.txt`: no plain brinjals in the big basket, and Baby Potato's spot is now at the left end
of the front row. Fable's checks: **LINT PASS 17/0/0**, `test_prompt_lint` PASS, and the other 16 shot files are byte-identical.
This gate: **ZO (10 s) + CA (8 s, Amma cuddles Baby Potato) + I1 (11 s, intro with the children) = 29 s, $2.90 list.**

## Hard limits
- **API spend ≤ $3.00 at list price.** Only `ZO,CA,I1`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`, `out/`, `tools/`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\`. Do not touch other songs.
- Move or rename, never delete. Do not edit any `shots\*.raw.txt` or `lint.json`. In `shots.csv`, change only the cells that
  item-01 step 1 names.
- **Do not touch ZK1** (`out\ZK1-seed30313-w3.*` is the keeper).

## Protocol (markers in `queue\2026-10-09-urulai-gate2\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $<x>`, tell Arul "Urulai gate 2 done — ask Fable to review queue\2026-10-09-urulai-gate2".
