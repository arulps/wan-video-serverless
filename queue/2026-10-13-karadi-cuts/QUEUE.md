# CC QUEUE — 2026-10-13 "Karadi cuts": A12 cutplan + TA/EN 1080p rough cuts (no API spend)

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

All 18 clips are kept (Fable's verdicts in the gate1b, gate2 and batch1 folders; Arul 13 Oct: keep CQb/CAb as they are).
Fable wrote `_gen\make_cutplan.py` in the song folder. It turns the builder's per-language slot plan (`karadi-shots.json`: Tamil 29
slots, English 24) into the repo's `cutplan.json`, with the batch-1 opening trims (I1 from 1.2 s, HKb 1.0 s later).
Fable ran it and `comfy\song_cuts.py` on a mirror of the clips and WAVs:
- every slot fits inside its clip;
- there are no gaps and no clip plays twice in a row;
- 480p preview cuts were frame-exact (TA 4644 frames = 154.800 s, EN 3840 = 128.000 s) with no held frames.

This queue makes the real 1080p rough cuts on Beast. **API spend: $0.00** — local ffmpeg only.

## Hard limits
- No API calls, no renders, no pod, no upscale. Never print `.env` values, keys, the workspace id or any URL.
- In the song folder `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\`, write **only** the staged clips (`NN_ID_slug.mp4`,
  copies) and `_cuts\`. Never touch the WAVs/MP3s, `refs\`, `_gen\` or the runsheet files.
- Repo: add `songs\a12-karadi-w3\cutplan.json` only. Do not edit `shots.csv`, the shot files or `out\`. Move, never delete.
- Commits carry `[skip ci]`. Never commit `.env`, `out/`, `out_4k/`, `tools/`.

## Protocol (markers in `queue\2026-10-13-karadi-cuts\`)
As before: `LOG.md` start/done lines, `item-N.report.md`, `item-N.done`, or `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $0.00`, tell Arul "Karadi rough cuts done — Fable will review queue\2026-10-13-karadi-cuts".
