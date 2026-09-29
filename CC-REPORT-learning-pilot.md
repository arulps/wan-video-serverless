# CC-REPORT — Learning pilot: 5 learning Shorts + L04 elbow sneeze on Wan 3.0 (2026-09-29)

Queue `queue\2026-09-29-learning-pilot`. **Result: 6/6 rendered, 0 failed. Estimate $3.00 at list price** (~$2.10 with the 30%
discount; cap $3.20). 720p 9:16 with sound, 5 s each, no upscale, no pod.

- Credentials: `credentials present: True`.
- Dry-runs:
  - learning pilot: 5 rows, `audio=on`, C1/F3/V2 refs=0, FD1/AC2 refs=1, **estimated $2.50**;
  - L04_w3d: **estimated $0.50**.
  - No MISSING or ERROR in either.
- **Run windows** (2026-09-29):
  - learning: **12:46:54 → 12:51:22 UTC** (08:46:54 → 08:51:22 Toronto EDT);
  - L04_w3d: **12:51:22 → 12:53:51 UTC** (08:51:22 → 08:53:51 Toronto).
- All six have video + audio streams. No URL or key appears in any sidecar or log.

| row | refs | status | task id | wall s | est (list) | seam |
|---|---|---|---|---|---|---|
| C1_w3 (red ball) | 0 | done | `fba5d899-2e1d-4c13-b00a-d5c154598ed2` | 111.5 | $0.50 | **3.0** |
| F3_w3 (apple) | 0 | done | `b94698b1-e502-49c8-a183-1f00c0694459` | 124.4 | $0.50 | **4.5** |
| FD1_w3 (Mintu idli) | 1 | done | `3443ab40-1aa1-4c5b-be21-752372188934` | 152.3 | $0.50 | **7.6** |
| AC2_w3 (Minnu clap) | 1 | done | `22d5c490-f1f3-48fc-955f-ee5eec4cc3ed` | 150.8 | $0.50 | **13.8** |
| V2_w3 (auto rickshaw) | 0 | done | `bbd82b69-4d3e-44a2-866e-4872765fede5` | 112.3 | $0.50 | **7.1** |
| L04_w3d (elbow sneeze) | 1 | done | `acc52b4b-139f-4111-95e6-bb15ef73b97b` | 147.2 | $0.50 | **9.4** |

**Seam method:** OpenCV (`cv2` 4.13), the same one-liner as retakes 1: the mean absolute difference of frame 0 vs the last
frame (150 frames each), BGR, on 0–255.
**Contact sheets:** 5×2, every 15th frame, 216 wide. **Loop previews:** `-stream_loop 2 -c copy`, 15.16 s each.

## Paths
Working copies — learning (`C:\Projects\opencode\video_image\songs\shorts-learning\out\`)
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\C1_w3-seed30313-w3.mp4` (+ `.json`), `...\out\_qc\C1_w3-strip.png`, `...\out\_qc\C1_w3-contact.png`, `...\out\_qc\C1_w3-loop-x3.mp4`
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\F3_w3-seed30313-w3.mp4` (+ `.json`), `...\out\_qc\F3_w3-strip.png`, `...\out\_qc\F3_w3-contact.png`, `...\out\_qc\F3_w3-loop-x3.mp4`
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\FD1_w3-seed30313-w3.mp4` (+ `.json`), `...\out\_qc\FD1_w3-strip.png`, `...\out\_qc\FD1_w3-contact.png`, `...\out\_qc\FD1_w3-loop-x3.mp4`
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\AC2_w3-seed30313-w3.mp4` (+ `.json`), `...\out\_qc\AC2_w3-strip.png`, `...\out\_qc\AC2_w3-contact.png`, `...\out\_qc\AC2_w3-loop-x3.mp4`
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\V2_w3-seed30313-w3.mp4` (+ `.json`), `...\out\_qc\V2_w3-strip.png`, `...\out\_qc\V2_w3-contact.png`, `...\out\_qc\V2_w3-loop-x3.mp4`
- Log: `C:\Projects\opencode\video_image\songs\shorts-learning\batch_pilot.log`

Working copy — L04
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L04_w3d-seed30313-w3.mp4` (+ `.json`), `...\out\_qc\L04_w3d-strip.png`, `...\out\_qc\L04_w3d-contact.png`, `...\out\_qc\L04_w3d-loop-x3.mp4`
- Log: `C:\Projects\opencode\video_image\songs\shorts-loops\batch_retakes3.log`

Copies. Each folder gained exactly 3 files; nothing was overwritten, and the `<ID>-metadata.md` files and earlier L04 clips are untouched.
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C1\C1_w3-seed30313-w3.mp4`, `...\C1\C1_w3-contact.png`, `...\C1\C1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\F3\F3_w3-seed30313-w3.mp4`, `...\F3\F3_w3-contact.png`, `...\F3\F3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FD1\FD1_w3-seed30313-w3.mp4`, `...\FD1\FD1_w3-contact.png`, `...\FD1\FD1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\AC2\AC2_w3-seed30313-w3.mp4`, `...\AC2\AC2_w3-contact.png`, `...\AC2\AC2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\V2\V2_w3-seed30313-w3.mp4`, `...\V2\V2_w3-contact.png`, `...\V2\V2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L04\L04_w3d-seed30313-w3.mp4`, `...\L04\L04_w3d-contact.png`, `...\L04\L04_w3d-loop-x3.mp4`

## Commit
The `[skip ci]` commit containing this report. It holds:
- `songs/shorts-learning/`: `_make_shots.py`, 72 `shots/`, `world.txt`, 5 `world-*.txt`, `characters.txt`, `style.txt`,
  `negative.txt`, `shots.csv`, and 7 `refs/*.png` added with `-f`. `out/` is not included.
- `songs/shorts-loops/shots/L04-w3d.txt` and `songs/shorts-loops/shots.csv`.
- The queue folder and this report.

The hash is in CC's chat reply. Not committed: `batch_pilot.log` / `batch_retakes3.log`, and the untracked
`songs/learning-loops/` and `REVIEW-shorts-batch1-2026-09-28.md`. None of these is in the queue's list.

## Not judged
Fable reviews.
