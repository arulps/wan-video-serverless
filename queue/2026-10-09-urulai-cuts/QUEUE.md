# CC QUEUE — 2026-10-09 "Urulai cuts": L05 cutplan + TA/EN rough cuts (no API spend)

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

All 17 clips exist (16 keepers; ZO is the current third take and stays until Arul decides on a retake). Fable wrote
`_gen\make_cutplan.py` in the song folder. It turns the builder's slot plan (`urulai-shots.json`, 33 slots) into the repo's
`cutplan.json` for `comfy\song_cuts.py`. Fable checked it in the cloud workspace:
- every slot fits inside its clip;
- there are no gaps;
- 480p preview cuts of both languages had exact frame counts (TA 4448, EN 4452) and no held frames.

This queue makes the real 1080p rough cuts on Beast. **API spend: $0.00** — local ffmpeg only.

## Hard limits
- No API calls, no renders, no pod, no upscale. Never print `.env` values, keys, the workspace id or any URL.
- In the song folder `C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\`, write **only** the staged clips
  (`NN_ID_slug.mp4`, copies) and `_cuts\`. Never touch `_audio\`, the WAVs, `refs\` or the runsheet files.
- Repo: add `songs\l05-urulai-w3\cutplan.json` only. Do not edit `shots.csv`, the shot files or `out\`. Move, never delete.
- Commits carry `[skip ci]`. Never commit `.env`, `out/`, `out_4k/`, `tools/`.

## Protocol (markers in `queue\2026-10-09-urulai-cuts\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $0.00`, tell Arul "Urulai rough cuts done — ask Fable to review queue\2026-10-09-urulai-cuts".
