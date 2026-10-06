# item-01 report — re-stage O3, build ROUGH3 cuts, commit ($0)

## 1. Checks
- `python tests\test_song_cuts_reuse.py --plan-only` → `PASS (plan only): rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit`.
- `python comfy\prompt_lint.py --song songs\a07-butterfly` → `LINT PASS: 33 shots, 0 fail, 0 warn`.
- `cutplan.json` names **33 distinct takes**, and all exist in `songs\a07-butterfly\out\` (0 missing). There are **10 splices**:
  O3, V1b, V1c, V2a, V2b, V2c, V3a, V4a, V4b, V6b. `O3-seed30313-w3-splice.mp4` is 1280×720 @ 30 fps, 204 frames.

## 2. O3 re-staged
`songs\a07-butterfly\out\O3-seed30313-w3-splice.mp4` → `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\32_O3_they-land-and-fall-asleep.mp4`
- md5 before `29882192369b3a23ea6b4ecbee1c6a9e` → after **`866c0ff2d349d5834e552f29d8b283e2`** = the splice's md5 ✔ (4,784,241 B).
- **The other 32 staged clips are md5 unchanged (32 of 32).**

## 3. ROUGH3 cuts
`python comfy\song_cuts.py songs\a07-butterfly cut --lang both --src out --tag ROUGH3 --song-folder "…\A07-Butterfly"` → exit 0,
**20:05:38 → 20:32:26 UTC, 2026-10-06** (16:05 → 16:32 Toronto). The log is
`C:\Projects\opencode\video_image\songs\a07-butterfly\cuts_rough3.log`.
- `wrote C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\_cuts\A07-BUTTERFLY-ROUGH3-TA.mp4 6481 video frames = plan 6481; container 216.040 s (audio 216.040 s)`
- `wrote C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\_cuts\A07-BUTTERFLY-ROUGH3-EN.mp4 6665 video frames = plan 6665; container 222.167 s (audio 222.160 s)`
- **"holds last frame" lines: none** (0 in the log, 0 in either ROUGH3 cutlog). The cutlogs have 47 slots (TA) and 48 (EN).
- **TA in-points** (`_cuts\A07-BUTTERFLY-ROUGH3-TA.cutlog.txt`), both as required:
  - `03 CH1=RA in    9.150 use  4.567 slip 0.000 frames  137 hard-cut` ✔ (required `in 9.150`)
  - `32 O3   in  209.340 use  6.700 slip 0.000 frames  201` ✔ (required `in 209.340`)

## 4. ffprobe (video frames counted with `-count_frames`)
| cut | video | frames | video dur | audio | size |
|---|---|---|---|---|---|
| `…\_cuts\A07-BUTTERFLY-ROUGH3-TA.mp4` | h264 1920×1080 30 fps | **6481** | 216.033 s | 1× AAC 48 kHz stereo, 216.040 s | 311,314,228 B |
| `…\_cuts\A07-BUTTERFLY-ROUGH3-EN.mp4` | h264 1920×1080 30 fps | **6665** | 222.167 s | 1× AAC 48 kHz stereo, 222.160 s | 318,149,249 B |

## Safety checks
- **ROUGH and ROUGH2 cuts unchanged:** all 8 files (4 mp4 + 4 cutlogs) have the same md5 as before.
- **Song folder (93 files before):**
  - changed: only `32_O3_they-land-and-fall-asleep.mp4` and `_cuts\_graph-ta.txt` (the cut tool rewrites its filter graphs);
  - new: only the two ROUGH3 mp4s and their two cutlogs.
- **Takes:** all 305 files in `songs\a07-butterfly\out\` are md5 unchanged.
- No API spend, no render. `songs\rowboat\` was not touched.

## 5. Commit
The `[skip ci]` commit containing this file: `songs/a07-butterfly/_splices.py`, `cutplan.json`, `shots.csv`, `shots/` (no changes there,
so a no-op), `cuts_rough3.log` and the queue folder. Nothing under `out/`. The hash is in CC's chat reply.
