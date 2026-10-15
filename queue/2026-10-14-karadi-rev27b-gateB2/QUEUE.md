# CC QUEUE — 2026-10-14 "Karadi rev 2.3 Gate B2": CAa retake + CQb at 6 s (the pacing test)

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

Gate B (`queue\2026-10-14-karadi-rev27-gateB\FABLE-VERDICT.md`): I1, CQ0 and CQa passed; CAa failed (Amma pops in at f50, then turns into
Appa). Gate B also showed that Wan 3.0 spreads a counted action chain over the whole clip, so builder **rev 2.3** renders counted clips
at **6 s** (not 8 s). This gate tests that on the two clips the batch depends on: **CAa** (the retake, with the parents' fix) and **CQb**
(the children's 8-count question at the upper stop). Both are needed clips, so nothing here is extra spend. Arul approved, 14 Oct 17:52
("go ahead, but make sure to reduce the wastages").
**Spend: ≤ $1.20 list** (CAa 6 s $0.60 + CQb 6 s $0.60). A12 stands at $21.50 of the $29.50 cap.

## Hard limits
- **API spend ≤ $1.20 at list price. Only `CAa,CQb`.** No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print `.env` values, keys, the workspace id or any URL (task ids are fine). Never touch RunPod. Commits carry `[skip ci]`;
  never commit `.env`, `out/`, `out_4k/`, `tools/`.
- **Move or rename, never delete or overwrite.** The failed CAa take is renamed before rendering (item-01 step 2).
- Song folder: the builder writes its four files; CC writes only `_cuts\_gateB2\` (new).
- Do not edit generated files, the builder or the runner (the runner's own status updates are fine).

## Protocol (markers in `queue\2026-10-14-karadi-rev27b-gateB2\`)
As before. After item-01: `QUEUE END <time> est $<x>`, tell Arul "Karadi Gate B2 done — Fable will review queue\2026-10-14-karadi-rev27b-gateB2".
