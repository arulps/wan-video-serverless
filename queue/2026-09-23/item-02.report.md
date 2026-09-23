# item-02 report — Phantom-Wan-14B subject-to-video, same two shots, separate refs

## Result: DONE — 3/3 rows succeeded after Fable's template fix

Ran the full batch exactly as `item-02.verdict`'s second REDO specified.

### Pod
- id `vv4wl320tibhql`, name `queue-0923-item2c`, **A100 80GB PCIe, secure cloud**, $1.59/h (community cloud: zero
  capacity for both H100 and A100 again — 4th time in a row this queue; A100 secure also needed 2 retries before a
  `pod create` succeeded, community/secure supply is generally tight right now).
- `wan-push` from the laptop first (ships the fixed `comfy/phantom_s2v_api.json` + reordered `shots.csv`). `pull`:
  178s (models cached in R2 from earlier attempts, fast). One more SSH-drop during the ComfyUI restart (5th
  occurrence of this gotcha across the queue) — recovered the same way as before (checked process state over a
  fresh connection, started ComfyUI manually). All three nodes confirmed OK.
- Phantom model: still not cached (the first blocked attempt's `model-push` never ran, and this is a fresh pod) —
  re-downloaded once more (~19 min), verified **29,052,237,696 bytes** again, `UNETLoader` confirms it. **Pushed to
  R2 immediately after** (`model-push`, before the batch, per the verdict) — manifest now 5 files, so this download
  never has to happen again for this model.
- Rented 16:35:13 → stop-cmd's `runpodctl stop pod` fired 17:35:07 UTC = **59.9 min ≈ $1.59** (close to Fable's
  ~$1.60 cap; most of it is the model re-download + the two full-sampling rows, ~700s of GPU time each).
- Removed after confirming `EXITED`.

### Batch — 3/3 done, 0 failed, 25.4 GPU-minutes (runner-reported)
Ran in CSV order (now cheap-first, as Fable reordered `shots.csv`) — matches `--only` order this time, no repeat
of item-01's ordering surprise.

| row | status | wall_s | mp4 | qc strip | json |
|---|---|---|---|---|---|
| T17_ph_d | done | 120.2 | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T17_ph_d-seed30313-s6.mp4` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\_qc\T17_ph_d-strip.png` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T17_ph_d-seed30313-s6.json` |
| T17_ph | done | 700.5 | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T17_ph-seed30313-s30.mp4` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\_qc\T17_ph-strip.png` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T17_ph-seed30313-s30.json` |
| T07_ph | done | 700.4 | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T07_ph-seed30313-s30.mp4` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\_qc\T07_ph-strip.png` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T07_ph-seed30313-s30.json` |

No `EXECUTION ERROR`, no `PROMPT REJECTED`, no `Traceback` — the template fix held across all 3 rows including
both full-sampling ones.

### LoRA-compatibility grep (item step 3)
`grep -c "lora key not loaded" comfyui.log` → **0**. Also grepped the whole debug log for `error|traceback` —
**nothing matched at all**, a fully clean run.

### model-push (before the batch, per the verdict)
```
[17:07:57]   OK   diffusion_models/Phantom-Wan-14B_fp16.safetensors 29052237696
[17:07:57] model-push done -> r2:minmini-wan/wan-models/models/diffusion_models/Phantom-Wan-14B_fp16.safetensors (manifest now 5 files)
```

### Output (all pulled to the laptop at the full paths above, plus)
- `songs/_ab4-2026-09-23/out/_debug/batch_item2c.log`, `.../out/_debug/comfyui.log`

## Cost this run: **≈ $1.59** (59.9 min × $1.59/h)
## Running total this queue: **≈ $4.27 of the $6 hard limit** ($0.97 item-01 + $0.61 item-02 attempt-1 + $1.10 item-02 redo-1 + $1.59 item-02 redo-2)

**QC strips not frame-checked by me — that's Fable's call, same division of labor as item-01.**

`item-02.done` created (all 3 rows succeeded this time). Waiting for verdict.

---

## Prior redo (superseded above): diagnostic single-row rerun, root cause found (template bug, not infra)

Ran Fable's diagnostic redo exactly as specified: one row only (`T17_ph_d`), 12-min cap, updated

Ran Fable's diagnostic redo exactly as specified: one row only (`T17_ph_d`), 12-min cap, updated
`pod_bootstrap.sh` (`out-push` now ships `comfyui.log`/`batch*.log` to R2 `out/_debug/` before the pod stops).

**Result: still BLOCKED, but this time with a confirmed, specific root cause.** `songs/_ab4-2026-09-23/out/_debug/batch_item2b.log`:
```
[T17_ph_d] FAILED on http://127.0.0.1:8188: PROMPT REJECTED (fix the named node input and rerun):
{"error": {"type": "prompt_outputs_failed_validation", ...},
 "node_errors": {"10": {"errors": [{"type": "return_type_mismatch",
   "message": "Return type mismatch between linked nodes",
   "details": "latent_image, received_type(CONDITIONING) mismatch input_type(LATENT)",
   "extra_info": {"input_name": "latent_image", ...,
     "received_type": "CONDITIONING", "linked_node": ["9", 2]}}],
   "dependent_outputs": ["14"], "class_type": "KSampler"}}}
total GPU-minutes (done shots): 0.0
```
This is a ComfyUI **graph validation** error, rejected before any node executes (0.0 GPU-minutes, no
sampling/model-load lines anywhere in `comfyui.log` — confirmed by grepping it for
`error|traceback|lora key not loaded`, only the same 4 `[ERROR]` lines matched, nothing else). Not OOM, not a
missing node, not a LoRA-compatibility issue — the LoRA grep the item asked for is moot here since sampling
never starts, so `lora key not loaded` can never appear.

**Traced to source:** `comfy/phantom_s2v_api.json` (the checked-in Phantom workflow template) wires **both**
KSampler (node `10`) inputs `negative` **and** `latent_image` to the same output, `["9", 2]`, of node `9`
(`WanPhantomSubjectToVideo`):
```json
"10": {"class_type": "KSampler", "inputs": {
  "model": ["5", 0], "positive": ["9", 0],
  "negative": ["9", 2], "latent_image": ["9", 2], ...}}
```
Output slot 2 of `WanPhantomSubjectToVideo` is a CONDITIONING output, not the LATENT output (which is almost
certainly slot 3 on this node) — `latent_image` needs to point there instead. One-line template bug, unrelated
to anything run on the GPU side; VACE's template (`comfy/vace_ref2v_api.json`) wires its KSampler correctly
(item-01 had zero validation errors across 3 rows), so this is specific to the Phantom template only.
**Not fixed** — out of scope for "run the item and report", and both the item and the verdict said no fixes.

### Redo pod/cost
- Fresh pod `srfb2ea7361cux`, A100 80GB PCIe secure cloud, $1.59/h (community cloud: zero capacity again for
  both H100 and A100, third time in a row). `wan-push` ran from the laptop first; updated `pod_bootstrap.sh`
  scp'd onto the pod directly (uncommitted, laptop-only, same as every prior pass). Pull, node check (all 3
  `node OK` after one restart — a first restart attempt's SSH session dropped silently mid-command, same known
  gotcha as before; recovered by starting ComfyUI manually over a fresh connection). Phantom model **not**
  cached in R2 (the first attempt's `model-push` never ran), so a full fresh 29 GB re-download was unavoidable
  (~19 min, verified again at exactly 29,052,237,696 bytes).
- Rented 15:15:13 → stopped 15:56:42 UTC = **41.5 min ≈ $1.10**. This is well over Fable's "~$0.50" estimate —
  almost entirely the unavoidable fresh model download plus the SSH-drop recovery detour, not the batch itself
  (which cost $0.00 GPU-minutes). Flagging the gap rather than hiding it; still far under the $6 hard limit.
- Removed after confirming `EXITED`.

### Running total this queue: **≈ $2.68 of the $6 hard limit** ($0.97 item-01 + $0.61 item-02 attempt-1 + $1.10 item-02 redo)

### Output
- `songs/_ab4-2026-09-23/out/_debug/batch_item2b.log`, `.../out/_debug/comfyui.log` — both pulled to the laptop
  at those same paths. No `.mp4`/`.json`/strip — the row never ran (rejected pre-flight).

`item-02.blocked` re-created (the row failed; not a `.done`). Waiting for the next verdict.

---

## Original report (first attempt, superseded above) — batch died within ~2 min of launch, no output produced, no traceback recoverable

## Pod
- id `y2shx23j0byhli`, name `queue-0923-item2`, **A100 80GB PCIe, SECURE cloud**, $1.59/h.
  - H100 (community): `podFindAndDeployOnDemand` returned `SUPPLY_CONSTRAINT` ("no longer any instances available with
    the requested specifications"), same as item-01.
  - A100 80GB (community): also `SUPPLY_CONSTRAINT` ("no longer any instances available"), with and without a pinned
    `CA-MTL-3` datacenter (its `gpu list` stock showed "Low" there).
  - Fell back to A100 80GB **secure** cloud (not tried by item-01, which only tried community) — this succeeded and
    is within the item's own H100/A100-80GB spec; secure-cloud price ($1.59/h) is close to item-01's community A100
    SXM4 price ($1.39/h).
- Created 13:46:01 UTC, container running 13:47 (BOOT-TO-READY 206s including model pull), stop-cmd's
  `runpodctl stop pod` fired at **14:08:55 UTC** = **22.9 min uptime ≈ $0.61**. Pod removed (`runpodctl pod delete`)
  after confirming `desiredStatus: EXITED` — container disk (and its logs) is gone.

## Steps 1–2 (model-get, node check, dry-run) — all clean, no gap here
```
[13:51:15]   node OK   WanPhantomSubjectToVideo
[13:51:15]   node OK   ImageBatch
```
(`WanVaceToVideoMultiRef` reported `MISSING` at this point only because ComfyUI was already running from template
boot before the custom-node copy landed, and item-2 doesn't need it — not investigated further, not a blocker.)

- `model-get` Phantom-Wan-14B_fp16.safetensors: **29,052,237,696 bytes**, exact match to the expected size, in 194s
  (from R2's models pull, not this file specifically — the Phantom download itself ran ~17 min via `wget` from
  HuggingFace, finished clean, size verified byte-for-byte after).
- `curl .../object_info/UNETLoader | grep -o "Phantom-Wan-14B_fp16.safetensors"` → matched. Model is loadable.
- Dry-run (`--only T17_ph_d,T17_ph,T07_ph --dry-run`): all 3 rows `2 SEPARATE references (Phantom native)`, no
  `REF MISSING`, no `OVER BUDGET` (~469–471 tokens). Created the same `python -> python3` symlink item-01 needed
  (this template also has no bare `python`), pre-emptively, before the batch — not diagnosed as the cause of the
  failure below since the symlink was in place before the batch started.

## Step 2 (the real batch) — this is where it broke
Launched at 14:05 UTC:
```
python3 comfy/batch_runner.py --song songs/_ab4-2026-09-23 --hosts http://127.0.0.1:8188 --seed 30313 \
  --only T17_ph_d,T17_ph,T07_ph --max-minutes 30 \
  --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/_ab4-2026-09-23; bash /workspace/pod_bootstrap.sh model-push diffusion_models/Phantom-Wan-14B_fp16.safetensors; runpodctl stop pod $RUNPOD_POD_ID"
```
The pod's `runpodctl stop pod` (the tail of `--stop-cmd`) fired at 14:08:55 — **under 3 minutes after launch**, far
too fast for even the cheap distilled row (item-01's equivalent distilled row alone took 90s of GPU time, but on top
of that there is per-row ComfyUI queue/prompt overhead, and this run needed to load a *freshly-downloaded* 29 GB
diffusion model into VRAM for the first time, which alone should take well over a minute). This is not consistent
with a normal completion of any of the 3 rows.

**I cannot confirm the actual cause.** I do not have a traceback. Evidence:
- R2 `songs/_ab4-2026-09-23/out/` still contains only item-01's three files (`*_vsep*`, timestamps 06:10 UTC) —
  **zero `T17_ph*`/`T07_ph*` files exist**, so `out-push` either ran against an empty/unchanged `out/` dir or never
  ran.
- R2's model manifest under `wan-models/models/diffusion_models/` still only lists `wan2.1_vace_14B_fp16.safetensors`
  — **the Phantom model was never pushed**, so `model-push` also either didn't run or failed silently before upload.
- `runpodctl pod logs` (read-only, works on a stopped pod) only returns Docker/RunPod *system* lifecycle lines, not
  the container's own stdout/stderr — it shows `create container` at 13:46:02, `stop container` at 14:08:55,
  `remove container` immediately after, and `WARN: container is unhealthy: exit code 137: (docker kill?); dead` —
  consistent with `runpodctl stop pod` killing it, tells nothing about *why* the batch stopped early.
- I could not read `/workspace/batch_item2.log` or `/workspace/comfyui.log` (which would have the real answer)
  because the pod was already `EXITED` by the time I checked (SSH connection refused), and **restarting the pod to
  read them was blocked by Claude Code's own auto-mode permission classifier as a real-money action** — correctly,
  since I have no standing authorization to spend more GPU time beyond the bounded run the item already specified.
  I did not attempt to work around that block. I removed the pod instead (stop-only, no further compute cost) per
  the "one pod at a time, stopped before waiting on a verdict" hard limit.

Given item-02's own instruction — *"If the FIRST row fails with EXECUTION ERROR ... copy the error + traceback ...
item-02.blocked. No fixes, no retries."* — and that I cannot produce that traceback, I'm marking this **blocked**
rather than guessing at a root cause (e.g. OOM loading a 14B fp16 model + existing VACE weights already resident;
`--stop-cmd`'s own quoting inside the outer SSH command; a `batch_runner.py` startup exception before any row ran).
Any of these is plausible; none is confirmed.

## LoRA-compatibility grep (item step 3)
**Not obtained** — same reason: needed `/workspace/comfyui.log`, pod was gone before I could read it.

## Cost this item: **≈ $0.61** (22.9 min × $1.59/h)
## Running total this queue: **≈ $1.58 of the $6 hard limit** ($0.97 item-01 + $0.61 item-02)

## What I'd suggest for a redo (not acted on — this is a report, not a decision)
Re-run with the SSH session kept open long enough after `--stop-cmd` to `tail -f` or `cat` both log files before the
final `runpodctl stop pod` fires — e.g. insert a `cp /workspace/comfyui.log /workspace/batch_item2.log
r2:<bucket>/songs/_ab4-2026-09-23/debug/` step into `--stop-cmd` ahead of the stop, so the logs survive pod removal
regardless of how fast the failure happens.
