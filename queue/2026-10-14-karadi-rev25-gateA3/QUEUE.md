# CC QUEUE — 2026-10-14 "Karadi rev 2.5 Gate A (3rd issue)": render HKa, sheets for HKa + O1, slot cuts with the music

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

`2026-10-13-karadi-rev23-gateA2` recovered O1 for $0 (item-01) and then blocked correctly at item-02: HKa's `shots.csv` status was
`failed` (set by gate A's runner), the item expected `todo`, and the runner skips `failed` rows without `--retry-failed`. Fable's
error. This queue renders HKa with `--retry-failed` (with `--only HKa` it can select nothing else), then makes the sheets and the slot
cuts for both gate clips. Client change since gate A2 (CC's note): a submit is now resubmitted only if the connection was never
opened (refused/DNS); a drop during or after the upload is reported, never resubmitted — no double pay. Mock test now 10 checks.
**Spend: ≤ $0.90 list** (HKa $0.80). A12 stands at $16.10 of the $29.50 cap.

## Hard limits
- **API spend ≤ $0.90 at list price. Only `HKa`.** No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print `.env` values, keys, the workspace id or any URL (task ids are fine). Never touch RunPod. Commits carry `[skip ci]`;
  never commit `.env`, `out/`, `out_4k/`, `tools/`.
- **Move or rename, never delete or overwrite.**
- Song folder: write only into `_cuts\_gateA\`. Never touch the WAVs, `refs\`, `_gen\`, `_previews\`, `_picnic-version\` or the runsheet files.
- Do not edit generated files or the runner (the runner's own status updates in `shots.csv` are fine).

## Protocol (markers in `queue\2026-10-14-karadi-rev25-gateA3\`)
As before. After item-01: `QUEUE END <time> est $<x>`, tell Arul "Karadi Gate A done — Fable will review queue\2026-10-14-karadi-rev25-gateA3".
