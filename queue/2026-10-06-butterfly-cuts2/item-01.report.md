# item-01 report — re-stage 3 clips, build ROUGH2 cuts, commit ($0)

## 1. Plan test and takes
- `python tests\test_song_cuts_reuse.py --plan-only` → `PASS (plan only): rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit`.
- `cutplan.json` names **33 distinct takes**, and all exist in `songs\a07-butterfly\out\` (0 missing). V1b, V4a and V4b now point to
  `<ID>-seed30313-w3-splice.mp4`. There are 9 splice takes in all: V1b, V1c, V2a, V2b, V2c, V3a, V4a, V4b, V6b.

## 2. Three staged clips replaced (plain copies, no `stage --force`)
In `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`:

| staged file | copied from (`songs\a07-butterfly\out\`) | md5 before | md5 after = splice md5 | size |
|---|---|---|---|---|
| `08_V1b_pretty-little-butterfly.mp4` | `V1b-seed30313-w3-splice.mp4` | `bd7f162e5b64fccbd086470aa00966cb` | `b5499302dfe8ef9ff569da0339e5a724` ✔ | 3,134,653 B |
| `20_V4a_hello-green-butterfly.mp4` | `V4a-seed30313-w3-splice.mp4` | `5dd21806f3f3939363f5be2f2757ce2a` | `6e25b92981d23399f142e248666aa252` ✔ | 3,909,400 B |
| `21_V4b_leafy-green-butterfly.mp4` | `V4b-seed30313-w3-splice.mp4` | `ac00732ef7501dd07ccf4defd3932984` | `eeb13f6cf9eae199815d98c29ab1954f` ✔ | 4,380,841 B |

- Each staged file's md5 equals its splice.
- **The other 30 staged clips are md5 unchanged (30 of 30).**

## 3. ROUGH2 cuts
`python comfy\song_cuts.py songs\a07-butterfly cut --lang both --src out --tag ROUGH2 --song-folder "…\A07-Butterfly"` → exit 0,
**18:45:04 → 19:11:38 UTC, 2026-10-06** (14:45 → 15:11 Toronto). The log is
`C:\Projects\opencode\video_image\songs\a07-butterfly\cuts_rough2.log`.
- `wrote C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\_cuts\A07-BUTTERFLY-ROUGH2-TA.mp4 6481 video frames = plan 6481; container 216.040 s (audio 216.040 s)`
- `wrote C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\_cuts\A07-BUTTERFLY-ROUGH2-EN.mp4 6665 video frames = plan 6665; container 222.167 s (audio 222.160 s)`
- **"holds last frame" lines: none** (0 in the log, 0 in either ROUGH2 cutlog). The cutlogs have 47 slots (TA) and 48 (EN).

## 4. ffprobe (video frames counted with `-count_frames`)
| cut | video | frames | video dur | audio | size |
|---|---|---|---|---|---|
| `…\_cuts\A07-BUTTERFLY-ROUGH2-TA.mp4` | h264 1920×1080 30 fps | **6481** | 216.033 s | 1× AAC 48 kHz stereo, 216.040 s | 311,698,956 B |
| `…\_cuts\A07-BUTTERFLY-ROUGH2-EN.mp4` | h264 1920×1080 30 fps | **6665** | 222.167 s | 1× AAC 48 kHz stereo, 222.160 s | 318,026,557 B |

## Safety checks
- **ROUGH (v1) cuts unchanged:** `A07-BUTTERFLY-ROUGH-TA.mp4`, `-ROUGH-EN.mp4` and their two cutlogs have the same md5 as before.
- **Song folder (88 files before):**
  - changed: only the three re-staged clips, plus `_cuts\_graph-en.txt`. The cut tool rewrites its filter graphs in `_cuts\`;
    `_graph-ta.txt` was rewritten with identical content.
  - new: only `_cuts\A07-BUTTERFLY-ROUGH2-TA.mp4`, `-ROUGH2-EN.mp4` and their two cutlogs.
  - Nothing else changed or was added.
- **Takes:** all 304 files in `songs\a07-butterfly\out\` are md5 unchanged. Nothing was deleted or overwritten.
- No API spend, no render. `songs\rowboat\` was not touched.

## 5. Commit
The `[skip ci]` commit containing this file: `songs/a07-butterfly/_splices.py`, `songs/a07-butterfly/cutplan.json`,
`songs/a07-butterfly/cuts_rough2.log` and the queue folder. Nothing under `out/`. The hash is in CC's chat reply.
