# item-03 report — Tamil + English rough cuts ($0, local ffmpeg)

- Command: `python comfy\song_cuts.py songs\rowboat cut --lang both --src out --force` → exit 0, run **21:49:08 → 21:59:47 UTC**.
  The log is `C:\Projects\opencode\video_image\songs\rowboat\cuts_rough1.log`.

| cut | path | duration | size | video | audio |
|---|---|---|---|---|---|
| Tamil | `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-TA.mp4` | **123.767 s** (plan 123.76; audio 123.760 s) | 170,269,807 B | h264 1920×1080 30 fps | 1× AAC 48 kHz stereo |
| English | `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-EN.mp4` | **96.920 s** (plan 96.92; audio 96.920 s) | 132,972,693 B | h264 1920×1080 30 fps | 1× AAC 48 kHz stereo |

- **Cutlogs:**
  - `...\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-TA.cutlog.txt` lists 29 shots (01 I1 … 29 T1).
  - `...\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-EN.cutlog.txt` lists 24 shots. X1a, X1b, X2a, X2b and T1 have no English slot in
    `cutplan.json` (`en_in`/`en_out` = None), so they are omitted by design.
  - The cutlogs give in-point / use / slip / transition per shot but not file names. **The take per shot is from `cutplan.json`:**
    every shot uses `<ID>-seed30313-w3.mp4`, except **V2d = `V2d-seed30313-w3-splice2.mp4`** (Fable's hand-built take, as intended).
- **Bad / missing shots: 0.** The log has 0 lines matching bad|missing|error|warn|not found.
- Also written by the tool in `_cuts\`: `_graph-ta.txt` (updated) and `_graph-en.txt` (new), the ffmpeg filter graphs.
- `_cuts\_partial-interrupted-TA.mp4` was left in place, md5 unchanged. Arul can delete it.
- **Song folder:** the 34 files outside `_cuts\` were fingerprinted before item-03. After it: 34 unchanged, 0 changed, 0 new.
  Only `_cuts\` was written. The 280 protected render files in `songs\rowboat\out\` are also unchanged.
