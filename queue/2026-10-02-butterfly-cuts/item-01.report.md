# item-01 report — stage clips, build both rough cuts, commit ($0)

## 1. Plan test
`python tests\test_song_cuts_reuse.py --plan-only` → `PASS (plan only): rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit`.

## 2. Takes
`songs\a07-butterfly\cutplan.json` names **33 distinct takes** for 48 slots, and **all 33 exist** in `songs\a07-butterfly\out\` (0 missing).
Six are splices: V1c, V2a, V2b, V2c, V3a and V6b (`<ID>-seed30313-w3-splice.mp4`).

## 3. Staged numbered clips
`python comfy\song_cuts.py songs\a07-butterfly stage --song-folder "C:\Channel Contents\MinMiniKids\songs\A07-Butterfly"` → exit 0.
There are 33 files in `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`. Each was checked by md5 to be a **byte-identical copy of
its cutplan take**:

01_I1_arriving-at-the-park.mp4 · 02_I2_the-butterflies-wake-up.mp4 · 03_RA_refrain-a-flap-in-a-row.mp4 ·
04_RB_refrain-b-flap-from-the-grass.mp4 · 05_CH3_flying-from-flower-to-flower.mp4 · 06_CH4_dancing-round-and-round.mp4 ·
07_V1a_hello-red-butterfly.mp4 · 08_V1b_pretty-little-butterfly.mp4 · 09_V1c_round-and-round-the-roses.mp4 ·
10_V1d_flapping-wings-off-it-goes.mp4 · 11_V2a_hello-tiny-yellow-butterfly.mp4 · 12_V2b_like-a-baby.mp4 ·
13_V2c_it-lands-on-the-jasmine.mp4 · 14_V2d_swaying-slowly.mp4 · 15_V3a_hello-blue-butterfly.mp4 · 16_V3b_sky-blue-butterfly.mp4 ·
17_V3c_high-above-the-park.mp4 · 18_V3d_it-smiles-at-a-flower.mp4 · 19_BRKb_searching-the-hedge-no-singing.mp4 ·
20_V4a_hello-green-butterfly.mp4 · 21_V4b_leafy-green-butterfly.mp4 · 22_V4c_hiding-in-the-leaves.mp4 · 23_V4d_peekaboo.mp4 ·
24_V5a_open-your-wings.mp4 · 25_V5b_close-your-wings.mp4 · 26_V5c_up-it-goes-down-it-comes.mp4 · 27_V5d_playing-with-the-breeze.mp4 ·
28_V6a_from-flower-to-flower.mp4 · 29_V6b_happy-smiling-faces.mp4 · 30_V6c_sunshine-warms-their-wings.mp4 ·
31_V6d_up-into-the-sky.mp4 · 32_O3_they-land-and-fall-asleep.mp4 · 33_O4_shh-they-re-sleeping-english-only.mp4

## 4. Rough cuts
`python comfy\song_cuts.py songs\a07-butterfly cut --lang both --src out --tag ROUGH --song-folder "…\A07-Butterfly"` → exit 0,
**00:24:47 → 00:50:52 UTC, 2026-10-03** (20:24 → 20:50 Toronto, 2026-10-02). The log is
`C:\Projects\opencode\video_image\songs\a07-butterfly\cuts_rough1.log`.
- `wrote C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\_cuts\A07-BUTTERFLY-ROUGH-TA.mp4 6481 video frames = plan 6481; container 216.040 s (audio 216.040 s)`
- `wrote C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\_cuts\A07-BUTTERFLY-ROUGH-EN.mp4 6665 video frames = plan 6665; container 222.167 s (audio 222.160 s)`
- **"holds last frame" lines: none** (0 in the log, 0 in either cutlog).
- The cutlogs have 47 slots (TA) and 48 (EN).

## 5. ffprobe (video frames counted with `-count_frames`)
| cut | video | frames | video dur | audio | size |
|---|---|---|---|---|---|
| `…\_cuts\A07-BUTTERFLY-ROUGH-TA.mp4` | h264 1920×1080 30 fps | **6481** | 216.033 s | 1× AAC 48 kHz stereo, 216.040 s | 313,885,820 B |
| `…\_cuts\A07-BUTTERFLY-ROUGH-EN.mp4` | h264 1920×1080 30 fps | **6665** | 222.167 s | 1× AAC 48 kHz stereo, 222.160 s | 320,239,921 B |

Also written in `_cuts\`: `A07-BUTTERFLY-ROUGH-TA.cutlog.txt`, `A07-BUTTERFLY-ROUGH-EN.cutlog.txt`, `_graph-ta.txt`, `_graph-en.txt`.

## Safety checks
- **Song folder:** all 49 files that existed before (at all levels) are md5 unchanged. 39 files are new, all of them allowed:
  the 33 `NN_ID_slug.mp4` plus the 6 files in `_cuts\`. Nothing else was added.
- **Takes:** all 301 files in `songs\a07-butterfly\out\` are md5 unchanged. Nothing was deleted or overwritten.
- No API spend, no render. `songs\rowboat\` was not touched.

## 6. Commit
The `[skip ci]` commit containing this file: `songs/a07-butterfly/_splices.py`, `songs/a07-butterfly/cutplan.json`,
`songs/a07-butterfly/cuts_rough1.log` and the queue folder. Nothing under `out/`. The hash is in CC's chat reply.
