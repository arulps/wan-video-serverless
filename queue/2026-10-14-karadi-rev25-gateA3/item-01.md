# item-01 — client update, checks, render HKa, QC sheets (HKa + O1), slot cuts with the music, commit (≤ $0.90 list)

1. **Client update** (Fable wrote the files; verify, don't edit): `comfy\wan3_api.py` contains `def _never_sent(`;
   `py -m py_compile comfy\wan3_api.py` → no output; `py tests\test_wan3_retry_mock.py` → `PASS test_wan3_retry_mock: 10 checks`;
   `py tests\test_wan3_mock.py` → PASS. Credentials check → True (print only True/False).
2. Checks (verify, don't edit): `shots.csv` has HKa `failed` or `todo`, O1 `done`; `out\O1-seed30313-w3.mp4` exists (210 frames);
   `out\` has no `HKa-seed30313-w3.mp4`; `shots\05_HKa.raw.txt` contains "the children do their own quick full turn beside him";
   `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`. Any mismatch → **blocked**.
3. Dry-run: `py comfy\batch_runner.py --song songs\a12-karadi-w3 --only HKa --retry-failed --hosts api --dry-run` → exactly 1 row,
   HKa 8 s `720P 16:9 audio=off`, refs = 7 (`01-mintu-front`, `02-minnu-front`, `03-karadi-mama`, `06-amma-front`, `07-appa-face`,
   `08b-appa-body-backpack`, `11-set-path-low`), "estimated $0.80"; no `ERROR`/`MISSING`/`OVER BUDGET`/`Traceback`. Else → **blocked**.
4. Render:
   ```
   py comfy\batch_runner.py --song songs\a12-karadi-w3 --only HKa --retry-failed --hosts api --max-usd 0.90 --timeout-min 40 2>&1 | tee songs\a12-karadi-w3\batch_gateA3.log
   ```
   If it fails, report every line verbatim (including any `NOT resubmitted` or `submitted task <id>` line) and **block**. If a task id
   was printed but the download failed, run `py comfy\wan3_api.py fetch <id> songs\a12-karadi-w3\out\HKa-seed30313-w3.mp4 --timeout-min 15`
   once ($0) before blocking.
5. QC sheets for **HKa and O1** into `out\_qc\` (HKa = 240 frames, O1 = 210): `<ID>-contact.png` (5×2, 384 wide); `<ID>-every4-all.png`
   (every 4th frame, number burned in, 192 wide, 10 per row); 100 % stills of frames 0, 12, 24, 36, 48, 60, 72, 90, 120, 150, 180 and
   the last frame (`<ID>-fNNN.png`).
6. Slot cuts with the music into `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateA\` (create it). Hard cut, 1920×1080,
   30 fps, H.264 CRF 16, AAC 256k 48 kHz; video from the take at the slip, audio from the master WAV at the slot start, both the slot length:

   | file | take | slip (s) | WAV | start (s) | length (s) |
   |---|---|---|---|---|---|
   | `HKa-TA-slot03.mp4` | `out\HKa-seed30313-w3.mp4` | 0.400 | `karadi mama.wav` | 11.076 | 5.317 |
   | `HKa-EN-slot04.mp4` | `out\HKa-seed30313-w3.mp4` | 0.400 | `karadi mama Eng.wav` | 16.370 | 5.317 |
   | `O1-TA-slot27.mp4` | `out\O1-seed30313-w3.mp4` | 0.000 | `karadi mama.wav` | 139.088 | 5.294 |
   | `O1-EN-slot22.mp4` | `out\O1-seed30313-w3.mp4` | 0.000 | `karadi mama Eng.wav` | 112.129 | 5.318 |

   e.g. `ffmpeg -y -ss 0.400 -t 5.317 -i "songs\a12-karadi-w3\out\HKa-seed30313-w3.mp4" -ss 11.076 -t 5.317 -i "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\karadi mama.wav" -map 0:v -map 1:a -vf "scale=1920:1080:flags=lanczos,fps=30" -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -b:a 256k -ar 48000 -shortest "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateA\HKa-TA-slot03.mp4"`
   Then `_cuts\_gateA\gateA-slots.png`: one row per slot cut, 8 frames at 0.0, 0.67, 1.35, 2.02, 2.70, 3.37, 4.04, 4.72 s (the 8 beats),
   240 wide, the file name burned in at the left.
7. Commit with `[skip ci]` and push: `comfy/wan3_api.py`, `tests/test_wan3_retry_mock.py`, `songs/a12-karadi-w3/` except `out/`
   (incl. `batch_gateA.log`, `batch_gateA3.log`), `queue/2026-10-14-karadi-rev25-gateA3`, `queue/2026-10-13-karadi-rev24-picnic-archive`,
   `queue/A12-WATCH.md`, `queue/A12-WATCH-LOG.md`. **Do not judge the clips.**

**item-01.report.md:** step 1–3 output lines; run window UTC + Toronto; HKa task id, wall s, frames (ffprobe `-count_frames`), est,
any retry lines; failure lines verbatim; the sheet/still paths; the four slot-cut paths with frame counts (159–160 each) and the sheet
path; the runner's final estimate; the commit hash.
