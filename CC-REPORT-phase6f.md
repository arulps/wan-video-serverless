# CC-REPORT — Phase 6f: L01 Peekaboo on Wan 3.0, pass 1: silent + "Peekaboo!" voice (2026-09-28)

**Result: 2/2 rendered, est $1.00 at list price** (~$0.70 with the 30% discount; cap $1.10). No pod. Both were upscaled
to vertical 4K, and the voice clip kept its audio.

## A — check
- `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
  It now passes **without** `PYTHONUTF8`, so the Windows fix works.
- `credentials present: True`. Dry-run: 2 rows, `L01_w3r` `audio=off` and `L01_w3v` `audio=on`, 720P 9:16 5 s, 1 ref (Minnu),
  `estimated $1.00`.

## B — render
- Window: **16:51:16 → 16:53:51 UTC** (12:51:16 → 12:53:51 Toronto EDT). Two tasks ran in parallel, with no errors.
- I have no access to the console's itemised bill. Arul: check under Usage & Billing whether `f9a1e88a…` (with audio)
  was charged differently from `bc87c505…`. The API's `usage` block is identical for both and has no audio field.

| row | task id | wall s | usage | est (list) | audio stream: native | audio stream: 4K |
|---|---|---|---|---|---|---|
| L01_w3r | `bc87c505-563c-4f62-9aa5-28d6aa92b7d4` | 147.4 | duration 5.0, output_video_duration 5.0, fps 30, video_count 1, SR 720, ratio 9:16 | $0.50 | **no** (`h264,video`) | **no** |
| L01_w3v | `f9a1e88a-bd74-4683-9835-c7e69f8f457a` | 147.4 | same | $0.50 | **yes** (`aac,audio,44100`) | **yes** (`aac,audio,44100`) |

- Both natives are 720×1280 @ 30 fps, 150 frames. The sidecar `params.audio` is False for `w3r` and True for `w3v`.
- No URL or key appears in either sidecar or in `batch_6f.log` (grepped).

## C — frames, upscale, copies
- **Frame folders:** every 10th frame, 15 PNGs each, `f001`–`f015` = frames 0, 10 … 140.
  `fNNN` = frame (NNN−1)×10.
- **Contact sheets:** 8×2 tiles at 270 wide, 2160×960; 15 tiles plus 1 empty.
- **Upscale** (Vulkan, Intel Iris Xe): `ncnn scale x3` → 2160×3840 @ 30 fps, 150 frames, interpolation `none`.

| clip | decode / upscale / encode s | s/frame |
|---|---|---|
| L01_w3r | 9.4 / 1181.5 / 133.4 | 7.88 |
| L01_w3v | 8.5 / 1127.3 / 137.9 | 7.52 |

## Paths
Native (`C:\Projects\opencode\video_image\songs\shorts-loops\out\`)
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L01_w3r-seed30313-w3.mp4`, `...\out\L01_w3r-seed30313-w3.json`, `...\out\_qc\L01_w3r-strip.png`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L01_w3v-seed30313-w3.mp4`, `...\out\L01_w3v-seed30313-w3.json`, `...\out\_qc\L01_w3v-strip.png`
- Log: `C:\Projects\opencode\video_image\songs\shorts-loops\batch_6f.log`

Contact sheets and frame folders
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L01_w3r-seed30313-w3-contact.png`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L01_w3v-seed30313-w3-contact.png`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L01_w3r-seed30313-w3-frames\` (f001–f015)
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L01_w3v-seed30313-w3-frames\` (f001–f015)

4K
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\4K\L01_w3r-seed30313-w3-4K.mp4` (+ `.mp4.json`)
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\4K\L01_w3v-seed30313-w3-4K.mp4` (+ `.mp4.json`)

Copies (`C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\wan3\`)
- `...\wan3\L01_w3r-seed30313-w3.mp4`, `...\wan3\L01_w3v-seed30313-w3.mp4`
- `...\wan3\L01_w3r-seed30313-w3-4K.mp4`, `...\wan3\L01_w3v-seed30313-w3-4K.mp4`
- `...\wan3\L01_w3r-seed30313-w3-contact.png`, `...\wan3\L01_w3v-seed30313-w3-contact.png`

## Commit
The `[skip ci]` commit that contains this report. It holds `shots.csv` (2× done), the two shot files, `batch_runner.py`,
`test_wan3_mock.py`, the 6f dispatch and this report. The hash is in CC's chat reply.

## Not judged
Fable picks the best face-out frame for pass 2.
