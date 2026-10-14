# CC QUEUE — 2026-10-13 "Karadi rev 2.1 refs": rebuild with the three set plates + Appa's daypack ref, move rev 1.x files aside, commit (no API spend)

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

Arul made the three Gemini set plates and Appa's trek body (13 Oct 22:34–22:49); Fable named them in the song folder's `refs\`:
`11-set-path-low.jpg`, `12-set-path-high.jpg`, `13-set-home.jpg`, `08b-appa-body-backpack.jpg` (+ Arul's re-rendered `06-amma-front.jpg`).
The builder (rev 2.1) picks them up by name: every trek-place clip now sends its plate, and Appa's 17 clips send the daypack body.
Verified on Fable's mirror: self-test OK, LINT PASS 21/0/0, dry-run **$12.20** (unchanged), kept verse answers byte-identical, cut plan no gaps.
This queue reproduces that on Beast, tidies the rev 1.x leftovers CC reported in `2026-10-13-karadi-rev20-build`, and commits.
**API spend: $0.00.**

## Hard limits
- No API calls, no render, no pod. Never print `.env` values, keys, the workspace id or any URL.
- Song folder `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\`: the builder writes `KARADI-MAMA-WAN3-RUNSHEET.md`,
  `karadi-shots.json`, `_gen\scale.json`, `_gen\lint.json` — nothing else. Never touch the WAVs, `refs\`, `_cuts\`, `_previews\`.
- Repo `songs\a12-karadi-w3\`: **move, never delete** (step 2). The four kept takes `V1A|V2A|V3A|V4A-seed30313-w3.mp4` stay in `out\`.
- Commits carry `[skip ci]`. Never commit `.env`, `out/`, `out_4k/`, `tools/`.

## Protocol (markers in `queue\2026-10-13-karadi-rev21-refs\`)
As before: `LOG.md` start/done lines, `item-N.report.md`, `item-N.done`, or `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $0.00`, tell Arul "Karadi rev 2.1 refs done — Fable will review queue\2026-10-13-karadi-rev21-refs".
