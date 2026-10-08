# CC DISPATCH — 2026-10-07 "Beast 4K": install Real-ESRGAN inside the repo + 4K upscale of A07 Butterfly (on Beast)

**Machine:** Beast (Arul's new desktop). Run everything **on Beast**, not the laptop.
**Repo:** `C:\Projects\opencode\video_image` · **Song folder:** `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly`
**Executor:** CC (Sonnet is fine) · **Manager:** Fable (reviews the report and the 4K cuts after).
**Cost:** $0 — local GPU only. No API, no RunPod.

## Why
The projects moved from the laptop to Beast, but the upscaler (`realesrgan-ncnn-vulkan`) lived in `C:\tools`, outside the
repo, so it didn't come along and `song_4k.ps1` stopped with "realesrgan-ncnn-vulkan not found". New rule: the tool lives
**inside the repo** at `tools\realesrgan-ncnn-vulkan\`, git-ignored (never committed), and the script looks there first.
Then: upscale the 33 Butterfly takes to 4K and build 4K versions of the ROUGH3 cuts (same cut points, frame for frame),
which Arul will swap into his CapCut edit with "Replace" and export in 4K.

## Hard limits
- **No API spend.** No RunPod, no pod, no cloud. Local GPU only.
- Never print, echo or log `.env` values, API keys, the workspace id or any video URL.
- Never commit `tools/`, `out/`, `out_4k/`, `.env`, `logs.txt`, `nil`, or any video. Commits carry `[skip ci]`.
- Never delete or overwrite anything in `songs\a07-butterfly\out\` or the song folder outside `_cuts\`.
  Do not touch the ROUGH, ROUGH2, ROUGH3 cuts.
- If a path in this file doesn't exist on Beast (repo or song folder), **stop → blocked** and report the actual paths. Don't guess.

## Protocol
Create `queue\2026-10-07-beast-4k\` in the repo, copy this file into it as `QUEUE.md`, and keep `LOG.md` there
(start/done lines per step, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop) — same as earlier queues.
When finished: `QUEUE END <time>`, and tell Arul "Beast 4K done — ask Fable to review queue\2026-10-07-beast-4k".

---

## item-01 — prerequisites + install the upscaler inside the repo (≈ 5 min)

1. **Check Beast has what the pipeline needs** (report versions/paths; anything missing → blocked):
   - `py --version` (Python 3.8+), `ffmpeg -version` and `ffprobe -version` on PATH.
   - `C:\Projects\opencode\video_image\songs\a07-butterfly\cutplan.json` exists; every `take` it names exists in
     `songs\a07-butterfly\out\` (33 distinct files, 10 of them `-splice.mp4`).
   - Song folder has both master WAVs: `butterfly (1).wav` and `butterfly english (1).wav`.
   - GPU: report the graphics card name (`Get-CimInstance Win32_VideoController | Select Name,DriverVersion`).
   - Free space on C: (need **≥ 30 GB**: ~15–20 GB temp frames + ~5 GB output). Less → blocked.
2. **Download** the official release zip (GitHub, xinntao/Real-ESRGAN v0.2.5.0):
   `https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip`
   Extract so that these exist (flatten any inner folder):
   - `C:\Projects\opencode\video_image\tools\realesrgan-ncnn-vulkan\realesrgan-ncnn-vulkan.exe`
   - `C:\Projects\opencode\video_image\tools\realesrgan-ncnn-vulkan\models\realesr-animevideov3-x3.param` / `.bin`
     (and the other model files from the zip). Report the sha256 of the zip and of the exe.
3. **`.gitignore`**: add a line `tools/` (with a comment: `# local binaries (Real-ESRGAN etc.) — installed per machine, never committed`).
   Confirm `git status` does not list anything under `tools/`.
**item-01.report.md:** versions, GPU, free space, take count, zip/exe sha256, `.gitignore` diff.

## item-02 — make the scripts find the in-repo tool (≈ 5 min)

1. `scripts\upscale_song.py`: where it adds `C:\tools\realesrgan-ncnn-vulkan` to PATH, change it to check, in order:
   1. `<repo>\tools\realesrgan-ncnn-vulkan` (repo = parent of `scripts\`, i.e. `HERE.parent / "tools" / "realesrgan-ncnn-vulkan"`)
   2. `C:\tools\realesrgan-ncnn-vulkan` (old location, kept as fallback)
   and prepend the **first one that exists** to PATH. Update the "not found" message to name both locations, and the
   module docstring line that says `C:\tools\realesrgan-ncnn-vulkan is put on PATH when it exists`.
2. `scripts\song_4k.ps1`: update the comment `Needs C:\tools\realesrgan-ncnn-vulkan` →
   `Needs tools\realesrgan-ncnn-vulkan in the repo (git-ignored; see queue\2026-10-07-beast-4k) or C:\tools\...`.
3. Check: `py scripts\upscale_song.py songs\a07-butterfly --dry` → lists 33 takes and the total frame count (≈ 5,217),
   no "not found". Paste the summary lines.
**item-02.report.md:** the diff of both files; the `--dry` output summary.

## item-03 — speed test on one clip (≈ 2–5 min)

1. `py scripts\upscale_song.py songs\a07-butterfly --only V1a` (150 frames).
2. Report: wall time, seconds per frame, output `songs\a07-butterfly\out_4k\V1a-seed30313-w3.mp4` is 3840×2160 @ 30 fps
   with 150 frames (ffprobe `-count_frames`), and the backend line from the log (must say `ncnn` / vulkan, not torch-CPU).
3. Estimate the full run: (5,217 − 150) × s/frame. If the estimate is **over 12 h**, stop → blocked and report (Fable
   will decide); otherwise continue.
**item-03.report.md:** the numbers above + the estimate.

## item-04 — full 4K run + 4K cuts (long; runs on its own)

1. Start it in its **own PowerShell window** so it survives this CC session (it is resumable — finished clips are
   skipped if it's run again):
   ```
   Start-Process powershell -ArgumentList '-NoExit','-ExecutionPolicy','Bypass','-Command','cd C:\Projects\opencode\video_image; powershell -ExecutionPolicy Bypass -File scripts\song_4k.ps1 -Song songs\a07-butterfly -Tag ROUGH3-4K'
   ```
   It upscales the remaining takes into `songs\a07-butterfly\out_4k\`, then builds
   `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\_cuts\A07-BUTTERFLY-ROUGH3-4K-TA.mp4` and `-ROUGH3-4K-EN.mp4`.
   Log: `songs\a07-butterfly\upscale_4k.log`.
2. Write `item-04.report.md` right after starting it (time started, expected finish from item-03), mark `item-04.started`,
   commit (item-05 step 1) and tell Arul it is running. **Do not wait hours in this session.**

## item-05 — commit now; verify later

1. **Commit now** with `[skip ci]` and push: `.gitignore`, `scripts/upscale_song.py`, `scripts/song_4k.ps1`,
   `queue/2026-10-07-beast-4k/`. Nothing under `tools/`, `out/`, `out_4k/`.
2. **When Arul says the run finished** (a later CC session), verify and append to `item-04.report.md`:
   - `out_4k\` has 33 files (+ `.json` sidecars), all 3840×2160 @ 30 fps.
   - `ROUGH3-4K-TA.mp4` = **6481** video frames (216.04 s), `ROUGH3-4K-EN.mp4` = **6665** frames (222.16 s), 3840×2160,
     30 fps, one AAC stream each (ffprobe `-count_frames`). The cut log has no "holds last frame" lines over 1 frame.
   - Two 100% stills from each 4K cut at 0:30 and 2:00 → `songs\a07-butterfly\out_4k\_qc\` for Fable.
   Then write `item-05.done`, `QUEUE END`, and tell Arul "Beast 4K done — ask Fable to review queue\2026-10-07-beast-4k".

## For Arul (after it's done)
In CapCut: right-click the ROUGH3 clip on the timeline → **Replace** → pick the matching `ROUGH3-4K` file (same length,
same frames, so your splits and slides stay) → export at 4K. Numbered clips you used directly have 4K versions in
`C:\Projects\opencode\video_image\songs\a07-butterfly\out_4k\` (same names as the takes).
