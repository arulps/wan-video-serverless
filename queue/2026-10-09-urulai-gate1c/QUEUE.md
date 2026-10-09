# CC QUEUE — 2026-10-09 "Urulai gate 1c": L05 rev 2.3 — ZK1 + ZO with SLEEPING owner refs

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.
gate1b: ZK1 rendered (timing, merge, plain-vegetable faces all pass) but Brinjal's eyes stayed open all 10 s — the awake reference
wins over "closed eyes" in the prompt, so it read as Brinjal doing it on purpose (breaks Arul's "nobody is mean" rule). ZO failed
at upload (~25 MB of PNG refs as data URIs, write timeout, no task id).
Rev 2.3 fixes both: the seven owners use **sleeping refs** (`refs\1?-*-asleep.png`, eyes closed, Arul's Gemini images 9 Oct) in
every shot where they sleep, with "eyes closed in sleep" descriptions; every clip now sends **JPEG copies** from `refs\send\`
(ZO ~2 MB). Fable's checks: LINT PASS 17/0/0, `test_prompt_lint` PASS, full dry-run est $13.50, no errors.
This gate re-renders **ZK1 (10 s) + ZO (10 s) = 20 s, $2.00 list.** gate1b's ZK1 take is kept for the record (step 1).

## Hard limits
- **API spend ≤ $2.10 at list price.** Only `ZK1,ZO`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`, `out/`, `tools/`, `_to_delete/`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\`. Do not touch other songs.
- Do not edit generated files (`shots\*.raw.txt`, `shots.csv`, `lint.json`, `world.txt`, `characters.txt`, `refs\send\*`) or the runner.
- Move/rename, never delete.

## Protocol (markers in `queue\2026-10-09-urulai-gate1c\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $<x>`, tell Arul "Urulai gate 1c done — Fable will review".
