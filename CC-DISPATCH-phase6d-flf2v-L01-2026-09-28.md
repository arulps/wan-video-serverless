# CC-DISPATCH — Phase 6d: loop Shorts on Wan2.2 first-last-frame (L01 Peekaboo) (2026-09-28)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine). Parts A → D **in one go, end to end**
(upscale starts by itself after the pod is gone); stop early only on a failure named below.
**Budget: Part B ≤ 90 min pod time (~$2.10 A100 community / ~$2.40 secure), `--max-minutes 55` for the batch.
Parts A, C, D $0.** Standing rules: one pod, fresh, stopped and removed before reporting; no retakes / extra seeds;
never print `.env` values; edit `shots.csv` cells, never restore it; report **full Windows paths**.

## 0 · Why (Arul chose option 1, 2026-09-28)
6c showed Phantom cannot do hide → reveal (empty rooms, pop-ins, a floating head) and cannot pin the last frame, so
no loop. Every Short must loop. Wan2.2-I2V-A14B with ComfyUI's core `WanFirstLastFrameToVideo` takes a first AND a
last frame: the same still in both places closes the loop by design, and Minnu's look comes from that still. The loop
is rotated to start on the "peekaboo!" frame (face out) so her face is in the still — a hidden-start still would give
the model no face to copy. Different model from the songs (Phantom), acceptable for stand-alone Shorts.

## 1 · On disk (Fable; tested; not committed)
| file | change | tested |
|---|---|---|
| `comfy/wan22_flf2v_api.json` | **new** API workflow: 2 UNETs (high/low noise), 2 Lightning LoRAs, 2 `ModelSamplingSD3`, `WanFirstLastFrameToVideo` (start_image/end_image), 2 `KSamplerAdvanced` splitting one schedule, VAE decode, SaveVideo | JSON + link check in the mock |
| `comfy/run_comfy.py` | `FLF2V_MODES` + `build_flf2v_workflow()`. distilled = Wan2.2-Lightning I2V Seko-V1 settings from its own NativeComfy workflow (4 steps split 2/2, cfg 1, euler/simple, shift 5); full = no LoRA, 20 steps split 10/10, cfg 3.5, euler/simple, shift 8 (ComfyUI Wan2.2 template values — verified on the pod in B3) | mock |
| `comfy/batch_runner.py` | `engine=flf2v`; new optional column `lastframe` (blank = keyframe again = loop); `ref` not required for flf2v; dry-run prints `lastframe=<same as keyframe> (seamless loop)`; sidecar records sampler/shift/LoRA/lastframe | `tests/test_flf2v_mock.py` PASS; dry-runs of _ab4/_ab6/twinkle/row unchanged |
| `tests/test_flf2v_mock.py` | **new**: fake ComfyUI checks every submitted flf2v workflow (links, frames, sampler split, LoRA on/off) | PASS |
| `scripts/pod_bootstrap.sh` | `PULL_SKIP=<regex>`: pull only the manifest files a batch needs (the manifest grows by ~60 GB here); `wait_ready` waits for the first pulled diffusion model (`READY_MODEL`) instead of hard-coded VACE; node check adds `WanFirstLastFrameToVideo`, `KSamplerAdvanced` | `bash -n`; filter + READY_MODEL logic on a sample manifest for both engines |
| `scripts/upscale_video.py` | ncnn: smallest animevideov3 scale that reaches the target (720p → 4K = x3 exactly, ~2x faster than x4 + shrink), if the x2/x3 model file exists, else x4 | fake-binary test: 720x1280 → x3 → 2160x3840; 480x832 → x4 → 2216x3840 |
| `docs/SHOT-LIST-SPEC.md` | `flf2v` engine + `lastframe` column | — |
| `songs/shorts-loops/shots/L01-flf.txt`, `shots.csv` (+3 rows) | L01 rotated loop: face out → hide → face out. Rows `L01_flf_d` (distilled, seed 30313), `L01_flf_d2` (distilled, 4242), `L01_flf_f` (full, 30313), all 720x1280, keyframe `keyframes/L01-start.png` | dry-run: 3 rows, ~442 tokens, KEYFRAME MISSING until A1 |
| `C:\Channel Contents\MinMiniKids\YT Shorts\keyframes\L01-KEYFRAME-BRIEF.md` | what Arul makes: the still, its prompt, the checks | — |

## Part A — keyframe, tests, commit ($0)
1. **Keyframe.** If `C:\Channel Contents\MinMiniKids\YT Shorts\keyframes\L01-start.png` (or `.jpg`/`.jpeg`) does not
   exist: **stop here** and tell Arul "L01 keyframe still needed — see L01-KEYFRAME-BRIEF.md". If it exists, fit it:
   ```
   python -c "from PIL import Image; import sys; im=Image.open(sys.argv[1]).convert('RGB'); w,h=im.size; t=9/16; cw,ch=(int(h*t),h) if w/h>t else (w,int(w/t)); x,y=(w-cw)//2,(h-ch)//2; im.crop((x,y,x+cw,y+ch)).resize((720,1280),Image.LANCZOS).save(sys.argv[2])" "C:\Channel Contents\MinMiniKids\YT Shorts\keyframes\L01-start.png" songs\shorts-loops\keyframes\L01-start.png
   ```
   Report the source size and whether it had to be cropped (source not 9:16).
2. ```
   python tests\test_flf2v_mock.py                                   -> ends with PASS
   python -m py_compile comfy\run_comfy.py comfy\batch_runner.py scripts\upscale_video.py
   bash -n scripts/pod_bootstrap.sh
   python comfy\batch_runner.py --song songs\shorts-loops --hosts http://x --dry-run   -> 3 rows (L01_flf_*), no MISSING, no OVER BUDGET
   ```
3. Commit (scripts/ changed → **`[skip ci]` is required**, it stops the serverless redeploy):
   ```
   git add comfy/wan22_flf2v_api.json comfy/run_comfy.py comfy/batch_runner.py tests/test_flf2v_mock.py scripts/pod_bootstrap.sh scripts/upscale_video.py docs/SHOT-LIST-SPEC.md songs/shorts-loops/shots.csv songs/shorts-loops/shots/L01-flf.txt songs/shorts-loops/keyframes/L01-start.png songs/_ab6-2026-09-27-setplate/REVIEW-2026-09-27.md songs/shorts-loops/REVIEW-L01-2026-09-28.md CC-REPORT-phase6c.md CC-DISPATCH-phase6d-flf2v-L01-2026-09-28.md
   git commit -m "flf2v engine: Wan2.2-I2V-A14B first-last-frame loops (L01 Peekaboo); PULL_SKIP per-engine model pull; x3 upscale for 720p [skip ci]"
   git push
   ```
   Then `gh run list --workflow deploy.yml -L 1` must NOT show a run for this commit. `bash scripts/pod_bootstrap.sh wan-push`.

## Part B — pod (≤ 90 min)
1. Fresh A100 80 GB (community → secure; H100 if community has one), **container disk ≥ 150 GB** (Wan2.2 adds ~60 GB),
   R2 env vars in the console, copy `pod_bootstrap.sh`, then pull **only what flf2v needs**:
   `PULL_SKIP='Phantom|vace|lightx2v_cfg_step_distill' bash pod_bootstrap.sh pull`
   (first time the Wan2.2 files are not on R2 yet, so this pulls just the text encoder + VAE.)
2. Fetch the four new files onto the pod (report each size; expected 28.6 GB, 28.6 GB, 1.23 GB, 1.23 GB):
   ```
   bash pod_bootstrap.sh model-get https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_i2v_high_noise_14B_fp16.safetensors diffusion_models/wan2.2_i2v_high_noise_14B_fp16.safetensors
   bash pod_bootstrap.sh model-get https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_i2v_low_noise_14B_fp16.safetensors diffusion_models/wan2.2_i2v_low_noise_14B_fp16.safetensors
   bash pod_bootstrap.sh model-get https://huggingface.co/lightx2v/Wan2.2-Lightning/resolve/main/Wan2.2-I2V-A14B-4steps-lora-rank64-Seko-V1/high_noise_model.safetensors loras/wan22_i2v_lightning_4step_high.safetensors
   bash pod_bootstrap.sh model-get https://huggingface.co/lightx2v/Wan2.2-Lightning/resolve/main/Wan2.2-I2V-A14B-4steps-lora-rank64-Seko-V1/low_noise_model.safetensors loras/wan22_i2v_lightning_4step_low.safetensors
   ```
3. **Template check (read-only).** Find ComfyUI's bundled Wan2.2 first-last-frame template on the pod
   (`python3 -c "import comfyui_workflow_templates,os;print(os.path.dirname(comfyui_workflow_templates.__file__))"`,
   then a `*wan2_2*flf2v*.json` under it) and report its KSamplerAdvanced values (steps, cfg, sampler, scheduler,
   start/end steps) and ModelSamplingSD3 shift. If they differ from full = 20 / 3.5 / euler / simple / split 10 / shift 8,
   **report the difference and run as written** (Fable adjusts later). If no template is found, say so.
4. Restart ComfyUI once (`pkill -f "main.py --listen"`, then the same `PULL_SKIP=... bash pod_bootstrap.sh pull`) until
   the node check says OK for `WanFirstLastFrameToVideo` and `KSamplerAdvanced`, and
   `curl -s http://127.0.0.1:8188/object_info/UNETLoader | grep -c wan2.2_i2v` finds both experts (the ready line itself
   is generic this time: the Wan2.2 files are not in the R2 manifest until step 5).
5. **Push the models to R2 in parallel** (second tmux window) so later pods pull them from R2:
   `for f in diffusion_models/wan2.2_i2v_high_noise_14B_fp16.safetensors diffusion_models/wan2.2_i2v_low_noise_14B_fp16.safetensors loras/wan22_i2v_lightning_4step_high.safetensors loras/wan22_i2v_lightning_4step_low.safetensors; do bash /workspace/pod_bootstrap.sh model-push $f; done 2>&1 | tee /workspace/model_push.log`
6. Batch in the foreground of tmux window 1; the stop-cmd **waits for model-push to finish** before out-push + stop:
   ```
   cd /workspace/wan
   python3 comfy/batch_runner.py --song songs/shorts-loops --hosts http://127.0.0.1:8188 --seed 30313 --dry-run
   python3 comfy/batch_runner.py --song songs/shorts-loops --hosts http://127.0.0.1:8188 --seed 30313 --max-minutes 55 \
     --stop-cmd "while pgrep -f 'pod_bootstrap.sh model-push' >/dev/null; do sleep 20; done; bash /workspace/pod_bootstrap.sh out-push songs/shorts-loops; runpodctl stop pod <POD_ID>" 2>&1 | tee /workspace/batch_6d.log
   ```
   Order is CSV order: `L01_flf_d`, `L01_flf_d2` (distilled, expect ~4–6 min each, the first includes loading two
   28.6 GB experts), `L01_flf_f` (full, expect ~25–30 min). If the first row fails: STOP file, report the error.
   Watch the log for OOM on the full row (a finding, not a retry).
7. Confirm stopped → delete. Pull `out/` (+ `_debug/`) to the laptop. Report `model_push.log` tail (4 × OK, manifest count).
   **From now on every pull sets PULL_SKIP** (Phantom batches: `PULL_SKIP='wan2\.2_i2v|wan22_i2v_lightning|vace'`),
   otherwise each pod downloads ~60 GB it does not use.

## Part C — upscale + loop check ($0, laptop)
```
cd songs\shorts-loops\out ; mkdir 4K ; mkdir _qc\loop
foreach ($c in "L01_flf_d-seed30313-s4","L01_flf_d2-seed4242-s4","L01_flf_f-seed30313-s20") {
  powershell -ExecutionPolicy Bypass -File ..\..\..\scripts\upscale.ps1 "$c.mp4" -Dst "4K\$c-4K30.mp4" -Height 3840 -Fps 30
  ffmpeg -y -stream_loop 2 -i "$c.mp4" -c copy "_qc\loop\$c-x3.mp4"
  ffmpeg -y -i "$c.mp4" -vf "select='eq(n\,0)+eq(n\,80)',scale=360:-2,tile=2x1" -vsync 0 -frames:v 1 "_qc\loop\$c-first-last.png"
}
```
(Use the literal names in the `-Dst` path — 6c's loop wrote `4K$c` once; check each output name.) Sidecars must say
`ncnn scale x3` in the console log and `rife-v4.6 81->152`. Copy the three 4K files and the three `-x3.mp4` loop previews
to `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\flf\`.

## Part D — commit + report ($0)
Commit `songs/shorts-loops/shots.csv` (statuses) + `CC-REPORT-phase6d.md` with `[skip ci]`. Report: keyframe fit
(A1), test output, commit hashes, pod id/GPU/rate, the four model-get sizes + times, template values (B3), pull lines,
per-row wall s, peak VRAM if logged, model-push result, upscale sidecar values + s/frame, all full Windows paths,
$ total. **Do not judge the clips** — Fable checks: Minnu on-model; hides and pops out; last frame = first frame
(the loop previews); no floating head; 4K detail.
