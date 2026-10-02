# LOG — queue 2026-10-02-rowboat-v2-4k (append-only)
[2026-10-02] Fable: queue written; V2 hard-cut cuts + 4K smoke test; $0 API
[2026-10-02 05:21] item-01 start
[2026-10-02 05:26] item-01 BLOCKED: V2 cuts encode only 401 video frames (13.37 s; video stops at the first hard cut, audio runs full length). Hard cuts are 1-frame xfades whose offset+duration exceeds the accumulated stream length. ROUGH files unchanged. Not committed; item-02 not started. Question for Fable: fix song_cuts.py hard-cut join, then REDO?
[2026-10-02] Fable: REDO item-01 — song_cuts.py now frame-exact (concat hard cuts, xfade only with real frames, tb 1/30) + video frame-count check; preview test TA 3713/3713, EN 2908/2908. item-01.blocked -> item-01.blocked-1
[2026-10-02 05:44] item-01 REDO start
[2026-10-02 06:07] item-01 REDO done: V2-TA 3713 frames = plan, V2-EN 2908 = plan, 1920x1080 30 fps, 1 AAC each, 0 holds; ROUGH md5 unchanged; out_4k_test removed
