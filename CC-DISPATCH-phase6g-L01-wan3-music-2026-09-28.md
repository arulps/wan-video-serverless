# CC-DISPATCH — Phase 6g: L01 Peekaboo on Wan 3.0 with generated loopable music (2026-09-28)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine). One go, A → C.
**Budget: API ≤ $0.55 list (one 5 s 720p clip, ~$0.35 with the discount).** No pod. Never print `.env` values, the key,
the workspace id or any video URL. Edit `shots.csv` cells only. Commits `[skip ci]`. Report **full Windows paths**.

## 0 · Why
Arul wants to hear Wan 3.0's own music: row `L01_w3m` = the 6f voice shot (same ref, seed, framing) plus a sound line
asking for a gentle toddler melody (soft xylophone + ukulele) at one steady tempo, written as a seamless loop with no
intro/ending, dipping under her one "Peekaboo!". The question is whether generated music can survive the loop point.

## 1 · On disk (Fable; dry-run verified)
- `songs/shorts-loops/shots/L01-w3-music.txt`; `shots.csv` row `L01_w3m` (`engine=wan3`, `audio=yes`, 720x1280, 5 s, seed 30313).

## Part A — check ($0)
`python comfy\batch_runner.py --song songs\shorts-loops --hosts api --dry-run --only L01_w3m` → 1 row, `audio=on`, est $0.50.

## Part B — render (≤ $0.55)
```
python comfy\batch_runner.py --song songs\shorts-loops --only L01_w3m --hosts api --max-usd 0.55 --timeout-min 30 2>&1 | tee songs\shorts-loops\batch_6g.log
```
Auth/region/model/quota failure → stop, report the `code: message` line; no retry.

## Part C — checks, upscale, copies, commit ($0)
In `songs\shorts-loops\out\`:
```
ffprobe -v error -show_entries stream=codec_type,codec_name,sample_rate -of csv=p=0 L01_w3m-seed30313-w3.mp4
for %s in (0 0.5 1 1.5 2 2.5 3 3.5 4 4.5) do @ffmpeg -v info -ss %s -t 0.5 -i L01_w3m-seed30313-w3.mp4 -vn -af volumedetect -f null - 2>&1 | findstr mean_volume
ffmpeg -y -i L01_w3m-seed30313-w3.mp4 -vf "select='not(mod(n\,10))',scale=270:-2,tile=8x2" -vsync 0 -frames:v 1 _qc\L01_w3m-seed30313-w3-contact.png
ffmpeg -y -stream_loop 2 -i L01_w3m-seed30313-w3.mp4 -c copy "C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\wan3\L01_w3m-loop-x3-preview.mp4"
powershell -ExecutionPolicy Bypass -File ..\..\..\scripts\upscale.ps1 "L01_w3m-seed30313-w3.mp4" -Dst "4K\L01_w3m-seed30313-w3-4K.mp4" -Height 3840
```
(The `for` line is cmd syntax — run it in cmd, or do the same ten windows in PowerShell. It prints the loudness per half
second: music throughout should show no near-silent windows.) Confirm the 4K file keeps its audio stream.
Copy the mp4, the 4K file and the contact sheet to `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\wan3\`.
Commit `songs/shorts-loops/shots.csv`, `songs/shorts-loops/shots/L01-w3-music.txt`, `songs/shorts-loops/REVIEW-L01-wan3-2026-09-28.md`,
this dispatch and `CC-REPORT-phase6g.md` with `[skip ci]`; push.

## Report — `CC-REPORT-phase6g.md`
Task id, wall s, `usage`, list estimate, UTC/Toronto window; audio stream (native + 4K); the ten loudness values;
upscale sidecar values; full Windows paths (mp4, json, strip, contact sheet, 4K, loop preview, copies); commit hash.
**Do not judge the clip** — Arul listens; Fable checks the picture.
