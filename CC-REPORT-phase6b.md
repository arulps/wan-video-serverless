# CC-REPORT — Phase 6b (2026-09-27)

**Summary: A done · B0 done (`ba99f79`) · B done · C done, 4/4 rows, $0.67. Endpoint `wv9oneserd7vj6` is at 0/3 workers, not 0/0: question for Arul.**

## Part A — Vulkan tools on the laptop ($0)
- **Real-ESRGAN:** `xinntao/Real-ESRGAN` v0.2.5.0, asset **`realesrgan-ncnn-vulkan-20220424-windows.zip`**, newly installed to
  `C:\tools\realesrgan-ncnn-vulkan\` (has `realesrgan-ncnn-vulkan.exe` and `models\realesr-animevideov3-x4.bin/.param`).
- **RIFE:** `C:\tools\rife-ncnn-vulkan\` was **already present and reused** (`rife-ncnn-vulkan.exe` + `rife-v4.6\`). It is the
  latest release, `rife-ncnn-vulkan-20221029-windows.zip`. Neither tool is on the permanent PATH.
- **GPU line (both tools):** `[0 Intel(R) Iris(R) Xe Graphics]  queueC=0[1]  queueG=0[1]  queueT=0[1]`, with fp16 supported.
  Both one-frame smoke tests exited 0.
- **`upscale.ps1` T16 → 4K/30:** sidecar `backend: ncnn`, `device: vulkan`,
  `interpolation: "rife-ncnn-vulkan rife-v4.6 81->152 frames"`, output 3744×2160 @ 30 fps, 152 frames, 5.07 s, 8.9 MB.
  `seconds`: decode 2.4, **upscale 1182.9**, encode 93.1.
- **s/frame:** the sidecar's `upscale` stage includes RIFE.
  - As the dispatch defines it: 1182.9 ÷ 81 = **14.6 s/frame**.
  - Real-ESRGAN alone (console log): 317.7 s ÷ 81 = **3.92 s/frame**.
  - RIFE at 4K takes the other ~865 s.
  - Against Fable's "> ~6 s/frame = too slow" rule, the two readings land on opposite sides of the line. Fable's call.
- Paths:
  - `C:\Projects\opencode\video_image\outputs\upscale-test-2026-09-23\T16-4k-30-vulkan.mp4`
  - `C:\Projects\opencode\video_image\outputs\upscale-test-2026-09-23\T16-4k-30-vulkan.mp4.json`
  - `C:\Projects\opencode\video_image\outputs\upscale-test-2026-09-23\_qc\T16-4k-30-vulkan-crop60-63.png` (compare with `_qc\T16-4k-30-crop60-63.png`)

## Part B0 — housekeeping: done after Arul approved it (the first attempt was blocked by auto-mode)
- EOL check `git diff --ignore-cr-at-eol --quiet -- DEPLOY.md <4 shots.csv>` → **exit 0** (only line endings differed).
  The 5 files were reverted.
- The stale `.git\index.lock` (0 bytes, no git process) was removed. `STATUS.md` → `docs/history/STATUS-2026-09-17.md`.
- `.gitignore`: `/outputs/`, `logs.txt` and `nil` were added. The old last line `*.mp4` had no trailing newline, so the first
  append produced `*.mp4/outputs/`. That was fixed to two separate lines before the commit.
  `git ls-files outputs` still lists the same 5 files.
- **Commit `ba99f79`** `[skip ci]`. The staged diff was grepped for `Signature=` and key values: none.
- **CI (`gh run list --workflow deploy.yml -L 8`), all `build-deploy` on main, all success:**

| run | commit (title) | when (UTC) |
|---|---|---|
| 35930950372 | `a3ea33b` multi-reference: Phantom… | 09-23 22:55 |
| 35821511686 | `33f5820` scripts: upscale_video.py… | 09-23 05:13 |
| 35799812547 | phase4h infra… | 09-22 23:57 |
| 35775628367 | songs: Twinkle + Row re-cut… | 09-22 19:43 |
| 35678450130 | phase4: VACE worker path… | 09-22 02:09 |
| 35671415073 | (workflow_dispatch) | 09-22 00:18 |
| 35668907162 | worker: crf18 review copies… | 09-21 23:44 |
| 35653363616 | ci: pass R2 settings… | 09-21 20:48 |

  **Both `33f5820` and `a3ea33b` did rebuild and redeploy.**
- Endpoint `wv9oneserd7vj6` (read-only; the id matches `.env`), template `25514mi5ae`:
  **`workersMin 0 / workersMax 3` — NOT 0/0.**
  - `/health` shows workers idle 3 / ready 3 / running 0, jobs inQueue 0.
  - Not changed, per the dispatch. Question for Arul: scale it to 0/0?

## Part B — commit
- `_ab6` dry-run: 4 rows, 2–3 SEPARATE refs, max ~503 tokens, no REF MISSING, no OVER BUDGET.
  `py_compile` of `batch_runner.py` and `upscale_video.py` OK.
- The add set is the dispatch's list plus this report. `build_song_refs.py` had no changes, so its add was a no-op.
  There is no `.env`, `logs.txt`, `nil`, `out/` or `outputs/` in it.
- Committed as "phase 6b: …" `[skip ci]` (the hash is in CC's chat reply). The push covers B0 and B.

## Part C — set-plate test (832×480, seed 30313)
- **Pod `1t4q257jvobzy0`:** A100-SXM4-80GB, community cloud, **$1.39/h**. H100 community: no instances.
  - Created 01:33:47 UTC. It stopped itself at 02:02:44 UTC via the stop-cmd (out-push first).
  - Deleted after confirming `EXITED`; `pod get` now returns 404.
  - **~29 min ≈ $0.67** (budget: ≤ 35 min / $0.80).
- **Env import worked:** `pull` ran with **no `r2env.sh`** and no "missing env", using only the stock `pod_bootstrap.sh` copied over.
- **`pull` lines:**
  - First pull: models 418 s, total 430 s. Phantom was verified from R2. `WanVaceToVideoMultiRef` was MISSING
    (the template's ComfyUI was already running).
  - After the restart (`pkill` + `pull`): `BOOT-TO-READY: models 7 s, total 28 s`, with **node OK** for
    `WanVaceToVideoMultiRef`, `WanPhantomSubjectToVideo` and `ImageBatch`.
- **How the batch ran:** in the foreground of a **tmux** session on the pod, not `nohup &`. That kept normal signals and meant an SSH
  drop could not kill the runner before its stop-cmd. The literal pod id was in the stop-cmd. A laptop-side backstop was set
  to stop the pod at 02:20 UTC; it was not needed.

| row | refs | mode | wall s |
|---|---|---|---|
| T04_noset | 1 | distilled 6 | 110.0 (includes the first model load) |
| T04_set | 2 | distilled 6 | 70.0 |
| T08_set | 3 | distilled 6 | 80.0 |
| T07_set | 3 | full 30 | 640.3 |

- The runner reported 15.0 GPU-min. `grep -c "lora key not loaded" comfyui.log` → **0**. No traceback, no OOM.
- `vram.log` was not shipped this time: `out-push` only ships the ComfyUI and batch logs, and the pod is gone.
- Paths (all under `C:\Projects\opencode\video_image\songs\_ab6-2026-09-27-setplate\out\`):
  - `...\out\T04_noset-seed30313-s6.mp4`, `...\out\T04_noset-seed30313-s6.json`, `...\out\_qc\T04_noset-strip.png`
  - `...\out\T04_set-seed30313-s6.mp4`, `...\out\T04_set-seed30313-s6.json`, `...\out\_qc\T04_set-strip.png`
  - `...\out\T08_set-seed30313-s6.mp4`, `...\out\T08_set-seed30313-s6.json`, `...\out\_qc\T08_set-strip.png`
  - `...\out\T07_set-seed30313-s30.mp4`, `...\out\T07_set-seed30313-s30.json`, `...\out\_qc\T07_set-strip.png`
  - **Grid (frame 40, 2×2):** `C:\Projects\opencode\video_image\songs\_ab6-2026-09-27-setplate\out\_qc\ab6-grid-f40.png`
    - top-left T04_noset, top-right T04_set
    - bottom-left T08_set, bottom-right T07_set
  - Logs: `...\out\_debug\batch_ab6.log`, `...\out\_debug\comfyui.log`

**Not judged.** Fable checks:
- the same house in T04_set / T08_set / T07_set, matching the plate;
- night kept;
- no floating diorama;
- T07_set shows two distinct children.

## Cost
Part C $0.67. Parts A, B0 and B $0. **Total: $0.67.**
