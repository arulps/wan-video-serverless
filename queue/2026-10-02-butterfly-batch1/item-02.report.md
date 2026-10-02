# item-02 report — second half (67 s, ≤ $7.00 list), sheets, stand-in test, commit

## 1. Render, second half
**Window: 21:16:10 → 22:06:51 UTC, 2026-10-02** (17:16:10 → 18:06:51 Toronto EDT). One at a time, `--max-usd 7.00`; the runner exited 0.
V6b's 1147 s wall time was API queue time; it SUCCEEDED like the rest.

| clip | status | task id | wall s | length | frames | refs | est (list) | stills | every10 |
|---|---|---|---|---|---|---|---|---|---|
| V4a | done | `17e3ee74-ab18-498d-8b0d-9aabe0d05d52` | 195.5 | 5 s | 150 | 5 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V4b | done | `3006d6da-4b17-4e53-a6a9-0eaa6b6c0e34` | 132.3 | 5 s | 150 | 5 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V4c | done | `fbcfa004-3bfc-4cf4-a67c-22b25c9e912a` | 132.4 | 5 s | 150 | 5 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V4d | done | `1a8b86d5-ca84-41b5-a3eb-c092198b154d` | 133.6 | 5 s | 150 | 5 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V5b | done | `1f5cae96-f9c9-4cc7-9239-81a3ae77b1c1` | 148.5 | 5 s | 150 | 8 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V5c | done | `beb27125-f540-4391-9d61-cd4017e7fb8b` | 148.9 | 5 s | 150 | 8 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V5d | done | `c18b9a72-e7d0-4afc-9b26-79ccecde5bf0` | 164.0 | 5 s | 150 | 8 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V6a | done | `3ce8eb51-3fe1-4114-a5fa-c527794aa5c4` | 149.0 | 5 s | 150 | 8 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V6b | done | `a6bdb8ca-86d0-46ee-b41c-b3772e3a2350` | 1147.1 | 5 s | 150 | 8 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V6c | done | `8b6387fd-07cf-444f-bbf3-1b5829d60221` | 165.1 | 5 s | 150 | 8 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V6d | done | `c65b281a-2ced-42b8-820b-1c43dc926489` | 165.3 | 5 s | 150 | 8 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| O3 | done | `2e6a1850-71b6-465c-8a18-a5c6a7ce9bae` | 166.2 | 5 s | 150 | 8 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| O4 | done | `305041f1-c3f4-4902-a104-fcb805f96ff1` | 182.2 | 7 s | 210 | 8 | $0.70 | f000/f104/f209 | 21 frames 7x3 1792x432 |

- **Second half: 13/13 done, 67 s, estimated $6.70 at list price** (cap $7.00).
- **Failures:** none. All are 1280×720 @ 30 fps (frames counted by ffprobe), video only. Each sidecar prompt equals its `*.raw.txt`.
  No URL or key appears in the sidecars or in the log `C:\Projects\opencode\video_image\songs\a07-butterfly\batch1b.log`.

## 2. Sheets and stills
In `C:\Projects\opencode\video_image\songs\a07-butterfly\out\_qc\`, per clip:
- `<ID>-every10.png`: every 10th frame, 256 wide; O4 7×3 (21 frames → 1792×432), the others 5×3 (15 → 1280×432);
- `<ID>-f000.png` / `-fMID` / `-fLAST` (O4: f000/f104/f209; 5 s clips: f000/f074/f149), 1280×720;
- `<ID>-strip.png` (written by the runner).

Clips: `C:\Projects\opencode\video_image\songs\a07-butterfly\out\<ID>-seed30313-w3.mp4` (+ `.json`), for ID = V4a, V4b, V4c, V4d,
V5b, V5c, V5d, V6a, V6b, V6c, V6d, O3, O4.

## 3. Stand-in test
`python tests\test_song_cuts_reuse.py` → exit 0. The log is `C:\Projects\opencode\video_image\songs\a07-butterfly\cuts_standin2.log`.
- `PASS: rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit, both stand-in cuts frame-exact`
- `wrote …\A07-BUTTERFLY-ROUGH-TA-PREVIEW.mp4 6481 video frames = plan 6481; container 216.040 s (audio 216.040 s)`
- `wrote …\A07-BUTTERFLY-ROUGH-EN-PREVIEW.mp4 6665 video frames = plan 6665; container 222.167 s (audio 222.160 s)`
- The previews were made in a temp folder (deleted by the test).

## Queue totals
- item-01 $7.20 + item-02 $6.70 = **$13.90 at list price** for 27 clips / 139 s (~$9.73 with the 30% discount); cap $14.50.
- **IDs whose status is not `done`: none.** All 33 rows in `songs\a07-butterfly\shots.csv` are `done` (the 27 from this queue +
  RA, RB, V1a, V2a, V2b, V5a kept from the gates).
- The 79 files that were in `out\` before this queue (kept takes + review images) are md5 unchanged.
- Nothing was written to `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`. Its newest file is from 16:04, before this queue
  started at 16:40; those are Fable's rev 3.5 runsheet/json/html. `songs\rowboat\` was not touched.

## 4. Commit
The `[skip ci]` commit containing this file. It holds `songs/a07-butterfly/` except `out/` (rev 3.5 `shots/*.raw.txt`, `shots.csv`
with all 33 `done`, the batch and stand-in logs) and the queue folder. The hash is in CC's chat reply.
