# item-02 — Phantom-Wan-14B subject-to-video, same two shots, separate refs

**Why:** Phantom is ByteDance's subject-consistency finetune of Wan2.1-T2V-14B; its native ComfyUI node
`WanPhantomSubjectToVideo` encodes up to 4 reference images one by one (verified in `comfy_extras/nodes_wan.py`).
Same text encoder, VAE and (probably) the lightx2v LoRA as our stack — only the 29 GB diffusion model is new.
**Budget for this item: ≤ 40 min pod time (~$2.35 on an H100). `--max-minutes 30` for the batch itself.**
Model: `https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Phantom-Wan-14B_fp16.safetensors` — expected size
**29,052,237,696 bytes** (from the HF listing; the pod must report exactly that).

## Steps
1. **Fresh pod** exactly as item 1 step 3 (H100 80 GB, R2 env, `pull` with three `node OK`). Then on the pod:
   ```
   bash /workspace/pod_bootstrap.sh model-get https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Phantom-Wan-14B_fp16.safetensors diffusion_models/Phantom-Wan-14B_fp16.safetensors
   curl -s -A "Mozilla/5.0 WanComfyDriver" http://127.0.0.1:8188/object_info/UNETLoader | grep -o "Phantom-Wan-14B_fp16.safetensors" | head -1
   ```
   `model-get` prints the byte size — it must equal 29,052,237,696, else stop the pod and `item-02.blocked` (a partial
   file would waste the whole batch). If the `grep` prints nothing, restart ComfyUI (`pkill -f "main.py --listen"`,
   then `bash /workspace/pod_bootstrap.sh pull` again — models are already on disk, it takes seconds) and re-check.
2. Cheap row first (it also tells us whether the lightx2v LoRA applies to Phantom):
   ```
   cd /workspace/wan
   python comfy/batch_runner.py --song songs/_ab4-2026-09-23 --hosts http://127.0.0.1:8188 --only T17_ph_d,T17_ph,T07_ph --dry-run
   python comfy/batch_runner.py --song songs/_ab4-2026-09-23 --hosts http://127.0.0.1:8188 --seed 30313 --only T17_ph_d,T17_ph,T07_ph \
       --max-minutes 30 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/_ab4-2026-09-23; bash /workspace/pod_bootstrap.sh model-push diffusion_models/Phantom-Wan-14B_fp16.safetensors; runpodctl stop pod $RUNPOD_POD_ID"
   ```
   The stop-cmd pushes Phantom to R2 (`wan-models/models/diffusion_models/`, added to `MANIFEST.txt`; ~$0.45/month,
   so no re-download next time) and then stops the pod whatever happened before (`;` on purpose, not `&&`).
   If the FIRST row fails with `EXECUTION ERROR` (model failed to load in `UNETLoader`, or a node error): copy the error
   + traceback from `/workspace/comfyui.log`, make sure the pod stopped, `item-02.blocked`. No fixes, no retries.
3. Before the pod stops (or from the log if it already did): `grep -c "lora key not loaded" /workspace/comfyui.log` and
   the first 3 such lines — that is the LoRA-compatibility answer for T17_ph_d.
4. Confirm stopped → `runpodctl remove pod <id>`. Pull `out/` to the laptop as in item 1 step 5.
5. Write `item-02.report.md` (same table/paths/cost format as item 1, plus: `model-get` size + wall time, the
   `model-push` lines incl. `manifest now N files`, the LoRA grep). Create `item-02.done`, wait for `item-02.verdict`.
   After the verdict: there is no item-03 — append `QUEUE END` to `LOG.md` and exit.
