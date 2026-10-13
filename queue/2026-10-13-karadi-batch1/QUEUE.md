# CC QUEUE — 2026-10-13 "Karadi batch 1": A12 Karadi Mama rev 1.4 — the 13 remaining clips

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast (`arulps-beast`) · **Executor:** CC (Sonnet is fine) ·
**Manager:** Fable (frame-checks after).
Gates passed (Fable's verdicts in `queue\2026-10-13-karadi-gate1b\` and `queue\2026-10-13-karadi-gate2\`): CAa, CQa, O3, V3Q and V4A
are kept. The service refused V2A on its IP check, so builder **rev 1.4** re-stages it as a two-shot with Mintu. Only
`shots\11_V2A.raw.txt` and V2A's `shots.csv` row changed, and the done/failed status cells were kept.
This batch renders everything left, in story order:
- I1, HKa, HKb, CQb, CAb;
- V1Q, V1A, V2Q, V2A, V3A, V4Q;
- O1, O2.

That is 13 clips, 89 s, **$8.90 list**. Fable ran lint (18/0/0) and the runner's `--dry-run` on these 13 rows on a mirror: 13 rows,
$8.90, no errors.

## Hard limits
- **API spend ≤ $9.00 at list price.** Only the 13 IDs below. No pod, no GPU, no upscale. A failure is reported, not re-run, and the
  batch carries on with the remaining clips (the runner's normal behaviour).
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`, `out/`, `tools/`,
  `_to_delete/`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\`. Do not touch other songs.
- Do not edit generated files (`shots\*.raw.txt`, `shots.csv` except the runner's own status updates, `lint.json`, `scale.json`,
  `world.txt`, `characters.txt`, `refs\send\*`) or the runner. Move or rename, never delete. Keep the five kept clips and their sheets.

## Protocol (markers in `queue\2026-10-13-karadi-batch1\`)
As before: `LOG.md` start/done lines, `item-N.report.md`, `item-N.done`, or `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $<x>`, tell Arul "Karadi batch 1 done — Fable will review queue\2026-10-13-karadi-batch1".
