# CC-REPORT — Learning batch 2: animals A1–A6 + 3 retakes on Wan 3.0 (2026-09-29)

Queue `queue\2026-09-29-learning-batch2`. **Result: 9/9 rendered, 0 failed. Estimate $4.50 at list price** (~$3.15 with the
30% discount; cap $5.00). 720p 9:16 5 s with sound, no upscale, no pod.

- Credentials: `credentials present: True`.
- Dry-run: 9 rows, all `audio=on`. A1–A6 refs=0; MN1_w3b/MN3_w3b (Mintu) and VG3_w3b (Minnu) refs=1 at seed 4242.
  **Estimated $4.50**, no MISSING or ERROR.
- **Render window:** **16:06:25 → 16:15:57 UTC, 2026-09-29** (12:06:25 → 12:15:57 Toronto EDT). 3 tasks in parallel.
- All 9 have video + audio. No URL or key appears in any sidecar or the log. The 9 `shots.csv` status cells are `done`.

| row | seed | refs | status | task id | wall s | length | est (list) | seam |
|---|---|---|---|---|---|---|---|---|
| A1_w3 | 30313 | 0 | done | `a5f543e6-21a9-439b-b882-20368ee45a41` | 272.5 | 5 s | $0.50 | **5.5** |
| A2_w3 | 30313 | 0 | done | `a8051cb4-dfe5-469d-ac3b-de1ecf9e52f2` | 272.8 | 5 s | $0.50 | **5.3** |
| A3_w3 | 30313 | 0 | done | `80386683-c7b0-48e3-b1b0-e3fe8da1ea78` | 273.5 | 5 s | $0.50 | **5.3** |
| A4_w3 | 30313 | 0 | done | `ca3bf619-f02d-4ffd-8470-23fc814e6669` | 98.3 | 5 s | $0.50 | **6.0** |
| A5_w3 | 30313 | 0 | done | `3eb35cfe-fea8-456b-93b6-a8a932a99f03` | 97.8 | 5 s | $0.50 | **5.0** |
| A6_w3 | 30313 | 0 | done | `7ea2143a-9445-433b-b59d-f8fe8e0bf427` | 145.7 | 5 s | $0.50 | **5.2** |
| MN1_w3b | 4242 | 1 | done | `af5c96d5-a326-4d2f-9c5f-c1c91fda87e5` | 146.2 | 5 s | $0.50 | **8.8** (batch 1 MN1_w3: 7.8) |
| MN3_w3b | 4242 | 1 | done | `410231c1-1cf4-4652-8b3a-737663dc17fc` | 147.8 | 5 s | $0.50 | **9.3** (batch 1 MN3_w3: 9.9) |
| VG3_w3b | 4242 | 1 | done | `5158cf3e-480f-4a20-acfd-71b8c5b4f340` | 148.2 | 5 s | $0.50 | **8.1** (batch 1 VG3_w3: 6.5) |

**Seam method:** OpenCV (`cv2` 4.13), the pilot's one-liner: frame 0 vs the last of 150 frames, mean abs BGR difference, 0–255.
**Contact sheets:** 5×2, every 15th frame, 216 wide. **Loop previews:** `-stream_loop 2 -c copy`, 15.16 s.
Note: A1–A3 took ~273 s wall each, against ~98–148 s for the others. That is API queue time, not an error.

## Paths
Working copies (`C:\Projects\opencode\video_image\songs\shorts-learning\out\`)
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\A1_w3-seed30313-w3.mp4` … `A6_w3-seed30313-w3.mp4` (+ `.json` each)
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\MN1_w3b-seed4242-w3.mp4`, `MN3_w3b-seed4242-w3.mp4`, `VG3_w3b-seed4242-w3.mp4` (+ `.json` each)
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\<id>-strip.png`, `<id>-contact.png`, `<id>-loop-x3.mp4`, for id = A1_w3 … A6_w3, MN1_w3b, MN3_w3b, VG3_w3b
- Log: `C:\Projects\opencode\video_image\songs\shorts-learning\batch_learning2.log`

Copies. Each folder gained exactly 3 files and the no-overwrite guard hit nothing. `<ID>-metadata.md` and the batch-1
MN1/MN3/VG3 clips are untouched.
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A1\A1_w3-seed30313-w3.mp4`, `...\A1\A1_w3-contact.png`, `...\A1\A1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A2\A2_w3-seed30313-w3.mp4`, `...\A2\A2_w3-contact.png`, `...\A2\A2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A3\A3_w3-seed30313-w3.mp4`, `...\A3\A3_w3-contact.png`, `...\A3\A3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A4\A4_w3-seed30313-w3.mp4`, `...\A4\A4_w3-contact.png`, `...\A4\A4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A5\A5_w3-seed30313-w3.mp4`, `...\A5\A5_w3-contact.png`, `...\A5\A5_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A6\A6_w3-seed30313-w3.mp4`, `...\A6\A6_w3-contact.png`, `...\A6\A6_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\MN1\MN1_w3b-seed4242-w3.mp4`, `...\MN1\MN1_w3b-contact.png`, `...\MN1\MN1_w3b-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\MN3\MN3_w3b-seed4242-w3.mp4`, `...\MN3\MN3_w3b-contact.png`, `...\MN3\MN3_w3b-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\VG3\VG3_w3b-seed4242-w3.mp4`, `...\VG3\VG3_w3b-contact.png`, `...\VG3\VG3_w3b-loop-x3.mp4`

## Commit
The `[skip ci]` commit containing this report. It holds `_make_shots.py`, `shots/A1–A6-w3.txt` and the three `-w3b` shot files,
`world-garden-gate.txt`, `shots.csv`, `REVIEW-learning-batch1-2026-09-29.md`, the queue folder and this report.
The hash is in CC's chat reply.

## Not judged
Fable reviews.
