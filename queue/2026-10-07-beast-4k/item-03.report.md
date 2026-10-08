# item-03 — speed test on one clip (V1a) — DONE

## Deviation to note (not in the dispatch's prerequisite list)
The first run stopped at once with `ModuleNotFoundError: No module named 'numpy'` — Beast's Python 3.12 had neither
numpy nor Pillow, which `scripts\upscale_video.py` imports. Installed only those two with
`py -m pip install numpy "Pillow>=10.0"` → numpy 2.5.3, Pillow 12.3.0 (user Python at
`C:\Users\arulp\AppData\Local\Programs\Python\Python312`; local, $0; the rest of `requirements.txt` — runpod etc. — was
NOT installed). Rerun succeeded. torch is not installed (not needed: ncnn backend).

## Result — `py scripts\upscale_song.py songs\a07-butterfly --only V1a`
```
to do: 1 clips, 150 frames
[1/1] V1a V1a-seed30313-w3.mp4 (150 frames)
[23:13:14] source 1280x720 @ 30.000 fps, 5.00 s, audio=False -> target 3840x2160 @ 30.000 fps on vulkan
[23:13:14] ncnn scale x3
[23:13:15] decoded 150 frames in 0.7s
[23:13:15] Real-ESRGAN x3 via realesrgan-ncnn-vulkan (150 frames)
[23:14:25] upscaled 150 frames in 70.6s (0.47s/frame)
[23:14:35] encoded in 9.7s
[23:14:35] DONE songs\a07-butterfly\out_4k\V1a-seed30313-w3.mp4: 3840x2160 @ 30.000 fps, 5.00 s, 24.4 MB
   done V1a; 150/150 frames, 0.54 s/frame, ETA 0 min
ALL DONE: 1 clips in songs\a07-butterfly\out_4k
```
| | |
|---|---|
| Wall time | 82 s (whole command) |
| Seconds per frame | 0.47 s/frame upscale only; **0.54 s/frame** end to end (decode + upscale + encode) |
| Output | `songs\a07-butterfly\out_4k\V1a-seed30313-w3.mp4`, 24.4 MB, h264 |
| ffprobe -count_frames | 3840×2160, r_frame_rate 30/1, **150** frames |
| Backend | log: `on vulkan` / `Real-ESRGAN x3 via realesrgan-ncnn-vulkan`; sidecar: `"backend": "ncnn"`, `"device": "vulkan"` (RTX 2080 Ti) |

## Estimate for the full run
(5,217 − 150) = 5,067 frames × 0.54 s/frame ≈ 2,736 s ≈ **46 min** for the 32 remaining takes, plus the two 4K cut
encodes (a few minutes each, not measured). Far under the 12 h limit → continue to item-04.
