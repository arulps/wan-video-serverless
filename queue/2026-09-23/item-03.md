# item-03 — upscale utility: exercise the 16→30 fps interpolation path (laptop only, NO GPU rental, $0)

**Why:** phase 5a's test (`outputs/upscale-test-2026-09-23/01-4k*.mp4`) passed Fable's frame check for the upscale, but the source
was an OpenArt 30 fps clip so `--fps 30` did nothing (`"interpolation": "none"`). Our own Wan clips are 16 fps — that path is untested.
Arul tried to run it himself from the wrong folder with `python` not on PATH; CC runs it on the laptop with `py`.

## Steps (laptop, repo root `C:\Projects\opencode\video_image`)
1. `py scripts\upscale_video.py --help` (confirm `py` works; if only `python3` exists use that — never install anything).
2. `where rife-ncnn-vulkan` — note whether it is on PATH (decides RIFE vs ffmpeg `minterpolate`).
3. Run, timing it:
   ```
   py scripts\upscale_video.py songs\twinkle-twinkle\out\T16-seed30313-s6.mp4 outputs\upscale-test-2026-09-23\T16-4k-30.mp4 --fps 30
   ```
   Source is 832x480 @ 16 fps, 81 frames; expect 3840x2160 @ 30 fps, ~152 frames. Wall time on this GPU will be a few minutes.
4. Also make the QC pair Fable checks motion with (same folder, `_qc\`):
   ```
   ffmpeg -y -i outputs\upscale-test-2026-09-23\T16-4k-30.mp4 -vf "select='between(n,60,67)',scale=960:-1,tile=8x1" -vsync 0 -frames:v 1 outputs\upscale-test-2026-09-23\_qc\T16-4k-30-frames60-67.png
   ffmpeg -y -i songs\twinkle-twinkle\out\T16-seed30313-s6.mp4 -vf "select='between(n,32,35)',scale=960:-1,tile=4x1" -vsync 0 -frames:v 1 outputs\upscale-test-2026-09-23\_qc\T16-src-frames32-35.png
   ```
5. `item-03.report.md`: full paths of the mp4 + `.json` sidecar + the two PNGs; the sidecar's `interpolation` and `seconds` values;
   `ffprobe` width/height/fps/nb_frames of the output; which interpolator was used; any warnings. Then `item-03.done`, wait for verdict.
