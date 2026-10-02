# item-01 report — V2 cuts (1080p, hard cuts) — REDO after Fable's frame-exact fix

Run 1 was blocked (`item-01.report-1-blocked.md`: video track stopped at 13.4 s). This REDO ran Fable's fixed `comfy\song_cuts.py`.

- `python comfy\song_cuts.py songs\rowboat cut --lang both --src out --tag V2` → exit 0, **09:44:51 → 10:03:13 UTC** (05:44 → 06:03
  Toronto). The log is `C:\Projects\opencode\video_image\songs\rowboat\cuts_v2.log`. No `VIDEO FRAME CHECK FAILED`; 0 lines matching
  bad|missing|error|warn|failed.
- The tool printed:
  - `wrote ...-V2-TA.mp4 3713 video frames = plan 3713; container 123.767 s (audio 123.760 s)`
  - `wrote ...-V2-EN.mp4 2908 video frames = plan 2908; container 96.933 s (audio 96.920 s)`

| cut | path | video stream (ffprobe `-count_frames`) | audio | size | holds |
|---|---|---|---|---|---|
| Tamil | `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-V2-TA.mp4` | h264 1920×1080 30 fps, **3713 frames, 123.767 s** | 1× AAC 48 kHz stereo, 123.760 s | 167,583,681 B | **0** |
| English | `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-V2-EN.mp4` | h264 1920×1080 30 fps, **2908 frames, 96.933 s** | 1× AAC 48 kHz stereo, 96.920 s | 131,055,124 B | **0** |

- The frame counts above were independently decoded by ffprobe and match the plan and the tool's own check.
- `grep -c "holds last frame"` = 0 in both V2 cutlogs (`...-V2-TA.cutlog.txt` 29 shots, `...-V2-EN.cutlog.txt` 24 shots).
- **md5 check:** the `*-ROUGH-*` mp4s + cutlogs and `_partial-interrupted-TA.mp4` are unchanged (5/5 OK).
  - The 34 song-folder files outside `_cuts\` are unchanged, 0 new.
  - The 304 render files in `songs\rowboat\out\` are unchanged.
  - Written to `_cuts\`: the two V2 mp4s (overwriting run 1's defective ones), their cutlogs, and `_graph-ta.txt` / `_graph-en.txt`.
- **Step 3:** `songs\rowboat\out_4k_test` was confirmed empty and removed. `songs\rowboat\out_4k\` was kept (empty).
- **Step 4 commit:** the `[skip ci]` commit containing this file (`comfy/song_cuts.py`, `comfy/prompt_lint.py` (unchanged since
  `3d5d91b`, so a no-op), `scripts/upscale_song.py`, `scripts/song_4k.ps1`, the queue folder). The hash is in `item-02.report.md`
  and in CC's chat reply.
