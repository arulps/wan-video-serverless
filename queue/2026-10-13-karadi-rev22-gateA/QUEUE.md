# CC QUEUE — 2026-10-13 "Karadi rev 2.2 Gate A": the quick spin-and-skip with the children (HKa) + the arrival at his home (O1)

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

First render of "the family trek" (plan `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\KARADI-MAMA-WALK-HOME-PLAN.md` v1.1,
passes `KARADI-MAMA-DIRECTOR-AUDIENCE-PASS-REV20.md`). Gate A = the two riskiest clips: **HKa** — Karadi Mama's quick full turn with
props, Mintu and Minnu dancing it with him (the song's signature moment; Arul: "no compromise") — and **O1** — seven characters at the
new place (his home, with the set plate). Fable's mirror: LINT PASS 21/0/0, dry-run $12.20 for all 17, these two = **$1.50**.
**Spend: ≤ $1.60 list.** Song cap in `A12-WATCH.md` is now $29.50 (Arul, 13 Oct).

## Hard limits
- **API spend ≤ $1.60 at list price. Only `HKa,O1`.** No pod, no GPU, no upscale. A failure is reported, not re-run. Never retry a render.
- Never print `.env` values, keys, the workspace id or any URL. Never touch RunPod. Commits carry `[skip ci]`; never commit `.env`,
  `out/`, `out_4k/`, `tools/`.
- **Move or rename, never delete or overwrite.** Never overwrite a take, a staged clip or a cut.
- Song folder `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\`: write only into `_cuts\_gateA\` (new). Never touch the WAVs,
  `refs\`, `_gen\`, `_previews\` or the runsheet files.
- Do not edit generated files (`shots\*.raw.txt`, `shots.csv` except the runner's own status updates, `lint.json`, `scale.json`,
  `characters.txt`, `refs\send\*`) or the runner.

## Protocol (markers in `queue\2026-10-13-karadi-rev22-gateA\`)
As before: `LOG.md` start/done lines, `item-N.report.md`, `item-N.done`, or `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $<x>`, tell Arul "Karadi Gate A done — Fable will review queue\2026-10-13-karadi-rev22-gateA".
