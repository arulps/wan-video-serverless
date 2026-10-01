# item-02 — rebuild Tamil + English rough cuts ($0, local ffmpeg)

1. `python comfy\song_cuts.py songs\rowboat cut --lang both --src out --force 2>&1 | tee songs\rowboat\cuts_rough2.log`
2. ffprobe both `_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-TA.mp4` (≈ 123.76 s) and `...-ROUGH-EN.mp4` (≈ 96.92 s): 1920x1080,
   30 fps, one AAC stream each. Bad/missing count from the log must be 0. Only `_cuts\` is written.
**item-02.report.md:** both outputs with duration/size/streams; bad/missing count.
