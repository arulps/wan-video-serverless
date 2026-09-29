# CC-REPORT — Learning batch 3: cartoon-style retakes for the home sounds + 2 animals, on Wan 3.0 (2026-09-29)

Queue `queue\2026-09-29-learning-batch3`. **Result: 7/7 rendered, 0 failed. Estimate $3.50 at list price** (~$2.45 with the
30% discount; cap $4.00). 720p 9:16 5 s with sound, seed 4242, no refs, no upscale, no pod.

- Credentials: `credentials present: True`.
- Dry-run: 7 rows, all `audio=on`, refs=0, **estimated $3.50**, no MISSING or ERROR.
- **Render window:** **16:21:38 → 16:26:34 UTC, 2026-09-29** (12:21:38 → 12:26:34 Toronto EDT). 3 tasks in parallel.
- All 7 have video + audio. No URL or key appears in any sidecar or the log. The 7 `shots.csv` status cells are `done`.
- The generator change ("cartoon object style" + "one continuous shot") was already committed in `4b9be1f`. The new
  `-w3b` shot files contain it.

| row | refs | status | task id | wall s | length | est (list) | streams | seam (earlier w3) |
|---|---|---|---|---|---|---|---|---|
| SN1_w3b | 0 | done | `96a9a6ac-0926-4a6b-84d4-0fbb73266af3` | 98.1 | 5 s | $0.50 | video+audio | **3.2** (3.1) |
| SN2_w3b | 0 | done | `e0e9361a-f4e5-4897-9ce3-030e41bfcead` | 98.3 | 5 s | $0.50 | video+audio | **4.7** (2.9) |
| SN3_w3b | 0 | done | `2bc4c258-c93b-41be-939e-34f165d6c384` | 98.1 | 5 s | $0.50 | video+audio | **28.2** (3.0) |
| SN4_w3b | 0 | done | `a07e689f-ce36-4a00-b9ec-15a6d9c7582c` | 97.7 | 5 s | $0.50 | video+audio | **11.2** (3.7) |
| SN6_w3b | 0 | done | `e90b7ffc-6410-411c-b548-7ce9994f6b9c` | 129.7 | 5 s | $0.50 | video+audio | **5.8** (4.9) |
| A3_w3b | 0 | done | `7f0b3df4-e477-40e9-9bf1-6a45dfab425d` | 97.5 | 5 s | $0.50 | video+audio | **5.1** (5.3) |
| A6_w3b | 0 | done | `5c70f8c3-8084-4973-8970-6358b2d12086` | 98.0 | 5 s | $0.50 | video+audio | **5.0** (5.2) |

**Seam method:** OpenCV (`cv2` 4.13), the pilot's one-liner: frame 0 vs the last of 150 frames, mean abs BGR difference, 0–255.
The "earlier w3" values are the first versions from batch 1 (SN) and batch 2 (A).

**Numbers only, not a judgment:** SN3_w3b (28.2) and SN4_w3b (11.2) end noticeably further from their first frame than the
originals did. Fable should check those two loop previews.

**Contact sheets:** 5×2, every 15th frame, 216 wide. **Loop previews:** `-stream_loop 2 -c copy`, 15.16 s.

## Paths
Working copies (`C:\Projects\opencode\video_image\songs\shorts-learning\out\`)
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\<id>-seed4242-w3.mp4` (+ `.json`), for id = SN1_w3b, SN2_w3b, SN3_w3b, SN4_w3b, SN6_w3b, A3_w3b, A6_w3b
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\<id>-strip.png`, `<id>-contact.png`, `<id>-loop-x3.mp4` (same ids)
- Log: `C:\Projects\opencode\video_image\songs\shorts-learning\batch_learning3.log`

Copies. Each folder went from 4 to 7 files and the no-overwrite guard hit nothing. `<ID>-metadata.md` and the earlier w3 clips
are untouched.
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN1\SN1_w3b-seed4242-w3.mp4`, `...\SN1\SN1_w3b-contact.png`, `...\SN1\SN1_w3b-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN2\SN2_w3b-seed4242-w3.mp4`, `...\SN2\SN2_w3b-contact.png`, `...\SN2\SN2_w3b-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN3\SN3_w3b-seed4242-w3.mp4`, `...\SN3\SN3_w3b-contact.png`, `...\SN3\SN3_w3b-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN4\SN4_w3b-seed4242-w3.mp4`, `...\SN4\SN4_w3b-contact.png`, `...\SN4\SN4_w3b-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN6\SN6_w3b-seed4242-w3.mp4`, `...\SN6\SN6_w3b-contact.png`, `...\SN6\SN6_w3b-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A3\A3_w3b-seed4242-w3.mp4`, `...\A3\A3_w3b-contact.png`, `...\A3\A3_w3b-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\A6\A6_w3b-seed4242-w3.mp4`, `...\A6\A6_w3b-contact.png`, `...\A6\A6_w3b-loop-x3.mp4`

## Commit
The `[skip ci]` commit containing this report. It holds `songs/shorts-learning/shots/`: the 7 new `-w3b` files and Fable's
regenerated w3 shot files (A1–A6, OP3, SN1–SN4, SN6, V1, V2, V4). It also holds `shots.csv`, the queue folder and this report.
`_make_shots.py` is unchanged since `4b9be1f`, so its add was a no-op.
Not committed: Fable's uncommitted edit to `REVIEW-learning-batch1-2026-09-29.md`, which is not in this queue's list.
The hash is in CC's chat reply.

## Not judged
Fable reviews.
