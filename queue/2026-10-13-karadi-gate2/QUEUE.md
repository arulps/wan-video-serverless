# CC QUEUE — 2026-10-13 "Karadi gate 2": A12 Karadi Mama rev 1.3 — O3 + V3Q + V2A + V4A

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast (`arulps-beast`) · **Executor:** CC (Sonnet is fine) ·
**Manager:** Fable (frame-checks after).
Gate 1b passed (Fable's verdict: `queue\2026-10-13-karadi-gate1b\FABLE-VERDICT.md`): CAa's spin-and-skip held its props through a
full turn, and in CQa the children's head tops are level within a quarter-head. Gate 2 tests the four hardest remaining shots:
- **O3** (7 s, 10 refs, the reference cap): everyone on-model, one bear walking away down the trail, Minmini exactly once;
- **V3Q** (6 s): five characters in a close group with exact counts, and the squirrel on Mintu's shoulder;
- **V2A** (6 s): exactly three tiny bees around the honeycomb;
- **V4A** (6 s): the bear and all four friends spin-and-skip together from ~2.5 s (Arul added it to the gate on 13 Oct).

Total 25 s, **$2.50 list**. Fable ran the runner's `--dry-run` for these four rows on a mirror: 4 rows, $2.50, no errors.

## Hard limits
- **API spend ≤ $2.60 at list price.** Only `O3,V3Q,V2A,V4A`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`, `out/`, `tools/`,
  `_to_delete/`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\`. Do not touch other songs.
- Do not edit generated files (`shots\*.raw.txt`, `shots.csv` except the runner's own status updates, `lint.json`, `scale.json`,
  `world.txt`, `characters.txt`, `refs\send\*`) or the runner. Move or rename, never delete. Keep CAa and CQa and their sheets as they are.

## Protocol (markers in `queue\2026-10-13-karadi-gate2\`)
As before: `LOG.md` start/done lines, `item-N.report.md`, `item-N.done`, or `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $<x>`, tell Arul "Karadi gate 2 done — Fable will review queue\2026-10-13-karadi-gate2".
