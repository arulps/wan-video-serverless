# CC QUEUE — 2026-10-09 "Urulai gate 4": L05 rev 2.6 — the last nine clips (Z3, Z5, Z6, K5, K6, SA, SB, CB, O2)

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast (`arulps-beast`) · **Executor:** CC (Sonnet is fine) ·
**Manager:** Fable (frame-checks after).

Gate 3 verdict (`queue\2026-10-09-urulai-gate3\FABLE-VERDICT.md`):
- **Keep:** ZK2, ZK4, ZK7, K3, I1.
- **Failed:** ZO (it's not in this gate; Arul decides on a retake).

Arul's decisions (9 Oct, 15:47–15:55):
- keep CB;
- trim SA and SB to **7 s**;
- song budget **$18.00 list** (`queue\L05-WATCH.md` already says so).

The prompts for these nine clips are already on Beast (O2 has the rev 2.6 "children on the kitchen floor" wording). The only change
`shots.csv` needs is the two SA/SB duration cells (item-01 step 1).

This gate renders:
- **Z3, Z5, Z6** (6 s each): chorus, Baby Potato falls asleep in Tomato's, Radish's and Cabbage's baskets.
- **K5, K6** (6 s each): Radish tugs the cloth away; Cabbage flops a leaf over Baby Potato.
- **SA, SB** (7 s each): Amma searches.
- **CB** (8 s): Amma kisses and tickles Baby Potato.
- **O2** (6 s): Mintu and Minnu say "shh".

Total 58 s, **$5.80 list**.

## Hard limits
- **API spend ≤ $5.90 at list price.** Only `Z3,Z5,Z6,K5,K6,SA,SB,CB,O2`. No pod, no GPU, no upscale. A failure is reported, not
  re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`, `out/`, `tools/`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\`. Do not touch other songs.
- Move or rename, never delete. Do not edit any `shots\*.raw.txt` or `lint.json`. In `shots.csv`, change only the cells that
  item-01 step 1 names.
- **Do not touch the keepers:** ZK1, ZK2, ZK4, ZK7, K3, CA, I1 (`out\` files for those IDs). Leave every ZO file as it is.

## Protocol (markers in `queue\2026-10-09-urulai-gate4\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $<x>`, tell Arul "Urulai gate 4 done — ask Fable to review queue\2026-10-09-urulai-gate4".
