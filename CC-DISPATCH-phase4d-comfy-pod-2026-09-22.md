# CC-DISPATCH — Phase 4d: fast VACE on a ComfyUI pod (few-step LoRA A/B) — 2026-09-22

**Goal:** prove a 720p / 5 s reference-to-video clip in **≤ 6 min and ≤ $0.50** with identity and blocking intact,
using a maintained stack (native ComfyUI Wan VACE + the lightx2v step/cfg distillation LoRA) instead of more
hand-rolled worker code. **Gate:** if it passes, Phase 4e = a pod batch runner (network volume + auto-stop) for whole-song batches; serverless stays for on-demand single shots. If it
fails on quality, we stop investing in self-hosted generation and keep the endpoints for post-processing/batch.
**Executor:** CC, fully headless (pod shell + ComfyUI HTTP API via `comfy/run_comfy.py`). No UI clicks required.
**Budget:** one RunPod **pod** (not serverless), H100 80 GB or A100 80 GB, ~$3–4/h, hard stop at **2 h / $8**.
Pods have no cold-start churn and no CI deploy per attempt — that's why experiments go here.

## 0 · Sources (read 2026-09-22, not from memory)
- ComfyUI official VACE tutorial `docs.comfy.org/tutorials/video/wan/vace`: models `wan2.1_vace_14B_fp16.safetensors`
  (diffusion_models, ~32 GB), `umt5_xxl_fp8_e4m3fn_scaled.safetensors` (text_encoders), `wan_2.1_vae.safetensors`
  (vae); nodes `WanVaceToVideo(reference_image, control_video, control_masks, strength, width, height, length,
  batch_size)` → `TrimVideoLatent` → `VAEDecode`; "multiple reference images in a single image".
- Official template "Wan2.1 VACE 14B reference-to-video" (`comfy.org/workflows/video_wan_vace_14B_ref2v-…`): defaults
  steps 20, cfg 6.0; note: "With CausVid LoRA use fewer steps (2–4) and a low cfg (~1.0)".
- LoRA: `lightx2v/Wan2.1-T2V-14B-StepDistill-CfgDistill-Lightx2v` → `loras/Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank64.safetensors`
  (631 MB). Model card: **4 steps, guidance 1.0 (no CFG), shift 5.0, LCM scheduler**.
- Note: native `WanVaceToVideo` takes ONE `reference_image`, so multi-view refs go in as a single sheet
  (Fable built the 16:9 sheets under `outputs\vace\refs\`). Our own worker fed 4 separate
  refs; identity may differ slightly — that is part of what this A/B measures.

## 1 · Pod
1. RunPod → Pods → deploy **H100 80GB** (or A100 80GB) with the official **ComfyUI** template (any recent
   `runpod/comfyui`-style template that exposes port 8188; 100 GB container disk). Enable SSH. Note the pod id.
2. `runpodctl` / ssh in. Confirm `ComfyUI/` path and that the UI answers on 8188 (proxy URL from the console).
3. Download models (HF, ~40 GB total; use `hf download` or `wget` — on a pod the network is unmetered):
```
cd /workspace/ComfyUI/models   # adjust if the template uses another root
wget -c -O diffusion_models/wan2.1_vace_14B_fp16.safetensors \
  https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/diffusion_models/wan2.1_vace_14B_fp16.safetensors
wget -c -O text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors \
  https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors
wget -c -O vae/wan_2.1_vae.safetensors \
  https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors
wget -c -O loras/Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank64.safetensors \
  https://huggingface.co/lightx2v/Wan2.1-T2V-14B-StepDistill-CfgDistill-Lightx2v/resolve/main/loras/Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank64.safetensors
```
   Verify sizes (32 GB / ~6.7 GB / ~250 MB / 631 MB). If a URL 404s, look the file up in that repo's tree — do not
   substitute a different model.
4. Copy to the pod (`runpodctl send` or scp), or skip this and run the driver from the laptop against the proxy URL:
   `comfy/`, `outputs\vace\refs\*-16x9.png`, `prompts\mazhai\`. The driver uploads the ref itself via the API.

## 2 · Workflow — headless, no UI needed
Fable wrote the API-format workflow and a driver (node/input names verified against ComfyUI master source on 2026-09-22:
`UNETLoader`, `CLIPLoader(type=wan)`, `VAELoader`, `LoraLoaderModelOnly`, `ModelSamplingSD3`, `CLIPTextEncode`×2,
`LoadImage`, `WanVaceToVideo`, `KSampler`, `TrimVideoLatent`, `VAEDecode`, `CreateVideo`, `SaveVideo`):
- `comfy/vace_ref2v_api.json` — the graph with placeholders.
- `comfy/run_comfy.py` — stdlib-only driver: uploads the ref (`/upload/image`), patches prompt/ref/steps/cfg/shift/
  seed/size/LoRA, queues (`/prompt`), polls `/history`, downloads the mp4 (`/view`), writes a `.json` sidecar with
  wall time. Tested end to end against a mock server. `--no-lora` bypasses the LoRA node for the control run.
- Reference sheets rebuilt at exactly **1280×720** (`outputs\vace\refs\minnu-4view-16x9.png`,
  `mintu-2ref-16x9.png`, `mintu-lawn-16x9.png`) because `WanVaceToVideo` centre-crops the reference to the output
  aspect — a wide sheet would have lost the outer views.

Copy `comfy/`, the three 16:9 sheets and `prompts/mazhai/` to the pod (or run the driver from the laptop against the
pod's proxied 8188 URL — `--host https://<podid>-8188.proxy.runpod.net`). If `/prompt` rejects the graph, the driver
prints ComfyUI's `node_errors` naming the exact input; fix that one key in the JSON (most likely candidate:
`SaveVideo`'s `format`/`codec` keys — check with `--schema SaveVideo`). The UI route (Templates → Wan VACE
reference-to-video) remains the fallback if the API graph cannot be made to validate in 15 minutes.

## 3 · Runs (CC, from the pod shell or the laptop)
```
P=python; H=http://127.0.0.1:8188        # or the proxy URL from the laptop
$P comfy/run_comfy.py --host $H --ref outputs/vace/refs/minnu-4view-16x9.png --prompt-file prompts/mazhai/V2c-minnu-impatience-v3.txt --negative-file prompts/mazhai/NEGATIVE.txt --label v2c-A1 --steps 4 --cfg 1.0 --shift 5.0 --sampler lcm
$P comfy/run_comfy.py --host $H --ref outputs/vace/refs/minnu-4view-16x9.png --prompt-file prompts/mazhai/V2c-minnu-impatience-v3.txt --negative-file prompts/mazhai/NEGATIVE.txt --label v2c-A2 --steps 6 --cfg 1.0 --shift 5.0 --sampler lcm
$P comfy/run_comfy.py --host $H --ref outputs/vace/refs/mintu-2ref-16x9.png  --prompt-file prompts/mazhai/V1a-mintu-at-glass-v3.txt --negative-file prompts/mazhai/NEGATIVE-v1a.txt --label v1a-B --steps 4 --cfg 1.0 --shift 5.0 --sampler lcm
$P comfy/run_comfy.py --host $H --ref outputs/vace/refs/minnu-4view-16x9.png --prompt-file prompts/mazhai/V2c-minnu-impatience-v3.txt --negative-file prompts/mazhai/NEGATIVE.txt --label v2c-C --no-lora --steps 30 --cfg 5.0 --shift 5.0 --sampler uni_pc
```
| run | config | expect |
|---|---|---|
| A1 | V2c-v3, minnu sheet, lightx2v, 4 steps, cfg 1, shift 5, 1280×720×81 | 1–3 min |
| A2 | same, 6 steps | 2–4 min |
| B  | V1a-v3, mintu 2-ref sheet, NEGATIVE-v1a, lightx2v 4 steps | 1–3 min |
| C (control) | V2c-v3, no LoRA, 30 steps, cfg 5, uni_pc | 15–25 min — calibrates native-Comfy vs our worker |

Record per run: `wall_s` from the sidecar, peak VRAM (`nvidia-smi --query-gpu=memory.used --format=csv -l 5` in a
second shell), file size, and the 5-frame strip (same ffmpeg line as 4b). Files land in `outputs/vace/pod/` — bring
them to the laptop if the driver ran on the pod. **Stop the pod** when done (the money rule); keep the pod template.
If you created a network volume (see §6), keep it — it is $3/month and saves the 40 GB download next time.

## 4 · Pass / fail (Fable judges the strips against tonight's 720p V2c keeper)
Pass = A1 or A2 holds face/pigtails/bows/dungarees and the turn-to-camera beat at least as well as C, in ≤ 6 min.
Then Phase 4e: `comfy/batch_runner.py` — a shot-list CSV in, all clips out, auto-stop of the pod when the queue drains;
models + ComfyUI on a RunPod network volume so a pod is productive 2 minutes after boot. See §6.
Fail = visible identity loss or motion collapse at 4–6 steps even with the control C looking right → we stop
self-hosted generation work; keep the 5B/VACE endpoints for post-processing and batch only; OpenArt for generation.

## 5 · Not in this dispatch
- SageAttention / TeaCache / fp8 DiT: only if A1/A2 pass but miss the 6-min gate (they are further 1.5–2× levers).
- The I1 two-shot and the remaining Mazhai shots — production waits for the gate.
- Any change to the repo's worker code. Commit only this dispatch and the two ref sheets' provenance note.

## 6 · Pod vs serverless for production (decision input for 4e)
> **Superseded 2026-09-22 (4e rev 2):** the network volume is replaced by the existing Cloudflare R2 bucket as the model origin (`scripts/pod_bootstrap.sh`): ~$0.60/mo, zero egress, any datacenter, ~10 min boot instead of ~2. See `CC-DISPATCH-phase4e-batch-2026-09-22.md` §2.

Pod H100 80 GB ≈ $3–4/h regardless of load; serverless H100 ≈ $4.2/h of *active* time plus a cold model load
(~1–2 min) per scale-up and idle-timeout tail. For batch production (4 songs ≈ 100 shots in one sitting) a pod with a
**network volume** holding the models + ComfyUI (40 GB ≈ $3/month) is cheaper per clip, has no cold starts, and can run
a whole shot list unattended from one script. At the distilled target (~4 min/clip) 100 shots ≈ 7 h ≈ **$25**; at the
current 30-step rate it would be ~42 h ≈ $150 — which is why 4d's gate comes first. The risk is idle burn: the batch
runner must stop the pod itself (`runpodctl stop pod <id>`) when the queue drains, and the pod gets a hard max-runtime.
Serverless stays for on-demand single shots (e.g. from Oviyan later); it costs nothing at 0 workers.

