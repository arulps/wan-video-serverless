# item-02 report — rebuild Tamil + English rough cuts ($0, local ffmpeg)

- Command: `python comfy\song_cuts.py songs\rowboat cut --lang both --src out --force` → exit 0, run **22:57:44 → 23:08:51 UTC**.
  The log is `C:\Projects\opencode\video_image\songs\rowboat\cuts_rough2.log`.

| cut | path | duration | size | video | audio |
|---|---|---|---|---|---|
| Tamil | `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-TA.mp4` | **123.767 s** (audio 123.760 s) | 170,172,021 B | h264 1920×1080 30 fps | 1× AAC 48 kHz stereo |
| English | `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-EN.mp4` | **96.920 s** (audio 96.920 s) | 132,853,818 B | h264 1920×1080 30 fps | 1× AAC 48 kHz stereo |

- **Bad / missing shots: 0.** The log has 0 lines matching bad|missing|error|warn|not found.
- Cutlogs (`...\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-TA.cutlog.txt`, `...-EN.cutlog.txt`): TA has 29 shots and EN 24 (X1a, X1b, X2a, X2b
  and T1 have no English slot, by plan).
  - V5c is at TA 106.382 s and EN 82.374 s, using `V5c-seed30313-w3.mp4` (the new take; `cutplan.json` take).
  - Both cut files changed size vs the 17:59 build (TA 170,269,807 → 170,172,021 B; EN 132,972,693 → 132,853,818 B), which is
    consistent with the new V5c being cut in.
- **Only `_cuts\` was written:** the 4 outputs plus `_graph-ta.txt` / `_graph-en.txt`. The 34 song-folder files outside `_cuts\`
  are unchanged, with 0 new files (md5 before vs after). `_cuts\_partial-interrupted-TA.mp4` is unchanged.
- The 294 protected render files in `songs\rowboat\out\` (done shots, `*-v1-*`, `*-v2-*`, `*splice*`) are unchanged.
