# CC QUEUE — 2026-10-14 "Karadi rev 2.7 Gate B": the encounter (CQ0), the children's question (CQa), his answer (CAa), the long shot (I1)

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

Gate A passed on the retake (`queue\2026-10-14-karadi-rev26-gateA-retake\FABLE-VERDICT.md`). The builder now carries HKa's measured trim
(plays from 1.33 s) and O1's measured key window; no prompt changed, so HKa and O1 stay `done`. Gate B renders the next four planned clips.
**Spend: ≤ $3.20 list** (CQ0 $0.80, CQa $0.80, CAa $0.80, I1 $0.70). A12 stands at $18.40 of the $29.50 cap.

## Hard limits
- **API spend ≤ $3.20 at list price. Only `CQ0,CQa,CAa,I1`.** No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print `.env` values, keys, the workspace id or any URL (task ids are fine). Never touch RunPod. Commits carry `[skip ci]`;
  never commit `.env`, `out/`, `out_4k/`, `tools/`.
- **Move or rename, never delete or overwrite.** If `out\` holds an old take with the same name, rename it with `-v1-picnic` before rendering.
- Song folder: the builder writes its four files; CC writes only `_cuts\_gateB\` (new).
- Do not edit generated files or the runner (the runner's own status updates are fine).

## Protocol (markers in `queue\2026-10-14-karadi-rev27-gateB\`)
As before. After item-01: `QUEUE END <time> est $<x>`, tell Arul "Karadi Gate B done — Fable will review queue\2026-10-14-karadi-rev27-gateB".
