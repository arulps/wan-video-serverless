# CC-REPORT — Phase 6g: L01 Peekaboo on Wan 3.0 with generated loopable music (2026-09-28)

**Result: 1/1 rendered, est $0.50 at list price** (~$0.35 with the discount; cap $0.55). No pod.

## A — check
- `credentials present: True`.
- Dry-run `--only L01_w3m`: 1 row, `wan3.0-video 720P 9:16 5s audio=on`, 1 ref (Minnu), `estimated $0.50`.

## B — render
| task id | wall s | usage | est (list) |
|---|---|---|---|
| `ab90348f-3372-4e3a-98c5-9be104d97249` | 131.3 | duration 5.0, input_video_duration 0.0, output_video_duration 5.0, fps 30, video_count 1, SR 720, ratio 9:16 | $0.50 |

- Window: **19:28:12 → 19:30:25 UTC** (15:28:12 → 15:30:25 Toronto EDT). No errors.
- Sidecar `params.audio` = True. No URL or key appears in the sidecar or in `batch_6g.log` (grepped).

## C — checks
- **Audio stream:** native `h264,video` + **`aac,audio,44100`** (duration 5.04 s). 4K: `h264,video,2160,3840` + **`aac,audio,44100`**.
- **Loudness** (`volumedetect` mean over each half-second window):

| start s | 0 | 0.5 | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| mean dB | −22.7 | −24.1 | −25.6 | −14.3 | −14.7 | −29.0 | −26.2 | −23.4 | −24.7 | −24.9 |

  - Every window lies between −29 and −14 dB. There is no near-silent window; compare the 6f voice-only clip's −50 to −65 dB outside its word.
  - The first window (−22.7) and the last (−24.9) are about 2 dB apart.
- **Upscale** (Vulkan, Intel Iris Xe): `ncnn scale x3` → 2160×3840 @ 30 fps, 150 frames, interpolation `none`,
  decode / upscale / encode 10.5 / 1128.5 / 96.3 s (**7.52 s/frame**). The source audio was kept.
- **Loop preview:** `-stream_loop 2 -c copy`, 15.16 s (3 × 5.04 s).

## Paths
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L01_w3m-seed30313-w3.mp4`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L01_w3m-seed30313-w3.json`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L01_w3m-strip.png`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L01_w3m-seed30313-w3-contact.png`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\4K\L01_w3m-seed30313-w3-4K.mp4` (+ `.mp4.json`)
- Log: `C:\Projects\opencode\video_image\songs\shorts-loops\batch_6g.log`
- Loop preview, written directly to the review folder:
  `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\wan3\L01_w3m-loop-x3-preview.mp4`
- Copies in `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\wan3\`:
  - `L01_w3m-seed30313-w3.mp4`
  - `L01_w3m-seed30313-w3-4K.mp4`
  - `L01_w3m-seed30313-w3-contact.png`

## Commit
The `[skip ci]` commit that contains this report. It holds `shots.csv` (L01_w3m `done`), `shots/L01-w3-music.txt`,
`REVIEW-L01-wan3-2026-09-28.md`, the 6g dispatch and this report. The hash is in CC's chat reply.

## Not judged
Arul listens (music at the loop point, "Peekaboo!"); Fable checks the picture.
