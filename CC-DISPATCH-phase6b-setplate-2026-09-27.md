# CC-DISPATCH — Phase 6b: laptop upscaling on Vulkan, runner/bootstrap fixes, set-plate test (2026-09-27)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine). Parts A, B0, B, C, in order.
**Budget: Parts A, B0 and B $0. Part C ≤ 35 min pod time (~$0.80 A100 community), `--max-minutes 30`, hard stop 45 min.**
Standing rules: one pod, stopped and removed before reporting; no retakes, no extra seeds; never print `.env` values;
edit `shots.csv` cells, never restore it; report **full Windows paths** of everything produced.

## 0 · Why (Fable, from CC-REPORT-phase6a + frame check)
- Phantom at 720p held identity (T04 Minnu fully on-model; T08 Minmini TV head/antennae/wings/lantern held, no orange body)
  but **invents a different house in every shot** — a song cannot cut together. Test: the Twinkle terrace set plate as one
  more Phantom reference (Part C).
- **This laptop has no NVIDIA GPU.** The phase 5a `device: cuda` run was on a pod; the Patti intro 4K ran on CPU for 4.8 h.
  Fable added a Vulkan backend (Real-ESRGAN ncnn — runs on Intel Iris Xe) and made RIFE handle any fps ratio (Part A).
- 6a lost ~$0.65 because SIGINT to a backgrounded runner was ignored → runner now has a STOP file + SIGTERM; and the pod's
  R2 keys were only in `/proc/1/environ` → `pod_bootstrap.sh` now imports them itself.

## 1 · What changed on disk (Fable; all tested; nothing committed)
| file | change | tested |
|---|---|---|
| `scripts/upscale_video.py` | `--backend auto\|torch\|ncnn` (auto = torch on CUDA, else `realesrgan-ncnn-vulkan` if on PATH, else torch CPU); ncnn path = one folder pass x4 + one ffmpeg lanczos pass to target; RIFE now any ratio via `-n <target frames>` with rife-v4.6 (16→30 fps = real RIFE, 81→152 frames); sidecar records `backend`; `--ncnn-gpu` | stand-in binaries with the real CLI: ncnn + RIFE 17→32 frames at 30 fps OK; `auto` picks ncnn without CUDA; torch path regression OK |
| `scripts/upscale.ps1` | no CUDA-Python hunt; puts `C:\tools\realesrgan-ncnn-vulkan` and `C:\tools\rife-ncnn-vulkan` on PATH for the run, calls `py`, `-Backend` passthrough | syntax by inspection (no PowerShell here) |
| `comfy/batch_runner.py` | graceful stop: file `songs/<slug>/STOP` (or `--stop-file`) or SIGTERM → the row in flight finishes, no new row starts, stop-cmd still runs; SIGINT forced back to KeyboardInterrupt even when backgrounded; a stale STOP is removed at start | mock ComfyUI, 3 rows, STOP dropped during row 1 → 1 done, 2 never started, stop-cmd ran |
| `scripts/pod_bootstrap.sh` | `need_env` imports missing `S3_*`, `AWS_*`, `RUNPOD_POD_ID`, `RUNPOD_API_KEY` from `/proc/1/environ` (silent) | fake environ: fills only missing vars, keeps values containing `=`, never prints |
| `songs/_ab6-2026-09-27-setplate/` | **new** A/B folder: 4 rows, `set/terrace-set-16x9.png` (built by Fable, see README), `world-set.txt`, `world-noset.txt` | dry-run: 4 rows, 2–3 SEPARATE refs, max ~503 tokens, no REF MISSING |

## Part A — Vulkan tools on the laptop + speed test ($0)
1. Download and unzip (use the Windows zip assets; report the exact asset names):
   - Real-ESRGAN ncnn: `https://github.com/xinntao/Real-ESRGAN/releases` → tag **v0.2.5.0** → `realesrgan-ncnn-vulkan-*-windows.zip`
     → `C:\tools\realesrgan-ncnn-vulkan\` (the folder must contain `realesrgan-ncnn-vulkan.exe` and `models\realesr-animevideov3-x4.bin/.param`).
   - RIFE: `https://github.com/nihui/rife-ncnn-vulkan/releases` → latest `rife-ncnn-vulkan-*-windows.zip` →
     `C:\tools\rife-ncnn-vulkan\` (must contain `rife-ncnn-vulkan.exe` and a `rife-v4.6\` model folder).
   If either is already present from 6a, reuse it and say so. Do not add them to the permanent PATH — `upscale.ps1` does it per run.
2. Smoke each tool on one frame and capture the GPU line it prints at start (e.g. `[0 Intel(R) Iris(R) Xe Graphics] ...`):
   ```
   ffmpeg -y -i songs\twinkle-twinkle\out\T16-seed30313-s6.mp4 -frames:v 1 C:\tmp\f1.png
   C:\tools\realesrgan-ncnn-vulkan\realesrgan-ncnn-vulkan.exe -i C:\tmp\f1.png -o C:\tmp\f1x4.png -n realesr-animevideov3 -s 4
   ```
   If it reports no Vulkan device or crashes: stop Part A here, report the output verbatim, continue with Part B.
3. Speed + quality test, the real command Arul will use:
   ```
   powershell -ExecutionPolicy Bypass -File scripts\upscale.ps1 songs\twinkle-twinkle\out\T16-seed30313-s6.mp4 -Dst outputs\upscale-test-2026-09-23\T16-4k-30-vulkan.mp4 -Fps 30
   ffmpeg -y -i outputs\upscale-test-2026-09-23\T16-4k-30-vulkan.mp4 -vf "select='between(n,60,63)',crop=1200:900:1300:500,tile=4x1" -vsync 0 -frames:v 1 outputs\upscale-test-2026-09-23\_qc\T16-4k-30-vulkan-crop60-63.png
   ```
   Report from the sidecar: `backend` (must be `ncnn`), `interpolation` (must name rife-v4.6), `seconds`, output frames/fps,
   and **s/frame for the upscale** (upscale seconds ÷ 81). Fable compares the PNG with `_qc\T16-4k-30-crop60-63.png`
   (minterpolate: star edge smeared on frame 61).

## Part B0 — last week's uncommitted work: check, clean, commit ($0) — do this BEFORE Part B
Fable inspected the working tree on 2026-09-27 (`git status`, `git diff`, secret grep). What is there and what to do:

| path | what it is | action |
|---|---|---|
| `DEPLOY.md` | **line endings only** (LF→CRLF, no text change) | **revert** — it is the CI redeploy marker (`deploy.yml` paths): committing it would rebuild and redeploy the serverless endpoint |
| `songs/_ab-2026-09-22/shots.csv`, `songs/_ab4-2026-09-23/shots.csv`, `songs/_selftest/shots.csv`, `songs/twinkle-twinkle/_untrimmed-2026-09-22/shots.csv` | **line endings only**, cell content identical | revert (this is the one allowed exception to "never restore shots.csv from git": the check below proves no cell changed) |
| `SESSION-HANDOFF-2026-09-21-WAN-SERVERLESS-REVIEW.md` | real content: §11 "first video" record + phase 3 plan (2026-09-21); secret *names* only, no values | commit |
| `CC-DISPATCH-phase4g/4h/4i-*.md` | dispatch records from 09-22 (their song folders were committed in `fe1c461`, the files were not) | commit |
| `STATUS.md` | stale 09-17 resume marker (pre-ComfyUI serverless debugging) — misleading at the repo root | move to `docs/history/STATUS-2026-09-17.md`, commit |
| `outputs/**` (28 untracked: json sidecars, cutouts, ladder, upscale tests, VACE refs/_qc, ~200 MB) | **json sidecars contain presigned R2 URLs** (grep hit `Signature=`); the rest is large binaries | never commit — add `/outputs/` to `.gitignore` (the 5 already-tracked `outputs/vace/pod/_qc/*.png` stay tracked) |
| `logs.txt`, `nil` | junk | add to `.gitignore`, never commit |

```
git diff --ignore-cr-at-eol --quiet -- DEPLOY.md songs/_ab-2026-09-22/shots.csv songs/_ab4-2026-09-23/shots.csv songs/_selftest/shots.csv songs/twinkle-twinkle/_untrimmed-2026-09-22/shots.csv
    -> exit code MUST be 0 (only line endings differ). If it is 1: STOP B0, paste `git diff --ignore-cr-at-eol` of those files, restore nothing.
git checkout -- DEPLOY.md songs/_ab-2026-09-22/shots.csv songs/_ab4-2026-09-23/shots.csv songs/_selftest/shots.csv songs/twinkle-twinkle/_untrimmed-2026-09-22/shots.csv
mkdir docs\history
move STATUS.md docs\history\STATUS-2026-09-17.md
(append to .gitignore, one per line:)  /outputs/   logs.txt   nil
git ls-files outputs                      -> still the same 5 files
git status --short                        -> must list ONLY: .gitignore, SESSION-HANDOFF..., the 3 phase4g/h/i dispatches, docs/history/,
                                             and the phase 6b files (batch_runner, pod_bootstrap, upscale_video, upscale.ps1, _ab6, CC-REPORT-phase6a, this dispatch)
git add .gitignore SESSION-HANDOFF-2026-09-21-WAN-SERVERLESS-REVIEW.md CC-DISPATCH-phase4g-ab-2026-09-22.md CC-DISPATCH-phase4h-full-ab-2026-09-22.md CC-DISPATCH-phase4i-s03-2026-09-22.md docs/history/STATUS-2026-09-17.md
git commit -m "housekeeping: 09-21 handoff (first video, phase 3 plan), 4g-4i dispatch records, 09-17 STATUS to docs/history; ignore outputs/ (sidecars hold presigned URLs), logs.txt, nil [skip ci]"
```
Do not push yet — Part B pushes both commits together.

**CI check (read-only).** `.github/workflows/deploy.yml` triggers on `scripts/**`, so pushes that touched `scripts/`
(`33f5820`, `a3ea33b`) may have rebuilt and redeployed the serverless endpoint. Run
`gh run list --workflow deploy.yml -L 8` and report which commits started a run and their result. If any ran a deploy,
check (read-only, no scaling change) that endpoint `wv9oneserd7vj6` is still at min 0 / max 0 workers and report it; if it
is not 0/0, report and ask — do not change it yourself. Parts B0 and B carry `[skip ci]` so this push builds nothing.

## Part B — commit ($0)
```
python comfy\batch_runner.py --song songs\_ab6-2026-09-27-setplate --hosts http://x --dry-run      (4 rows, no REF MISSING, no OVER BUDGET)
python -m py_compile comfy\batch_runner.py scripts\upscale_video.py
git status   -- after B0 the only changes left are the phase 6b files; confirm NO .env, logs.txt, nil, songs/*/out/, outputs/ in the add set
git add comfy/batch_runner.py scripts/upscale_video.py scripts/upscale.ps1 scripts/pod_bootstrap.sh scripts/build_song_refs.py ^
        songs/_ab6-2026-09-27-setplate CC-REPORT-phase6a.md CC-DISPATCH-phase6b-setplate-2026-09-27.md
git commit -m "phase 6b: Vulkan upscaling for GPU-less machines, RIFE at any fps ratio, runner STOP file, env import; set-plate A/B

upscale_video: --backend auto|torch|ncnn (realesrgan-ncnn-vulkan runs on Intel/AMD GPUs; the laptop has
no CUDA and torch-CPU took 4.8 h for a 20 s 720p clip); RIFE rife-v4.6 with an explicit target frame count
so 16->30 fps is real RIFE; sidecar records the backend. upscale.ps1: C:\tools ncnn builds on PATH per run.
batch_runner: songs/<slug>/STOP or SIGTERM = finish the row in flight, start no new row (6a lost ~\$0.65 to
an ignored SIGINT); SIGINT restored for backgrounded runs. pod_bootstrap: imports R2/RunPod vars from
/proc/1/environ when SSH sessions do not see them. songs/_ab6-2026-09-27-setplate: terrace set plate as a
Phantom reference. CC-REPORT-phase6a: Phantom at 720p (T04, T08). [skip ci]"
git push     (pushes B0 + B; both carry [skip ci] -> no build. Confirm with `gh run list --workflow deploy.yml -L 2` that no new run started.)
```

## Part C — set-plate test on a pod (`songs/_ab6-2026-09-27-setplate/`, 832×480)
1. `bash scripts/pod_bootstrap.sh wan-push` from the laptop. Fresh pod (A100 80 GB community → secure fallback; H100 if
   available), R2 env vars in the console, copy `scripts/pod_bootstrap.sh`, `bash pod_bootstrap.sh pull`. The env import is
   now automatic — **do not** create `r2env.sh`; if `pull` still says "missing env", report it. Restart ComfyUI once so all
   three nodes say OK (`pkill -f "main.py --listen"`; `pull` again).
2. Run in the **foreground of the SSH session** (not `nohup &`), logs preserved, **literal pod id** in the stop-cmd:
   ```
   cd /workspace/wan
   python3 comfy/batch_runner.py --song songs/_ab6-2026-09-27-setplate --hosts http://127.0.0.1:8188 --seed 30313 --dry-run
   python3 comfy/batch_runner.py --song songs/_ab6-2026-09-27-setplate --hosts http://127.0.0.1:8188 --seed 30313 \
       --max-minutes 30 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/_ab6-2026-09-27-setplate; runpodctl stop pod <POD_ID>" 2>&1 | tee /workspace/batch_ab6.log
   ```
   Order is the CSV order (cheap first): T04_noset, T04_set, T08_set (distilled, ~2 min each after the first model load),
   then T07_set (full, ~12 min). To stop early at any point: `touch /workspace/wan/songs/_ab6-2026-09-27-setplate/STOP`
   from a second SSH session — the row in flight finishes, nothing new starts, the stop-cmd runs. If the first row fails,
   STOP immediately and report.
3. Confirm stopped → remove the pod. Pull `out/` (+ `_debug/`) to the laptop. On the laptop make the comparison grid
   (frame 40 of each clip, 2×2):
   ```
   cd songs\_ab6-2026-09-27-setplate\out
   ffmpeg -y -i T04_noset-seed30313-s6.mp4 -i T04_set-seed30313-s6.mp4 -i T08_set-seed30313-s6.mp4 -i T07_set-seed30313-s30.mp4 ^
     -filter_complex "[0]select=eq(n\,40)[a];[1]select=eq(n\,40)[b];[2]select=eq(n\,40)[c];[3]select=eq(n\,40)[d];[a][b][c][d]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0" ^
     -frames:v 1 _qc\ab6-grid-f40.png
   ```
4. `CC-REPORT-phase6b.md` in the repo root: Part A (asset names, GPU line, sidecar values, s/frame, PNG path); Part B0 (EOL check
   exit code, commit hash, the `gh run list` table + endpoint worker counts if checked); Part B (commit
   hash); Part C (pod id/GPU/rate, `pull` lines incl. whether env import worked, per-row wall s, full paths of the 4 mp4 +
   strips + json + the grid PNG, $ for the part). **Do not judge the clips** — Fable checks: same house in T04_set / T08_set /
   T07_set and matching the plate; night kept; no floating diorama; T07_set two distinct children.

## What Fable decides from this
- **Set plate holds** → production recipe: Phantom, character refs + one set plate per location, full rows at 480p,
  4K + 30 fps on the laptop (if Part A's s/frame is workable) or on the pod. Next: Arul's beats for the next song.
- **Plate pasted as an object / daylight kept** → next A/B: plate as a keyframe-style first frame is not available on
  Phantom, so try the plate with the characters composited onto it (one image) as the reference.
- **Vulkan too slow on the laptop** (> ~6 s/frame at 480p→4K) → the 4K pass moves onto the pod right after generation
  (torch backend on CUDA, ~0.3 s/frame), priced into the per-song estimate.
