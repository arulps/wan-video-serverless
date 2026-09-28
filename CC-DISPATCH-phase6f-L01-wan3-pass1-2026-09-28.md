# CC-DISPATCH — Phase 6f: L01 Peekaboo on Wan 3.0, pass 1 — silent + "Peekaboo!" voice test (2026-09-28)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine). One go, A → C.
**Budget: API ≤ $1.10 list (two 5 s 720p clips, ~$0.70 with the 30% discount).** No pod. Never print `.env` values,
the key, the workspace id or any video URL. Edit `shots.csv` cells only. Commits `[skip ci]`. Report **full Windows paths**.

## 0 · Why
Wan 3.0 cannot combine character references with first/last frames in one call. Pass 1 renders L01 from Minnu's
reference picture and a clear prompt (hidden → peekaboo → hidden). Fable then picks the best "face out" frame; pass 2
(later) uses it as first = last frame, which guarantees the loop. Arul also wants to hear Wan 3.0's own sound once:
`L01_w3v` is the same shot with audio ON and Minnu calling "Peekaboo!" in a little girl's voice (Tamil, if wanted,
is dubbed in CapCut).

## 1 · On disk (Fable; dry-run + mock verified)
- `songs/shorts-loops/shots/L01-w3.txt` (silent) and `L01-w3-voice.txt` (same + she calls "Peekaboo!" once in a bright
  little girl's voice; sound = only that word + soft room tone, no music).
- `songs/shorts-loops/shots.csv` — new column `audio` (blank = off) and rows `L01_w3r` (silent) and `L01_w3v` (audio=yes):
  `engine=wan3`, `ref=refs/minnu-body-9x16.png`, `ref_labels=Minnu`, 720x1280, 5 s, seed 30313, standard.
- `comfy/batch_runner.py` — `audio` column for wan3 rows (yes/no → the API's `audio` flag; recorded in the sidecar;
  dry-run prints `audio=on|off`).
- `tests/test_wan3_mock.py` — Windows fix from 6e (subprocess output read as UTF-8).

## Part A — check ($0)
```
python tests\test_wan3_mock.py        -> PASS (no PYTHONUTF8 needed now)
python comfy\batch_runner.py --song songs\shorts-loops --hosts api --dry-run --only L01_w3r,L01_w3v   -> 2 rows, audio=off / audio=on, est $1.00
```

## Part B — render (≤ $1.10)
```
python comfy\batch_runner.py --song songs\shorts-loops --only L01_w3r,L01_w3v --hosts api,api --max-usd 1.10 --timeout-min 30 2>&1 | tee songs\shorts-loops\batch_6f.log
```
If a task fails on auth/region/model/quota: stop and report the `code: message` line; no retry. Afterwards check each
file with `ffprobe -v error -show_entries stream=codec_type,codec_name,sample_rate -of csv=p=0 <file>`: L01_w3v must
have an audio stream, L01_w3r must not — report both.

## Part C — frames for Fable, upscale, copy, commit ($0)
In `songs\shorts-loops\out\`, for each `$c` in `L01_w3r-seed30313-w3`, `L01_w3v-seed30313-w3`:
```
mkdir _qc\$c-frames
ffmpeg -y -i $c.mp4 -vf "select='not(mod(n\,10))',scale=270:-2,tile=8x2" -vsync 0 -frames:v 1 _qc\$c-contact.png
ffmpeg -y -i $c.mp4 -vf "select='not(mod(n\,10))'" -vsync 0 _qc\$c-frames\f%03d.png
powershell -ExecutionPolicy Bypass -File ..\..\..\scripts\upscale.ps1 "$c.mp4" -Dst "4K\$c-4K.mp4" -Height 3840
```
(Write the literal names — check every output path. `fNNN.png` = frame (NNN-1)×10: f001 = frame 0, f002 = frame 10 …)
The upscaler copies the source audio; confirm the 4K L01_w3v still has its audio stream (ffprobe).
Copy both mp4s, both 4K files and both contact sheets to `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\wan3\`.
Commit `songs/shorts-loops/shots.csv`, `songs/shorts-loops/shots/L01-w3.txt`, `songs/shorts-loops/shots/L01-w3-voice.txt`,
`comfy/batch_runner.py`, `tests/test_wan3_mock.py`, this dispatch and `CC-REPORT-phase6f.md` with `[skip ci]`; push.

## Report — `CC-REPORT-phase6f.md`
Test line; per row: task id, wall s, `usage`, list estimate, audio stream yes/no (native and 4K); UTC/Toronto time window
(for the console bill — note whether the audio clip shows a different charge, if the console itemises it); upscale
sidecar values; full Windows paths of mp4s, jsons, strips, contact sheets, frame folders, 4K files and the copies;
commit hash. **Do not judge the clips.**
