# CC QUEUE — 2026-10-09 "Urulai gate 3": L05 rev 2.5 — K3 + ZK2 + ZK4 + ZK7 + ZO retake + I1 retake

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast (`arulps-beast`) · **Executor:** CC (Sonnet is fine) ·
**Manager:** Fable (frame-checks after).

Gate 2 verdict (`queue\2026-10-09-urulai-gate2\FABLE-VERDICT.md`):
- CA PASS.
- I1 failed: the children stood on the shelf, doll-sized (Arul agrees).
- ZO failed again, this time because of a second Cabbage.

Builder rev 2.5 changes only `shots\14_ZO.raw.txt` and `shots\01_I1.raw.txt`. Fable's checks: **LINT PASS 17/0/0**, and the other 15 shot files are unchanged.

This gate renders:
- the three remaining merged chorus+verse clips: **ZK2** (Okra), **ZK4** (Carrot), **ZK7** (Beans), 10 s each;
- **K3** (Tomato verse, 6 s);
- **ZO** (10 s);
- **I1** (11 s, restaged: camera on the shelf looking out, children standing on the floor).

Total 57 s, **$5.70 list**.

## Hard limits
- **API spend ≤ $5.80 at list price.** Only `K3,ZK2,ZK4,ZK7,ZO,I1`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`, `out/`, `tools/`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\`. Do not touch other songs.
- Move or rename, never delete. Do not edit any `shots\*.raw.txt` or `lint.json`. In `shots.csv`, change only the cells that
  item-01 step 1 names.
- **Do not touch the keepers** ZK1 and CA (`out\ZK1-*`, `out\CA-*`).

## Protocol (markers in `queue\2026-10-09-urulai-gate3\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $<x>`, tell Arul "Urulai gate 3 done — ask Fable to review queue\2026-10-09-urulai-gate3".
