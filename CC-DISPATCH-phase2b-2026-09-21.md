# CC-DISPATCH — wan-video-serverless Phase 2b: VAE-decode OOM fix + second bounded run (2026-09-21)

**Repo:** `C:\Projects\opencode\video_image` → `github.com/arulps/wan-video-serverless`
**Branch:** `main` (HEAD = the Phase-2 commit you pushed at ~12:30; CI green; cached model attached)
**Executor:** Claude Code on the laptop. Part A commit/push/watch CI (no cost). Part B = ONE run of
`scripts\first_video.ps1` (≈$0.10–0.15; weights are cached now).
**Prepared by:** Fable, from CC's failure report of job `caf3f7b9-…-u2`.

---

## 0 · What happened and why (diagnosis, so nobody re-derives it)

Job `caf3f7b9`: weights from the RunPod cache in 30 s, pipeline loaded, **all 20 sampling steps
completed through the corrected SDPA shim** (≈5.5 min), then `vae.decode` → `vae2_2.py:40 F.pad`
raised `torch.OutOfMemoryError: Tried to allocate 2.60 GiB … 509 MiB free; 18.35 GiB allocated;
4.17 GiB reserved but unallocated`.

Read against upstream `wan/modules/vae2_2.py` (main `1ea34ff4`, the ref the image clones):

- Upstream already moves the DiT to CPU and calls `empty_cache()` before decode, so the 18 GiB is
  the **decoder itself**: it runs in fp32 (`Wan2_2_VAE(dtype=torch.float)`), its finest level has
  **160 channels at full 1280×704**, so a single 4-frame activation is 160×704×1280×4×4 B ≈ 2.3–2.6 GiB —
  exactly the failed allocation — and several are live at once inside a residual block.
- `decode()` accumulates its output with `out = torch.cat([out, out_], 2)` on **every latent
  frame** (21 times for 81 frames): 21 allocations of steadily growing size. The caching
  allocator cannot reuse the freed smaller block for the next bigger one → "reserved but
  unallocated" grows (4.17 GiB) while a 2.6 GiB contiguous request fails. That is the pattern
  `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` was built for.
- So: not the DiT, not T5, not a leak — fp32 decode at 704p on a 24 GB card is at the edge, and
  fragmentation pushed it over. The other options from the report (freeing T5/DiT, offload) are
  already in effect upstream; a 48 GB GPU would also work but costs ~2× per second and isn't
  needed.

## 1 · The fix (two independent layers; either alone should suffice)

| file | change |
|---|---|
| `Dockerfile` | `ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (last layer before `CMD`, so the build cache above it is untouched) |
| `config/endpoint.json` | same variable in `template.env` — the template carries it even if a stale image is ever bound |
| `app/generator.py` | `_install_decode_guard(pipe)`: wraps `pipe.vae.decode`; runs `gc.collect()` + `empty_cache()` before decode; on `torch.cuda.OutOfMemoryError` clears the VAE's feature cache, converts the VAE to **bfloat16** and decodes again — **the sampled latents are still in hand inside the wrapper, so the retry costs seconds, not a resample**. Upstream `vae2_2.py` line 66 already carries a bf16 compatibility fix for its upsampler, so bf16 decode is an anticipated mode. Result carries `vae_decode_dtype`, `vae_decode_retried`, `alloc_conf`. |
| `handler.py` | selftest reports `alloc_conf` |
| `scripts/first_video.ps1` | **stops before the real job** if the selftest shows the worker is running without `expandable_segments:True` (i.e. the new image/template isn't live); prints `vae_decode`/`retried` on success |
| `tests/test_decode_guard.py` | new — OOM once → bf16 retry with latents intact; no-OOM path; non-OOM errors not swallowed; idempotent wrap |
| `RUNBOOK.md` §9, `SESSION-HANDOFF-…` §10 | state + diagnosis |

All five test files pass offline; `py_compile` clean.

Expected on the next run: decode succeeds in fp32 with expandable segments (`vae_decode_retried=false`).
If it still OOMs, the guard's bf16 retry should carry it (`vae_decode_retried=true`) — report that
value either way; it decides whether bf16 decode becomes the default.

## 2 · Part A — review, commit, push, watch CI (no RunPod calls)

```
git status
git diff app/generator.py     # the guard; confirm the retry converts vae.model + vae.dtype to bfloat16
git diff Dockerfile config/endpoint.json scripts/first_video.ps1 handler.py
powershell -NoProfile -Command "[void][scriptblock]::Create((Get-Content -Raw scripts/first_video.ps1)); 'ps1 parses'"
git add Dockerfile config/endpoint.json app/generator.py handler.py scripts/first_video.ps1 tests/test_decode_guard.py RUNBOOK.md CC-DISPATCH-phase2b-2026-09-21.md SESSION-HANDOFF-2026-09-21-WAN-SERVERLESS-REVIEW.md
```
Commit (message in §4), push, `gh run watch`. In the deploy log confirm:
- template `25514mi5ae` → `imageName …:<new sha>` and its `env` now contains `PYTORCH_CUDA_ALLOC_CONF`
- endpoint `wv9oneserd7vj6` → `templateId 25514mi5ae`, workers restored `0 / 3`
- **`runpodctl serverless get wv9oneserd7vj6 -o json` still shows the cached model reference**
  (`deploy.sh` ran `serverless update` without `--model-reference`; if it was cleared, re-attach with
  the §3 command from the phase2 dispatch before Part B — the selftest's
  `weights.runpod_cached_snapshot` is the final word).

## 3 · Part B — ONE bounded run

```
cd C:\Projects\opencode\video_image
powershell -ExecutionPolicy Bypass -File scripts\first_video.ps1
```
Same parameters as before (ti2v-5B, 1280*704, 81 f, 20 steps, seed 30313) so the run is
comparable. The script now refuses to submit the real job if the selftest's `alloc_conf` is not
`expandable_segments:True`.

Report: selftest JSON (`alloc_conf`, `runpod_cached_snapshot`), the job meta JSON (especially
`vae_decode_dtype`, `vae_decode_retried`, `t_sample_s`, `t_total_s`, `video_bytes`), the mp4 path,
final `/health`. On FAILED: the error text, then stop.

## 4 · Suggested commit

```
fix: survive Wan2.2 VAE decode OOM on 24 GB (expandable segments + bf16 retry)

Job caf3f7b9 sampled all 20 steps at 1280x704x81f on an RTX 4090 and then
died in vae.decode allocating 2.60 GiB with 4.17 GiB reserved-but-unallocated.
Upstream's decoder runs in fp32 with 160 channels at full resolution and grows
its output with torch.cat per latent frame, which fragments the caching
allocator. Set PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True in the image
and the template env, and wrap vae.decode so an OOM clears the cache and
retries in bfloat16 with the latents still in hand instead of failing the job.
Selftest reports alloc_conf; first_video.ps1 refuses to spend if it is unset.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01K74qgLLkw1m2TCrreoB84E
```

## 5 · If this run also fails at decode

Do not loop. The next levers, in order, are decided in Cowork from the reported numbers:
1. make bf16 decode the default (skip the fp32 attempt) — zero cost;
2. 48 GB GPU first in the priority list (L40S; ≈2× $/s, similar speed) — a `gpuTypeIds` change;
3. a spatially tiled decode for the Wan VAE (ComfyUI does this; non-trivial for a causal 3D VAE).
