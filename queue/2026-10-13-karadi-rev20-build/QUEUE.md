# CC QUEUE — 2026-10-13 "Karadi rev 2.0 build": the family-trek runsheet onto Beast, lint + dry-run + cut plan, commit (no API spend)

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

Arul approved the re-plan (13 Oct 22:18): A12 becomes **"the family trek"** — see
`C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\KARADI-MAMA-WALK-HOME-PLAN.md` (v1.1) and the written passes in
`KARADI-MAMA-DIRECTOR-AUDIENCE-PASS-REV20.md`. Fable rewrote the builder (`_gen\build_karadi_runsheet.py` rev 2.0) and verified it on an
exact mirror: self-test OK (place / facing / word-action / pacing / camera rules each refuse a bad clip), LINT PASS 21/0/0, runner
dry-run 17 todo rows **$12.20** list, the 4 kept verse answers byte-identical and still `done`, cut plan TA 29 / EN 24 slots with no gaps.
This queue reproduces that on Beast and commits. **API spend: $0.00.** No render, no pod, no upscale.

## Hard limits
- No API calls. Never print `.env` values, keys, the workspace id or any URL.
- Song folder `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\`: the builder writes `KARADI-MAMA-WAN3-RUNSHEET.md`,
  `karadi-shots.json`, `_gen\scale.json`, `_gen\lint.json` — nothing else there. Never touch the WAVs, `refs\`, `_cuts\`, `_previews\`.
- Repo: the builder writes `songs\a12-karadi-w3\` (shots.csv, shots\*.raw.txt, lint.json, scale.json, world.txt, characters.txt,
  refs\send\*.jpg) and `make_cutplan.py` writes `cutplan.json`. **Do not touch `out\`** (the current takes stay where they are; Gate A
  renames them). Move or rename, never delete.
- Commits carry `[skip ci]`. Never commit `.env`, `out/`, `out_4k/`, `tools/`.

## Protocol (markers in `queue\2026-10-13-karadi-rev20-build\`)
As before: `LOG.md` start/done lines, `item-N.report.md`, `item-N.done`, or `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $0.00`, tell Arul "Karadi rev 2.0 build done — Fable will review queue\2026-10-13-karadi-rev20-build".
