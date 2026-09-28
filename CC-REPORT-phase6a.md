# CC-REPORT — Phase 6a Part C: Phantom at 1280×720 (run 2026-09-27)

**Result: 2 of 3 rows produced (T04, T08). T07 was not produced**: 720p full sampling takes ~39 min/row, so T07 could not
finish inside the 90-min hard stop (details below). Part A was already committed (`a3ea33b`) before this run; Part B was
not part of this execution.

## Pod
| | |
|---|---|
| id | `xc7bsejzkoyk3j` (template `cw3nka7d08`, 150 GB container disk) |
| GPU / cloud / rate | **A100-SXM4-80GB, community, $1.39/h** (H100 community: no instances) |
| rented | 23:06 UTC → stopped 00:33:12 UTC by the runner's `--max-minutes 70` stop-cmd (out-push ran first) |
| removed | after confirming `EXITED`; `pod get` now 404 |
| **cost** | **~87 min ≈ $2.01** = Part C and the total for this dispatch (A, B $0) |

## Step 1 (laptop)
- `build_song_refs.py --song twinkle-twinkle --no-cut` built `songs\twinkle-twinkle\refs\minmini-sideA-16x9.png`. It also
  re-wrote `minnu-body-16x9.png` / `mintu-front-16x9.png`; those were pixel-identical to HEAD, so they were restored with `git checkout`.
- `_ab5` dry-run: 3 rows, T08/T07 "2 SEPARATE references", **no REF MISSING**. `wan-push` done.

## Step 2 (pull)
- R2 manifest: 5 files. Phantom `29052237696` B **verified from R2, no `model-get`**.
- **BOOT-TO-READY: models 617 s, total 632 s.** `WanPhantomSubjectToVideo` OK and `ImageBatch` OK;
  `WanVaceToVideoMultiRef` MISSING, because the template's ComfyUI was already running.
- Custom-node restart (`pkill` + `pull`): models 6 s, total 27 s, **all three nodes OK**. It also moved ComfyUI's log to
  `/workspace/comfyui.log`; the template's own instance logged elsewhere.
- New gotcha: **pod env vars (the R2 keys) are not visible in SSH sessions or `/etc/rp_environment`**, only in
  `/proc/1/environ`. The first `pull` died with "missing env" (~1 min). The workaround was to export them from there
  (helper `/workspace/r2env.sh`), without printing any values. Suggest `pod_bootstrap.sh` does this itself.
- Pod rclone is v1.58.1. It prints `s3 provider "Cloudflare" not known` notices, which are harmless.

## Step 3 (batch, seed 30313)
| row | mode | status | wall s | s/step |
|---|---|---|---|---|
| T04_ph720 | distilled 6 | done | **240.1** | (includes the first model load) |
| T08_ph720 | full 30 | done | **2321.1** | ~77 |
| T07_ph720 | full 30 | **not produced**: interrupted at ~step 22/30 by the 70-min cap | (~1680 spent) | ~77 |

- Runner total: 42.7 GPU-min for the done shots. **Peak VRAM 53,851 MiB of 80 GB: no OOM** (`nvidia-smi` every 10 s, `vram.log`).
- `grep -c "lora key not loaded" comfyui.log` → **0**. No error or traceback in `comfyui.log`.

### Why T07 is missing (and ~$0.65 wasted)
- 720p full sampling ran at ~77 s/step (480p in `_ab4` was ~23 s/step, 700 s/row). T08's ~39 min meant T07 would end
  around minute 94 of pod time, past the 90-min hard stop. Arul chose **"stop after T08"**.
- A pod-side watcher caught T08's `done` and sent SIGINT to the runner. **The SIGINT was ignored.** The runner had been
  started as a background (`nohup … &`) job from a non-interactive shell, which inherits SIGINT as SIG_IGN, so no
  KeyboardInterrupt was raised. The runner went on to start T07, which sampled ~28 min (≈ $0.65) until the 70-min cap
  interrupted it. This was my (CC's) error.
- **Fix for next time:** give `batch_runner.py` a stop-file or SIGTERM handler that stops before the next row. Never rely on SIGINT to a
  backgrounded runner.

## Output (pulled from R2 to the laptop)
- `C:\Projects\opencode\video_image\songs\_ab5-2026-09-23-phantom720\out\T04_ph720-seed30313-s6.mp4`
- `C:\Projects\opencode\video_image\songs\_ab5-2026-09-23-phantom720\out\T04_ph720-seed30313-s6.json`
- `C:\Projects\opencode\video_image\songs\_ab5-2026-09-23-phantom720\out\_qc\T04_ph720-strip.png`
- `C:\Projects\opencode\video_image\songs\_ab5-2026-09-23-phantom720\out\T08_ph720-seed30313-s30.mp4`
- `C:\Projects\opencode\video_image\songs\_ab5-2026-09-23-phantom720\out\T08_ph720-seed30313-s30.json`
- `C:\Projects\opencode\video_image\songs\_ab5-2026-09-23-phantom720\out\_qc\T08_ph720-strip.png`
- `C:\Projects\opencode\video_image\songs\_ab5-2026-09-23-phantom720\out\_debug\batch_ab5.log`, `comfyui.log`, `vram.log`

## Numbers for Fable's budget
- A100 community at 720p: distilled row ≈ 4 min ≈ $0.09; **full row ≈ 39 min ≈ $0.90**, 3.3× the 480p full row (~$0.27).
  Fable's per-song ~$10–18 at 720p should be re-checked against ~$0.90 per full row plus ~15 min of pod boot/overhead.
- A 720p full row doesn't fit the old "~25 min" planning figure. A two-full-row A/B at 720p needs a ≥ 100-min cap.

## Not judged
Clips were not frame-checked by CC. Fable checks **T04** (face on-model at 720p) and **T08** (TV head, antennae, wings,
lantern held; no orange body). **T07 (two children at 720p) is still untested.**
