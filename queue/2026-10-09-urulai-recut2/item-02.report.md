# item-02 — 4K master started and running. $0.00.

## Pre-checks (all present)
- `tools\realesrgan-ncnn-vulkan\realesrgan-ncnn-vulkan.exe` exists (6,161,408 bytes).
- `py -c "import numpy, PIL"` works: numpy 2.4.4, Pillow 12.2.0.
- `ffmpeg -version`: `ffmpeg version 9.0.2-full_build-www.gyan.dev`.
- Extra: `py scripts\upscale_song.py songs\l05-urulai-w3 --dry` listed 17 clips, 3,955 frames, starting with
  `I1-seed30313-w3-splice.mp4` (295 frames).

## Start
Started 2026-10-09 21:59:18 in its own PowerShell window (process id 22588, `-NoExit`) with the command in the item
(`scripts\song_4k.ps1 -Song songs\l05-urulai-w3 -Tag V1-4K`, working directory the repo root).

## Log after about 2.5 minutes — last 10 lines of `songs\l05-urulai-w3\upscale_4k.log`
```
[21:59:22] Real-ESRGAN x3 via realesrgan-ncnn-vulkan (295 frames)
[22:01:26] upscaled 295 frames in 124.4s (0.42s/frame)
[22:01:45] encoded in 18.5s
[22:01:45] DONE songs\l05-urulai-w3\out_4k\I1-seed30313-w3-splice.mp4: 3840x2160 @ 30.000 fps, 9.83 s, 28.6 MB
   done I1; 295/3955 frames, 0.49 s/frame, ETA 30 min
[2/17] SA SA-seed30313-w3.mp4 (210 frames)
[22:01:46] source 1280x720 @ 30.000 fps, 7.00 s, audio=False -> target 3840x2160 @ 30.000 fps on vulkan
[22:01:46] ncnn scale x3
[22:01:47] decoded 210 frames in 1.0s
[22:01:47] Real-ESRGAN x3 via realesrgan-ncnn-vulkan (210 frames)
```
The first take (the I1 splice) finished at 22:01:45 and the second (SA) is upscaling, on ncnn/vulkan. No error in the log.
The log's own estimate is about 30 minutes for the upscale, then the two 4K cuts.
