# CC-REPORT — Tamil voice test: C1 red ball with a Tamil voice, 2 variants, on Wan 3.0 (2026-09-30)

Queue `queue\2026-09-30-tamil-voice-test`. **Result: 2/2 rendered. Estimate $1.00 at list price** (~$0.70 with the 30% discount;
cap $1.20). Same shot as `C1_w3` (Minnu, red ball, seed 30313); only the voice lines differ. 720p 9:16 5 s with sound, no pod.

- Credentials: `credentials present: True`.
- Dry-run: 2 rows, `audio=on`, refs=1 (Minnu), **estimated $1.00**, no MISSING or ERROR.
- **Render window:** **03:27:10 → 03:30:14 UTC, 2026-10-01** (23:27:10 → 23:30:14 Toronto EDT, 2026-09-30). 2 tasks in parallel.
- Both have `h264` video + `aac` 44.1 kHz audio. No URL or key appears in the sidecars or the log. Both `shots.csv` statuses are `done`.

| row | voice lines as sent (from the sidecar prompt) | task id | wall s | est (list) | seam |
|---|---|---|---|---|---|
| C1_w3ta | Tamil script: "இது என்ன நிறம்?" → "சிவப்பு!" → "சிவப்பு பந்து!" | `cd84ea2d-1d91-4843-9a9c-a39db49233d9` | 178.8 | $0.50 | **7.5** |
| C1_w3tr | Latin: "Idhu enna niram?" → "Sivappu!" → "Sivappu pandhu!" | `b242bb4c-67eb-44aa-8fd4-8fa4f468de27` | 178.8 | $0.50 | **7.3** |

- **Encoding check:** the prompt recorded in C1_w3ta's sidecar contains all 31 Tamil characters, with the three lines verbatim.
  The Tamil script reached the API intact, not as mojibake. Both prompts frame it as "a warm, cheerful off-screen female voice
  speaks slowly and clearly in Tamil, with natural Tamil pronunciation".
- **Loudness, numbers only** (`volumedetect` mean per 1-second window, 0–4 s):
  - C1_w3ta −14.9 / −28.2 / −16.2 / −16.3 / −34.7 dB;
  - C1_w3tr −14.8 / −21.5 / −16.7 / −14.5 / −29.6 dB.
  - Both are loudest at 0–1 s and 2–4 s, which is where the lines fall.
- **Seam method:** OpenCV (`cv2` 4.13), the pilot's one-liner: frame 0 vs the last of 150 frames, 0–255. For comparison, the
  English C1_w3 was 7.6.
- **Contact sheets:** 5×2, every 15th frame. **Loop previews:** `-stream_loop 2 -c copy`, 15.16 s.
- **Audio extracts:** `ffmpeg -i <clip> -vn -ac 1 -ar 44100`, mono, 44.1 kHz, 5.04 s each.

## Paths
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\C1_w3ta-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\C1_w3tr-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\C1_w3ta-strip.png`, `C1_w3ta-contact.png`, `C1_w3ta-loop-x3.mp4`, **`C1_w3ta-audio.wav`**
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\C1_w3tr-strip.png`, `C1_w3tr-contact.png`, `C1_w3tr-loop-x3.mp4`, **`C1_w3tr-audio.wav`**
- Log: `C:\Projects\opencode\video_image\songs\shorts-learning\batch_tamil_test.log`

Copies. The C1 folder went from 9 to 15 files and the no-overwrite guard hit nothing. `C1-metadata.md`, `C1_short_1080x1920_wm.mp4`,
`C1_thumbnail.png`, the C1_w3 and `-objectonly` files, and `renders-learning\USE-CLIPS.md` are untouched.
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C1\C1_w3ta-seed30313-w3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C1\C1_w3ta-contact.png`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C1\C1_w3ta-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C1\C1_w3tr-seed30313-w3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C1\C1_w3tr-contact.png`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C1\C1_w3tr-loop-x3.mp4`

## Commit
The `[skip ci]` commit containing this report. It holds `shots/C1-w3ta.txt`, `shots/C1-w3tr.txt`, `shots.csv`, the queue folder and
this report. The hash is in CC's chat reply. Not committed: Fable's uncommitted edit to `REVIEW-learning-batch1-2026-09-29.md`,
which is not in this queue's list.

## Not judged
Fable and Arul listen: which variant Wan pronounces better.
