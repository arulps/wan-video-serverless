# CC-REPORT — Shorts retakes 2: L04 sneeze, hands-over-nose version on Wan 3.0 (2026-09-28)

Queue `queue\2026-09-28-shorts-retakes2`. **Result: 1/1 rendered. Estimate $0.50 at list price** (~$0.35 with the 30% discount;
cap $0.60). 720p 9:16 with sound, no upscale, no pod.

- Credentials: `credentials present: True`. Dry-run: 1 row, `audio=on`, 5 s, seed 4242, estimated $0.50, no MISSING or ERROR.
- Render window: **03:38:22 → 03:41:22 UTC, 2026-09-29** (23:38:22 → 23:41:22 Toronto EDT, 2026-09-28).
- No URL or key appears in the sidecar or the log.

| row | status | task id | wall s | length | est (list) | seam |
|---|---|---|---|---|---|---|
| L04_w3c (seed 4242) | done | `d87bdbe3-7814-45aa-8510-cf80d98d0534` | 178.7 | 5 s (150 f) | $0.50 | **8.6** |

**Seam method:** OpenCV (`cv2` 4.13), the same one-liner as retakes 1. It is the mean absolute difference of frame 0 vs
the last decoded frame over all BGR pixels, on 0–255. For comparison, L04_w3b was 11.6.

**Contact sheet:** 5×2, every 15th frame, 216 wide. **Loop preview:** `-stream_loop 2 -c copy`, 15.16 s.

## Paths
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L04_w3c-seed4242-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L04_w3c-strip.png`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L04_w3c-contact.png`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L04_w3c-loop-x3.mp4`
- Log: `C:\Projects\opencode\video_image\songs\shorts-loops\batch_retakes2.log`

Copies in `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L04\`: 3 files added. Nothing was overwritten, and
`L04-metadata.md` and the L04_w3 / L04_w3b files are untouched.
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L04\L04_w3c-seed4242-w3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L04\L04_w3c-contact.png`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L04\L04_w3c-loop-x3.mp4`

## Commit
The `[skip ci]` commit containing this report. It holds `shots.csv` (L04_w3c `done`), `shots/L04-w3c.txt`,
`REVIEW-shorts-retakes1-2026-09-28.md`, the queue folder and this report. The hash is in CC's chat reply.

## Not judged
Fable reviews: in particular, whether any white mark under the nose remains around the sneeze.
