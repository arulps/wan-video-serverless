# CC QUEUE — 2026-10-14 "Karadi rev 2.6 Gate A retake": single-shot prompts (rev 2.2), re-render HKa + O1, sheets, slot cuts

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

Fable's Gate A verdict (`queue\2026-10-14-karadi-rev25-gateA3\FABLE-VERDICT.md`): HKa and O1 each came back as **three shots** (hard
cuts / a dissolve) because the prompts carried time ranges ("from about 0.4 to 1.1 seconds, …") — Wan 3.0's multi-shot storyboard
format. Amma and Appa only appeared in the last shot; in HKa the children watched instead of dancing. Builder **rev 2.2** fixes all 17
new prompts (single-shot line, no time ranges, the children dance with him in one row) and only resets a row to `todo` when its prompt
text changed. Fable's mirror: self-test OK, LINT PASS 21/0/0, dry-run $12.20, kept verse answers byte-identical, cut plan no gaps.
**Spend: ≤ $1.60 list** (HKa $0.80 + O1 $0.70), from the retake buffer Arul approved. A12 stands at $16.90 of the $29.50 cap.

## Hard limits
- **API spend ≤ $1.60 at list price. Only `HKa,O1`.** No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print `.env` values, keys, the workspace id or any URL (task ids are fine). Never touch RunPod. Commits carry `[skip ci]`;
  never commit `.env`, `out/`, `out_4k/`, `tools/`.
- **Move or rename, never delete or overwrite.**
- Song folder: the builder writes its four files; CC writes only `_cuts\_gateA2\` (new). Never touch the WAVs, `refs\`, `_previews\`,
  `_picnic-version\`, `_cuts\_gateA\`.
- Do not edit generated files or the runner (the runner's own status updates are fine).

## Protocol (markers in `queue\2026-10-14-karadi-rev26-gateA-retake\`)
As before. After item-01: `QUEUE END <time> est $<x>`, tell Arul "Karadi Gate A retake done — Fable will review queue\2026-10-14-karadi-rev26-gateA-retake".
