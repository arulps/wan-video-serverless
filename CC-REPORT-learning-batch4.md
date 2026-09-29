# CC-REPORT — Learning batch 4: home sounds with a kid + crow with locked frames, on Wan 3.0 (2026-09-29)

Queue `queue\2026-09-29-learning-batch4`. **Result: 5/5 rendered, 0 failed. Estimate $2.50 at list price** (~$1.75 with the
30% discount; cap $3.00). 720p 9:16 5 s with sound, seed 30313, no upscale, no pod. SN4 keeps its first render.

- Credentials: `credentials present: True`.
- Dry-run: 5 rows, all `audio=on`. SN1/SN3 have refs=1 (Mintu) and SN2/SN6 refs=1 (Minnu). **A6_w3c** has refs=0, with
  `first=` and `last=` both `songs\shorts-learning\keyframes\A6-gate-empty.png` (720×1280 RGB).
  **Estimated $2.50**, no MISSING or ERROR.
- **Render window:** **17:31:44 → 17:35:39 UTC, 2026-09-29** (13:31:44 → 13:35:39 Toronto EDT). 3 tasks in parallel.
- All 5 have video + audio. No URL or key appears in any sidecar or the log. The 5 `shots.csv` status cells are `done`.

| row | refs | frames | status | task id | wall s | length | est (list) | streams | seam (earlier w3, w3b) |
|---|---|---|---|---|---|---|---|---|---|
| SN1_w3c | 1 | - | done | `8558ea2f-d049-4954-9ca2-635318a3a03d` | 115.1 | 5 s | $0.50 | video+audio | **15.1** (3.1, 3.2) |
| SN2_w3c | 1 | - | done | `ba6e7059-8b70-43f0-83cb-7fa5ed351106` | 115.0 | 5 s | $0.50 | video+audio | **8.8** (2.9, 4.7) |
| SN3_w3c | 1 | - | done | `556e6ef1-c5fc-4ad9-aa36-74e8ee0e04f1` | 130.7 | 5 s | $0.50 | video+audio | **6.5** (3.0, 28.2) |
| SN6_w3c | 1 | - | done | `35ed75a9-976f-4d2c-acb1-a36c2fa5ee67` | 114.9 | 5 s | $0.50 | video+audio | **12.5** (4.9, 5.8) |
| A6_w3c | 0 | first = last = keyframe | done | `ef91d918-1ed8-42d0-9a18-c3501edc0984` | 100.9 | 5 s | $0.50 | video+audio | **1.6** (5.2, 5.0) |

**Seam method:** OpenCV (`cv2` 4.13), the pilot's one-liner: frame 0 vs the last of 150 frames, mean abs BGR difference, 0–255.
**A6_w3c vs its keyframe**, same metric: frame 0 = **2.7**, last frame = **2.9**. Both end frames land on the locked empty-gate still.
**Contact sheets:** 5×2, every 15th frame, 216 wide. **Loop previews:** `-stream_loop 2 -c copy`, 15.16 s.

## Paths
Working copies (`C:\Projects\opencode\video_image\songs\shorts-learning\out\`)
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\<id>-seed30313-w3.mp4` (+ `.json`), for id = SN1_w3c, SN2_w3c, SN3_w3c, SN6_w3c, A6_w3c
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\<id>-strip.png`, `<id>-contact.png`, `<id>-loop-x3.mp4` (same ids)
- Keyframe: `C:\Projects\opencode\video_image\songs\shorts-learning\keyframes\A6-gate-empty.png`
- Log: `C:\Projects\opencode\video_image\songs\shorts-learning\batch_learning4.log`

Copies. Each folder went from 7 to 10 files and the no-overwrite guard hit nothing. `<ID>-metadata.md` and the earlier w3/w3b
clips are untouched.
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN1\SN1_w3c-seed30313-w3.mp4`, `...\SN1\SN1_w3c-contact.png`, `...\SN1\SN1_w3c-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN2\SN2_w3c-seed30313-w3.mp4`, `...\SN2\SN2_w3c-contact.png`, `...\SN2\SN2_w3c-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN3\SN3_w3c-seed30313-w3.mp4`, `...\SN3\SN3_w3c-contact.png`, `...\SN3\SN3_w3c-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN6\SN6_w3c-seed30313-w3.mp4`, `...\SN6\SN6_w3c-contact.png`, `...\SN6\SN6_w3c-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A6\A6_w3c-seed30313-w3.mp4`, `...\A6\A6_w3c-contact.png`, `...\A6\A6_w3c-loop-x3.mp4`

## Commit
The `[skip ci]` commit containing this report. It holds the four `shots/SN*-w3c.txt` files and `A6-w3c.txt`, `shots.csv`,
`keyframes/A6-gate-empty.png` (added with `-f`), `REVIEW-learning-batch1-2026-09-29.md`, the queue folder and this report.
The hash is in CC's chat reply.

## Not judged
Fable reviews.
