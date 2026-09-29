# CC-REPORT — Learning batch 5: crow A6, one more try (A6_w3d) on Wan 3.0 (2026-09-29)

Queue `queue\2026-09-29-learning-batch5`. **Result: 1/1 rendered. Estimate $0.50 at list price** (~$0.35 with the 30% discount;
cap $0.60). 720p 9:16 5 s with sound, seed 30313, no upscale, no pod.

- Credentials: `credentials present: True`.
- Dry-run: 1 row, `audio=on`, refs=0, `first=` and `last=` both `songs\shorts-learning\keyframes\A6-gate-empty.png`,
  **estimated $0.50**, no MISSING or ERROR.
- **Render window:** **18:02:39 → 18:04:53 UTC, 2026-09-29** (14:02:39 → 14:04:53 Toronto EDT).
- Video + audio. No URL or key appears in the sidecar or the log. The `shots.csv` status is `done`.

| row | refs | frames | status | task id | wall s | length | est (list) | seam |
|---|---|---|---|---|---|---|---|---|
| A6_w3d | 0 | first = last = keyframe | done | `92a97bd3-2bba-43d7-908d-762913df8c99` | 132.6 | 5 s | $0.50 | **1.6** |

- **Seam method:** OpenCV (`cv2` 4.13), the pilot's one-liner: frame 0 vs the last of 150 frames, mean abs BGR difference, 0–255.
- **Against the keyframe:** frame 0 = **2.7**, last frame = **2.9**. These are the same as A6_w3c, as expected with the same locked frames.
- **A6_w3d is a new clip, not a duplicate of A6_w3c.** The md5, task id and prompt all differ. The per-frame difference vs A6_w3c
  is 0.6 at frame 0, 3.2 at 40, 7.8 at 75, 11.6 at 110 and 1.6 at 149: the middle differs, and the locked ends agree.
- **Contact sheet:** 5×2, every 15th frame, 216 wide. **Loop preview:** `-stream_loop 2 -c copy`, 15.16 s.

## Paths
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\A6_w3d-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\A6_w3d-strip.png`
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\A6_w3d-contact.png`
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\A6_w3d-loop-x3.mp4`
- Log: `C:\Projects\opencode\video_image\songs\shorts-learning\batch_learning5.log`

Copies. The A6 folder went from 10 to 13 files and the no-overwrite guard hit nothing. `A6-metadata.md`, the earlier A6 clips and
`renders-learning\USE-CLIPS.md` are untouched.
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A6\A6_w3d-seed30313-w3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A6\A6_w3d-contact.png`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A6\A6_w3d-loop-x3.mp4`

## Commit
The `[skip ci]` commit containing this report. It holds `shots/A6-w3d.txt`, `shots.csv`, `REVIEW-learning-batch1-2026-09-29.md`,
the queue folder and this report. The hash is in CC's chat reply.

## Not judged
Fable reviews, in particular whether the crow is big and centred this time.
