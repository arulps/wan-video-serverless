# item-03 — Tamil + English rough cuts ($0, local ffmpeg)

1. `python comfy\song_cuts.py songs\rowboat cut --lang both --src out --force 2>&1 | tee songs\rowboat\cuts_rough1.log`
   (song folder comes from `cutplan.json`; outputs go to its `_cuts\`). Any error → **blocked** with the log tail.
2. Check with ffprobe and report: `_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-TA.mp4` ≈ 123.76 s, `...-ROUGH-EN.mp4` ≈ 96.92 s,
   both 1920x1080, 30 fps, one AAC audio stream. List the two `_cuts\*cutlog*` files (they say which take was used per shot).
3. A file `_cuts\_partial-interrupted-TA.mp4` (an interrupted test by Fable) may exist — leave it; Arul can delete it.
**item-03.report.md:** the two outputs with duration/size/streams; the "bad"/missing-shot count from the log (must be 0).
