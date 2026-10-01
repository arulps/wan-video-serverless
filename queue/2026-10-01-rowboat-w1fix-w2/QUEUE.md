# CC QUEUE — 2026-10-01 "Rowboat W1 retakes + W2": L04 Row Row Row Your Boat on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (frame-checks after).
Fable reviewed W1: I1, I2, V1c, X1a pass (with V1a). Six retakes. Cause of four of them: boat shots that referenced only part
of the family (kids-only / Appa-only packs) came back with the missing people invented off-model. Fable changed
`songs\rowboat\_make_rowboat.py` (`PACK_SWAP`, `PACK_SHOT`, `SHOT_FIX`): every boat shot now carries all six family refs,
V2c gets family + Modhu, plus wording fixes (V2a stays a close-up, V2d no cut / not crying, X1b boat stays on the water).
Old takes kept as `out\<ID>-seed30313-w3-v1-<reason>.mp4` (+ `_qc\<ID>-v1-<reason>-*.png`); their status cells blanked.
**Added before dispatch (Arul, 14:57):** every boat prompt says only Appa rows (Mintu had been drawn as the rower); every
shot with timed beats gets "one continuous take, no cuts between the timed moments"; new pre-dispatch gate
`comfy\prompt_lint.py` (+ `tests\test_prompt_lint.py`, rules in `songs\rowboat\lint.json`) — item-01 step 2b.
This queue renders **V1b,V2a,V2b,V2c,V2d,X1b,V3a,V3b,V3c** — the 6 W1 retakes (22 s) + world 2, golden grass and Singa (13 s).
Est **$3.50** list (35 s).

## Hard limits
- **API spend ≤ $4.00 at list price.** Only the 9 shots above. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\`.
- Do not delete, overwrite or re-render any clip whose status is `done` or any `*-v1-*` file.

## Protocol (markers in `queue\2026-10-01-rowboat-w1fix-w2\`)
As in `queue\2026-10-01-rowboat-w1`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Rowboat W1 retakes + W2 done — ask Fable to review queue\2026-10-01-rowboat-w1fix-w2".
