# CC QUEUE — 2026-10-13 "Karadi restage 1": A12 rev 1.5 — V1A, V2A, V3A, V4A in new places + ROUGH2 cuts

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.
Arul (13 Oct): "the background is so static across all frames". Fable's director and audience pass
(`C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\KARADI-MAMA-DIRECTOR-AUDIENCE-PASS.md`) moves the four verse answers to
where the lyric points, with no set image and a slow tracking camera:
- V1A: the open meadow under a big sky;
- V2A: the bees' tree, with Mintu;
- V3A: the river splash;
- V4A: the blueberry bushes.

Builder **rev 1.5** changes only these four prompts. The old takes are kept as `-v1-picnic` (fallback; never deleted).
Fable's checks on a mirror: LINT PASS 18/0/0, `test_prompt_lint` PASS, runner dry-run 4 rows $2.40, no errors.
**Spend:** 24 s, $2.40 list, cap $2.50. Arul raised the song cap to $17 (A12 total ≤ $15.50).

## Hard limits
- **API spend ≤ $2.50 at list price.** Only `V1A,V2A,V3A,V4A`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print `.env` values, keys, the workspace id or any URL. Never touch RunPod. Commits carry `[skip ci]`; never commit `.env`,
  `out/`, `out_4k/`, `tools/`, `_to_delete/`.
- **Move or rename, never delete or overwrite.** Never overwrite a take, a staged clip or a cut.
- In the song folder `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\`:
  - write only staged clips, `_cuts\` and `_superseded-2026-10-13\`;
  - never touch the WAVs/MP3s, `refs\`, `_gen\` or the runsheet files.
- Do not edit generated files (`shots\*.raw.txt`, `shots.csv` except the runner's own status updates, `lint.json`, `scale.json`,
  `characters.txt`, `refs\send\*`) or the runner.

## Protocol (markers in `queue\2026-10-13-karadi-restage1\`)
As before: `LOG.md` start/done lines, `item-N.report.md`, `item-N.done`, or `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Karadi restage 1 done — Fable will review queue\2026-10-13-karadi-restage1".
