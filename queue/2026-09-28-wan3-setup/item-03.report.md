# item-03 report — 4K upscale, comparisons, copies, report, commit ($0)

**Upscale** (laptop, Vulkan on Intel Iris Xe). No `-Fps`: Wan 3.0 is already 30 fps. `-Height 2160`; the console printed
**`ncnn scale x3`** for all three.

| clip | output | backend / factor | interpolation | decode / upscale / encode s | s/frame |
|---|---|---|---|---|---|
| T04_w3 | 3840×2160 @ 30, 150 f | ncnn / x3 | none | 7.0 / 1094.4 / 169.5 | 7.30 |
| T08_w3 | 3840×2160 @ 30, 150 f | ncnn / x3 | none | 6.6 / 873.9 / 62.7 | 5.83 |
| T07_w3 | 3840×2160 @ 30, 150 f | ncnn / x3 | none | 6.4 / 1000.3 / 118.1 | 6.67 |

**4K files**
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\4K\T04_w3-seed30313-w3-4K.mp4` (+ `.mp4.json`)
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\4K\T07_w3-seed30313-w3-4K.mp4` (+ `.mp4.json`)
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\4K\T08_w3-seed30313-w3-4K.mp4` (+ `.mp4.json`)

**Comparison PNGs** (t = 2.5 s; Wan 3.0 left, Phantom right; 720 high)
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\_qc\T04-wan3-vs-phantom720.png` (2560×720)
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\_qc\T07-wan3-vs-phantom480.png` (2528×720)
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\_qc\T08-wan3-vs-phantom720.png` (2560×720)

**L01:** not rendered (no keyframe), so there is no loop preview, first/last PNG or L01 copy.

**Copies** in `C:\Channel Contents\MinMiniKids\songs\Twinkle Twinkle\wan3-test\`:
- `T04_w3-seed30313-w3-4K.mp4`, `T07_w3-seed30313-w3-4K.mp4`, `T08_w3-seed30313-w3-4K.mp4`
- `T04-wan3-vs-phantom720.png`, `T07-wan3-vs-phantom480.png`, `T08-wan3-vs-phantom720.png`

**Report:** `C:\Projects\opencode\video_image\CC-REPORT-phase6e.md`

**Commit:** the `[skip ci]` commit that contains this file. It holds `_ab7` `shots.csv` (3× done), the report, `batch_6e.log`
(no URLs or keys) and this queue folder. `songs/shorts-loops/shots.csv` is unchanged because L01 was not run.
The hash is in chat and in `git log -1 -- queue/2026-09-28-wan3-setup/item-03.report.md`.

Clips not judged; Fable frame-checks them.
