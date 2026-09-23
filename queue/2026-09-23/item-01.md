# item-01 — VACE with SEPARATE reference images (custom node), T17 + T07 at 480p

**Why:** the two-child failures (T17/T18/T20) used ONE sheet with both children. Core ComfyUI `WanVaceToVideo` uses only
`reference_image[:1]` (verified in `comfy_extras/nodes_wan.py`), so a batch of tiles never worked natively. Fable wrote
`comfy/custom_nodes/wan_vace_multiref.py` (`WanVaceToVideoMultiRef`: every image of the batch encoded on its own and
prepended as its own latent frame — what the original VACE `src_ref_images` and Phantom do). Tested against the real
ComfyUI code on CPU with a fake VAE: single-ref output is byte-identical to the core node; two refs give two separate
reference latents, `trim_latent=2`. The runner now takes `ref` = `a.png|b.png` and an `engine` column.
**Budget for this item: ≤ 30 min pod time (~$1.75 on an H100). `--max-minutes 30`.**

## What is on disk (Fable; nothing committed — commit is NOT part of this queue)
| file | change |
|---|---|
| `comfy/custom_nodes/wan_vace_multiref.py` | **new** custom node |
| `comfy/run_comfy.py` | `build_workflow` takes one ref name or a LIST (ImageBatch chain, node ids 20+; node 9 switched to `WanVaceToVideoMultiRef` for >1 refs on VACE; Phantom's `images` input handled); CLI `--ref` repeatable |
| `comfy/batch_runner.py` | `ref` cell split on `|`; new `engine` column (`vace` default / `phantom`); per-engine base workflow; sidecar records `refs` + `engine`; dry-run prints `N SEPARATE references` |
| `comfy/phantom_s2v_api.json` | **new** (item 2) |
| `scripts/pod_bootstrap.sh` | `pull` copies `wan/comfy/custom_nodes/*.py` into `<ComfyUI>/custom_nodes/` before starting ComfyUI, then checks `/object_info` for `WanVaceToVideoMultiRef`, `WanPhantomSubjectToVideo`, `ImageBatch` (`node OK` / `node MISSING`); new `model-get` / `model-push` (item 2) |
| `songs/twinkle-twinkle/refs/mintu-front-16x9.png`, `minnu-body-16x9.png` | **new** single-tile sheets (built, looked at: clean, no halo); added to `scripts/build_song_refs.py` |
| `songs/_ab4-2026-09-23/` | **new** A/B folder: 6 rows, see its README; this item runs the three `*_vsep*` rows |

## Steps
1. **Laptop, no GPU.** From the repo root:
   ```
   python comfy\batch_runner.py --song songs\_ab4-2026-09-23 --hosts http://x --dry-run
   python comfy\batch_runner.py --song songs\twinkle-twinkle --hosts http://x --dry-run
   python -m py_compile comfy\custom_nodes\wan_vace_multiref.py comfy\run_comfy.py comfy\batch_runner.py
   ```
   Expect: `_ab4` = 6 rows, every one `2 SEPARATE references`, no `REF MISSING`, no `OVER BUDGET` (~469–471 tokens);
   twinkle = 4 pending, unchanged from 4k. Anything else → `item-01.blocked` with the output.
2. `bash scripts/pod_bootstrap.sh wan-push` from the laptop (R2 env from `.env` as in 4e–4k; never echo values). This
   ships `comfy/custom_nodes/`, the two new sheets and `songs/_ab4-2026-09-23/`.
3. **Fresh pod**: ComfyUI template, **H100 80 GB** (A100 80 GB if no H100 anywhere), 100 GB container disk, the four
   R2 env vars set in the console as before, copy `scripts/pod_bootstrap.sh` in, `bash pod_bootstrap.sh pull`.
   Log the pod id + GPU + hourly rate in `LOG.md`. `pull` must end with `BOOT-TO-READY` **and** three `node OK` lines.
   If `node MISSING WanVaceToVideoMultiRef`: `grep -n -B2 -A12 "wan_vace_multiref" /workspace/comfyui.log` into the
   report, stop the pod, `item-01.blocked`. Do not edit the node.
4. On the pod, cheap row first:
   ```
   cd /workspace/wan
   python comfy/batch_runner.py --song songs/_ab4-2026-09-23 --hosts http://127.0.0.1:8188 --only T17_vsep_d,T17_vsep,T07_vsep --dry-run
   python comfy/batch_runner.py --song songs/_ab4-2026-09-23 --hosts http://127.0.0.1:8188 --seed 30313 --only T17_vsep_d,T17_vsep,T07_vsep \
       --max-minutes 30 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/_ab4-2026-09-23; runpodctl stop pod $RUNPOD_POD_ID"
   ```
   Expect ~1 min (distilled) + 2 × ~6–8 min (full, 480p on H100). If the FIRST row fails with `EXECUTION ERROR` naming
   `WanVaceToVideoMultiRef`, copy the error + the matching traceback from `/workspace/comfyui.log` into the report,
   confirm the pod stopped, `item-01.blocked`. No retries, no other seeds.
5. Confirm the pod is **stopped** (`runpodctl get pod <id>`), then `runpodctl remove pod <id>` (container disk only;
   nothing to keep — outputs are in R2). Pull outputs to the laptop:
   `rclone copy r2:<bucket>/songs/_ab4-2026-09-23/out/ songs\_ab4-2026-09-23\out\`. Leave the three rows' `status`
   as `done` (item 2 runs the other three rows with `--only`). The pod's `shots.csv` is also in R2 next to `out/` — do
   not copy it over the laptop's; edit cells only if ever needed.
6. Write `queue\2026-09-23\item-01.report.md`:
   - table: row · status · wall s · **full Windows path** of the mp4, the `_qc\<row>-strip.png` and the `.json`;
   - pod id, GPU, DC, minutes from create to stop, $ (minutes × rate), running total for the queue;
   - the `pull` lines `BOOT-TO-READY` and the three `node OK/MISSING` lines, verbatim;
   - `grep -c "WanVaceToVideoMultiRef" /workspace/comfyui.log` result (captured before stop) and any `Error`/`Traceback` lines;
   - stop-cmd exit code line from the runner.
   Then create `item-01.done` and wait for `item-01.verdict`.
