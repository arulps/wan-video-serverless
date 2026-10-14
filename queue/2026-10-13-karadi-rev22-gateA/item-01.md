# item-01 — prerequisite, checks, render HKa + O1, QC sheets, slot cuts with the music, commit (≤ $1.60 list)

0. **Prerequisite.** `queue\2026-10-13-karadi-rev21-refs\item-01.done` must exist (rev 2.1 with the set plates and Appa's daypack is
   built and committed). If it is missing → **blocked** ("run queue\2026-10-13-karadi-rev21-refs first"), $0.00 spent.
1. **Rev 2.1+ is in place** (verify, don't edit):
   - `songs\a12-karadi-w3\shots\05_HKa.raw.txt` contains "the children do their own quick full turn beside him" and
     "Image 7 is the lower forest path set";
   - `songs\a12-karadi-w3\shots\19_O1.raw.txt` contains "Karadi Mama's home set" and "a tall olive-green hiking daypack";
   - `shots.csv`: HKa and O1 are `todo`; V1A, V2A, V3A, V4A are `done`;
   - `refs\send\` has `11-set-path-low.jpg`, `13-set-home.jpg`, `08b-appa-body-backpack.jpg`;
   - `out\` has **no** `HKa-seed30313-w3.mp4` or `O1-seed30313-w3.mp4` at the top level (the rev 1.x takes were moved to
     `out\_rev1x-2026-10-13\` by the refs queue). If either is still there, move it into that folder first (rename, never delete) and say so.

   Any other mismatch → **blocked**.
2. `py tests\test_wan3_mock.py` → PASS. Credentials check (as in the Shorts queues) → True (print only True/False).
3. `py tests\test_prompt_lint.py` → PASS; `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`.
   Any failure → **blocked**.
4. Dry-run: `py comfy\batch_runner.py --song songs\a12-karadi-w3 --only HKa,O1 --hosts api --dry-run` must show:
   - 2 rows, `720P 16:9 audio=off`; HKa 8 s, refs = 7 (`01-mintu-front`, `02-minnu-front`, `03-karadi-mama`, `06-amma-front`,
     `07-appa-face`, `08b-appa-body-backpack`, `11-set-path-low`); O1 7 s, refs = 9 (the same plus `04-rabbit`, `05-squirrel`, and
     `13-set-home` instead of the path);
   - "estimated $1.50";
   - no `ERROR`, `unknown cast`, `MISSING`, `OVER BUDGET`, `refused` or `Traceback`.

   Otherwise → **blocked**.
5. Render:
   ```
   py comfy\batch_runner.py --song songs\a12-karadi-w3 --only HKa,O1 --hosts api --max-usd 1.60 --timeout-min 40 2>&1 | tee songs\a12-karadi-w3\batch_gateA.log
   ```
6. QC sheets for each rendered clip into `songs\a12-karadi-w3\out\_qc\` (same tools as the earlier gates; HKa = 240 frames, O1 = 210):
   - `<ID>-contact.png` — 5×2, 10 frames evenly spaced, 384 wide;
   - `<ID>-every4-all.png` — every 4th frame through the whole clip, frame number burned in, 192 wide, 10 per row (the turn and the
     children's copy need the whole clip);
   - 100 % stills (1280×720) of frames 0, 12, 24, 36, 48, 60, 72, 90, 120, 150, 180 and the last frame (`<ID>-fNNN.png`) — the
     12–72 run is the turn (planned at 1.1–2.4 s = frames 33–72).
7. **Slot cuts with the music** (learnings 0d: a gate is reviewed in its real slot), into
   `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateA\` (create it). Hard cuts, 1920×1080, 30 fps, H.264 CRF 16,
   AAC; video from the take at the slot's slip, audio from the master WAV at the slot's start, both the slot's length:

   | file | take | slip (s) | WAV | start (s) | length (s) |
   |---|---|---|---|---|---|
   | `HKa-TA-slot03.mp4` | `out\HKa-seed30313-w3.mp4` | 0.400 | `karadi mama.wav` | 11.076 | 5.317 |
   | `HKa-EN-slot04.mp4` | `out\HKa-seed30313-w3.mp4` | 0.400 | `karadi mama Eng.wav` | 16.370 | 5.317 |
   | `O1-TA-slot27.mp4` | `out\O1-seed30313-w3.mp4` | 0.000 | `karadi mama.wav` | 139.088 | 5.294 |
   | `O1-EN-slot22.mp4` | `out\O1-seed30313-w3.mp4` | 0.000 | `karadi mama Eng.wav` | 112.129 | 5.318 |

   e.g. `ffmpeg -y -ss 0.400 -t 5.317 -i "songs\a12-karadi-w3\out\HKa-seed30313-w3.mp4" -ss 11.076 -t 5.317 -i "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\karadi mama.wav" -map 0:v -map 1:a -vf "scale=1920:1080:flags=lanczos,fps=30" -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -b:a 256k -ar 48000 -shortest "...\_cuts\_gateA\HKa-TA-slot03.mp4"`
   (the WAVs are in the song folder; the TA master is `karadi mama.wav`, the EN master `karadi mama Eng.wav`).
   Then one **per-slot sheet** `_cuts\_gateA\gateA-slots.png`: one row per slot cut, 8 frames per row at 0.0, 0.67, 1.35, 2.02, 2.70,
   3.37, 4.04, 4.72 s of the cut (= the 8 beats), 240 wide, the file name burned in at the left.
8. Commit with `[skip ci]` and push: `songs/a12-karadi-w3/` except `out/` (`shots.csv` carries the runner's status updates),
   `queue/2026-10-13-karadi-rev22-gateA`, `queue/A12-WATCH.md`, `queue/A12-WATCH-LOG.md`. `git add` by explicit path only.
   **Do not judge the clips.**

**item-01.report.md** must cover: the prerequisite and rev 2.1 checks; checks 2–3 output lines; dry-run rows + total; run window UTC +
Toronto; per clip: task id, wall s, length, frames (ffprobe `-count_frames`), refs, est; failure lines verbatim (e.g.
`IPInfringementSuspect`); the QC sheet/still paths; the four slot-cut paths with their frame counts (expect 160, 160, 159, 160) and the
per-slot sheet path; the runner's final estimate; the commit hash.
