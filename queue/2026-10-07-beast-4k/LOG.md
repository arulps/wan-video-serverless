# LOG — queue 2026-10-07-beast-4k (machine: arulps-beast)

- 2026-10-07 23:12 QUEUE START
- 23:12 item-01 start
- 23:12 item-01 done (prereqs OK, tool installed in tools\, .gitignore updated)
- 23:12 item-02 start
- 23:13 item-02 done (dry: 33 clips, 5217 frames, no "not found")
- 23:13 item-03 start (V1a speed test)
- 23:13 item-03 note: first try failed, `ModuleNotFoundError: numpy` (Beast's Python had no numpy/Pillow). Installed numpy 2.5.3 + Pillow 12.3.0 with pip (local, $0), reran.
- 23:14 item-03 done (150 frames, 82 s wall, 0.54 s/frame, ncnn/vulkan; full-run estimate ~46 min + cuts — under 12 h, continue)
- 23:15 item-04 start
- 23:15 item-04 started (own PowerShell window, PID 19568; expected finish ~00:05-00:20); not waiting
- 23:16 item-05 step 1: commit + push; step 2 (verify) pending until the run finishes — queue stays open, no QUEUE END yet
- 2026-10-08 00:44 (Arul) first cut attempt had failed on ffmpeg 9 (`-filter_complex_script` rejected); Fable fixed `comfy/song_cuts.py`, Arul re-ran `song_4k.ps1`; both 4K cuts built 00:47 / 00:50 (see item-05-addendum.md)
- 2026-10-08 item-05 step 2 start (later CC session)
- item-05 step 2: out_4k 33 clips + 33 sidecars, all 3840x2160 @ 30 fps; ROUGH3-4K-TA 6481 frames, ROUGH3-4K-EN 6665 frames, one AAC each, 0 holds; test PASS; 4 stills in `out_4k\_qc`
- item-04 done, item-05 done
- QUEUE END 2026-10-08 20:08
