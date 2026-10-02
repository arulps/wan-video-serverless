# item-01 report — V2 cuts (1080p, hard cuts): BLOCKED

## What ran
`python comfy\song_cuts.py songs\rowboat cut --lang both --src out --tag V2` → exit 0, **09:21:32 → 09:24:39 UTC** (05:21 → 05:24 Toronto).
The log is `C:\Projects\opencode\video_image\songs\rowboat\cuts_v2.log`. The tool printed
`wrote ...-V2-TA.mp4 123.760 s (audio 123.760 s)` and `wrote ...-V2-EN.mp4 96.920 s (audio 96.920 s)`.

## Checks
| check | TA | EN |
|---|---|---|
| container duration | 123.760 s | 96.920 s |
| 1920×1080, 30 fps, one AAC (48 kHz stereo) | yes | yes |
| `grep -c "holds last frame"` in the V2 cutlog | **0** | **0** |
| cutlog shots / xfade / hard-cut | 29 / 4 / 24 | 24 / 4 / 19 |
| **video stream duration / frames** | **13.367 s / 401 frames** | **13.367 s / 401 frames** |
| audio stream duration | 123.760 s | 96.920 s |
| file size | 23,169,144 B | 22,231,206 B |

**The video track stops after the second shot.** Both V2 files have only 401 video frames (13.37 s = I1 7.749 s dissolved 0.4 s into
I2 6.035 s). For the rest of the song there is audio only. The TA and EN video streams are bit-identical (stream-copy md5
`7b7c52448f09c073ceaca074a5489dd4`). ROUGH-TA, by contrast, has 3713 video frames. The "≈123.76 / 96.92 s" check passes only
because the container duration comes from the audio. That is why I marked the item **blocked** rather than done.

## Likely cause (for Fable; not fixed by CC)
In `_cuts\_graph-ta.txt` every hard cut is a 1-frame `xfade` (`duration=0.0333`) chained onto the previous output, for example
`[x1][c2]xfade=transition=fade:duration=0.0333:offset=13.3510[x2]`.
- After `[c0][c1]xfade=...duration=0.4000:offset=7.3490[x1]`, the stream `[x1]` really holds 401 frames = **13.367 s**.
- The next xfade needs offset + duration = 13.351 + 0.0333 = **13.384 s**. That is past `[x1]`'s last real frame (the padded clip
  lengths such as 6.0353 s are not whole frames at 30 fps).
- So xfade never starts the next input, and the video ends. Every later hard cut has the same edge condition.
- `--dry` only writes the graph and cutlog without encoding, so it could not catch this.
- Fixes for Fable to pick from: hard cuts as `concat` of trimmed segments instead of 1-frame xfades; or round each segment to
  whole frames and keep offset + duration ≤ the accumulated length (e.g. subtract one frame); or verify the output's video frame
  count against the plan after encode.

## Safety checks (all OK)
- `*-ROUGH-*` files (TA/EN mp4 + cutlogs) and `_partial-interrupted-TA.mp4`: **md5 unchanged**.
- The 34 song-folder files outside `_cuts\`: unchanged, 0 new.
- The 304 render files in `songs\rowboat\out\`: unchanged.
- Written to `_cuts\`: `...-V2-TA.mp4`, `...-V2-EN.mp4`, their two cutlogs, and `_graph-ta.txt` / `_graph-en.txt`
  (overwritten; not ROUGH files).

## Not done (queue stopped at the blocked check)
- Step 3 (remove `songs\rowboat\out_4k_test`) and step 4 (commit/push) were not done. Nothing was committed.
- item-02 (4K smoke test) was not started.

## Paths
- `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-V2-TA.mp4` (defective: 13.4 s of video)
- `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-V2-EN.mp4` (defective: 13.4 s of video)
- `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-V2-TA.cutlog.txt`, `...-V2-EN.cutlog.txt`
- `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\_graph-ta.txt`, `_graph-en.txt`
