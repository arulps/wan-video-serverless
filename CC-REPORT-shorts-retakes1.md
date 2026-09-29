# CC-REPORT — Shorts retakes 1: L03 yawn, L04 sneeze, L10 raindrop on Wan 3.0 (2026-09-28)

Queue `queue\2026-09-28-shorts-retakes1`. **Result: 3/3 rendered, 0 failed. Estimate $1.60 at list price** (~$1.12 with
the 30% discount; cap $1.80). 720p 9:16 with sound, no upscale, no pod.

- Credentials: `credentials present: True`. Dry-run: 3 rows, all `audio=on`, estimated $1.60, no MISSING or ERROR.
- Render window: **01:19:05 → 01:22:46 UTC, 2026-09-29** (21:19:05 → 21:22:46 Toronto EDT, 2026-09-28).
- No URL or key appears in the sidecars or the log.

| row | status | task id | wall s | length | est (list) | seam |
|---|---|---|---|---|---|---|
| L03_w3b (seed 4242) | done | `c3588a8e-655b-4cbc-9de8-115a1db65027` | 211.3 | 6 s (180 f) | $0.60 | **8.6** |
| L04_w3b (seed 30313) | done | `9df92af4-6f70-43b9-b855-24fa357ca2f2` | 163.5 | 5 s (150 f) | $0.50 | **11.6** |
| L10_w3b (seed 30313) | done | `d7a48f51-ac3e-4095-b72e-ae6687a6692a` | 178.9 | 5 s (150 f) | $0.50 | **22.3** |

**Seam method:** OpenCV (`cv2` 4.13). Frame 0 and the last decoded frame are compared as the mean absolute difference over
all BGR pixels, on 0–255. This is the item's one-liner.

**Contact sheets:** 5×2, every 15th frame, 216 wide.
**Loop previews:** `-stream_loop 2 -c copy`; 18.16 s for L03, 15.16 s for L04 and L10.

## Paths
Working copies
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L03_w3b-seed4242-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L04_w3b-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L10_w3b-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L03_w3b-strip.png`, `L03_w3b-contact.png`, `L03_w3b-loop-x3.mp4`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L04_w3b-strip.png`, `L04_w3b-contact.png`, `L04_w3b-loop-x3.mp4`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L10_w3b-strip.png`, `L10_w3b-contact.png`, `L10_w3b-loop-x3.mp4`
- Log: `C:\Projects\opencode\video_image\songs\shorts-loops\batch_retakes1.log`

Copies. These were added next to the first-batch files; nothing was overwritten, and the `Lxx-metadata.md` files are untouched.
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L03\L03_w3b-seed4242-w3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L03\L03_w3b-contact.png`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L03\L03_w3b-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L04\L04_w3b-seed30313-w3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L04\L04_w3b-contact.png`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L04\L04_w3b-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L10\L10_w3b-seed30313-w3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L10\L10_w3b-contact.png`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L10\L10_w3b-loop-x3.mp4`

## Housekeeping and commit
- `queue\_retakes1-combined.tmp` was deleted. It was untracked: Fable's 4 KB concatenation of the queue files.
- Commit: the `[skip ci]` commit containing this report. It holds `shots.csv` (3× done), `shots/L03-w3b.txt`, `L04-w3b.txt`,
  `L10-w3b.txt`, `world-garden-rain.txt`, the queue folder and this report. The hash is in CC's chat reply.
- Not committed and not touched: the untracked phase 7a YouTube-upload files, `REVIEW-shorts-batch1-2026-09-28.md`,
  the `.gitignore` change, and the batch logs. None of them is in this queue's list.

## Not judged
Fable reviews.
