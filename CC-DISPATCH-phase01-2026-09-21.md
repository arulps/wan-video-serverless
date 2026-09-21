# CC-DISPATCH — wan-video-serverless Phase 0 + 1 (2026-09-21)

**Repo:** `C:\Projects\opencode\video_image` → `github.com/arulps/wan-video-serverless`
**Branch:** `main` (HEAD at dispatch time: `7e9f193`)
**Executor:** **Sonnet** (Claude Code, local). The work is fully specified and already
verified; the only decision point is an explicit stop condition. Phase 2 is Opus.
**Role of CC:** review the working-tree changes below, then commit and push. Cowork made
the edits; CC owns git.

**Scope fence — do NOT do any of these in this dispatch:**
- No RunPod API calls, no `runpodctl`, no endpoint or template changes.
- No job submissions. Nothing in this dispatch should cost a GPU-second.
- No changes to `.env`, `config/endpoint.json`, `Dockerfile`, `handler.py`,
  `app/generator.py`, `app/storage.py`, `requirements.txt`. Those are Phase 2/3.

---

## Why this dispatch exists

The endpoint has never produced a video. The review found the causes split into two
groups: **import-time bugs that kill the worker** (Phase 0) and **a deploy pipeline that
cannot be trusted to have shipped the fix** (Phase 1). Both are fixed here, and both are
verifiable without spending money.

The single most important finding: **the SDPA shim added in `6ae3fe74` did not work.**
It patched `wan.modules.attention.flash_attention`, but `wan/modules/model.py` does
`from .attention import flash_attention` at module scope and therefore holds its own
reference to the original function. Clearing `FLASH_ATTN_2_AVAILABLE` while `model.py`
still calls the original is precisely what produces the traceback in the RUNBOOK:

```
model.py:145 → attention.py:112 → assert FLASH_ATTN_2_AVAILABLE
```

So the "fix already merged" was cosmetic, and every subsequent failure was the *original*
bug, not a new one.

---

## Changes in the working tree

### 1. `app/boot.py` — make the SDPA patch actually reach the call site

- Import the whole `wan` package before patching, so every submodule that could have
  from-imported the originals is loaded.
- Capture the original `flash_attention` / `attention` function objects, then sweep every
  loaded `wan.*` module and rebind **any attribute whose value IS one of those originals**.
  Identity matching means genuine re-exports are caught and unrelated same-named
  attributes are never clobbered.
- Log the patched binding list at **INFO**, and warn loudly if nothing was found on
  `wan.modules.model`.
- `log.debug` → `log.info` for both shim messages. The template sets `LOG_LEVEL=INFO`, so
  the old DEBUG lines never appeared — meaning RUNBOOK §4 step 4 ("confirm the boot logs
  show the SDPA lines") could never have succeeded, whatever image was running.
- `report_failure`: capture `sys.exc_info()` once instead of calling `__import__("sys")`
  twice across a conditional; replace deprecated `datetime.utcnow()`.

**Verification performed (no GPU, no network):** a fake `wan` package mirroring Wan2.2's
layout — `modules/attention.py` defining both functions, `modules/model.py` doing the
from-import — was built and the real `_force_sdpa_attention()` run against it.

```
--- before patch ---
model.self_attn_forward -> FLASH
BOOT: wan attention forced to scaled_dot_product_attention; patched 3 binding(s):
      wan.modules.attention.attention, wan.modules.attention.flash_attention,
      wan.modules.model.flash_attention
--- after patch ---
model.self_attn_forward -> SDPA

--- control: what the OLD shim did ---
AssertionError from attention.py -- production traceback reproduced.
```

The control reproduces the exact production failure, which is the strongest evidence we
have that this was the blocker.

### 2. `app/models.py` — drop `local_dir_use_symlinks`

Deprecated in huggingface_hub 0.23, **removed in 1.0**. `requirements.txt` pins
`huggingface_hub>=0.24` with no ceiling, so a current build resolves to 1.x and the kwarg
raises `TypeError` on the *first job* — worker boots clean, accepts the job, dies. Since
0.23 a plain `local_dir` already writes real files, so removing it is a no-op on old
versions and a fix on new ones.

> **CC: please verify this one in the built image** — `pip show huggingface_hub` and
> `python -c "import inspect,huggingface_hub as h; print('local_dir_use_symlinks' in inspect.signature(h.snapshot_download).parameters)"`.
> It could not be checked from the review environment (package not installed there).
> If it resolves to 0.x the change is harmless either way.

### 3. `.github/workflows/deploy.yml` — add `DEPLOY.md` to the path filter

> ⚠️ **CC MUST APPLY THIS ONE BY HAND.** Files under `.github/workflows/` are protected
> from remote writes, so unlike every other change in this dispatch it is **not** in the
> working tree. Apply it before committing.

`DEPLOY.md` is the redeploy marker file, and it was not in `paths:`. So commit `7e9f193`
("ci: marker - force redeploy…") **triggered no workflow at all**. Any belief that a
redeploy happened after `6ae3fe74` is unfounded.

Add one entry to `on.push.paths`, after `".github/workflows/deploy.yml"`:

```yaml
      # DEPLOY.md is the redeploy marker file. It was NOT in this list, so every
      # "ci-redeploy-trigger" commit that touched only DEPLOY.md matched no path
      # and silently ran nothing -- while the endpoint was assumed to have been
      # rotated onto a new image. Keep it here so the marker actually works.
      - "DEPLOY.md"
```

### 4. `scripts/deploy.sh` — four fixes

| Fix | Was | Now |
|---|---|---|
| Template binding | `serverless update` never passed `--template-id`, so the endpoint kept whatever template it had | `--template-id "$TPL_ID"` on every update |
| Endpoint destruction | A substring `grep` for the GPU name against the whole endpoint JSON; on mismatch it ran `serverless delete` and recreated, **changing the endpoint id** while `.env` kept the old one | Warn only. Never delete. |
| Silent failure | `serverless create … \|\| true`, so an unsupported flag failed invisibly and surfaced as the generic FATAL | `\|\| true` removed; the real error propagates |
| Stale workers | Not handled — RUNBOOK §6 says workers keep the old image and it must be done by hand every deploy | Scale to 0, drain, scale back. `ROTATE_WORKERS=0` / `ROTATE_DRAIN_SEC` to override |

The endpoint-delete path is worth calling out on its own: it is almost certainly the
origin of the stale-endpoint-id confusion in `STATUS.md` and the 404s in RUNBOOK §6.

### 5. `scripts/inspect_now.ps1` — assign `$envl`

`$envl` was read on lines 4–5 but never assigned (the `Get-Content` line existed only in
the RUNBOOK snippet). `$key` and `$eid` were therefore empty and every call failed with
`{"code":"no_credentials"}` — which is exactly what is sitting in `./nil`. Added
`$envl = Get-Content "$root\.env"`.

---

## Checklist — verified before dispatch

- [x] `bash -n scripts/deploy.sh` clean
- [x] `python3 -m py_compile` clean on boot.py, models.py, generator.py, storage.py, config_get.py
- [x] `deploy.yml` parses; `paths` now contains `DEPLOY.md`
- [x] SDPA sweep reaches `wan.modules.model.flash_attention` (test above)
- [x] Old shim's failure reproduced as a control
- [x] Every edit diffed against its original; no unrelated lines touched
- [x] No secrets read, printed, or written; `.env` untouched
- [ ] `.github/workflows/deploy.yml` — **CC to apply by hand** (protected path, see §3)
- [ ] `huggingface_hub` version confirmed in the image — **CC to verify**

## Suggested commit

```
fix: make SDPA patch reach model.py, drop removed hf_hub kwarg, harden deploy

The 6ae3fe74 SDPA shim patched wan.modules.attention only; wan/modules/model.py
from-imports flash_attention and kept the original reference, so the
assert FLASH_ATTN_2_AVAILABLE at attention.py:112 could still fire. Sweep every
loaded wan.* module by function identity instead, and log the result at INFO so
the boot-log check in RUNBOOK 4.4 can actually pass.

Also: drop local_dir_use_symlinks (removed in huggingface_hub 1.0, unpinned here,
TypeError on first job); add DEPLOY.md to the CI path filter so marker commits
trigger a build; bind --template-id on endpoint update; stop deleting and
recreating the endpoint on a GPU substring mismatch; stop swallowing create
failures; rotate workers onto the new image after deploy; assign $envl in
inspect_now.ps1.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01UXhU23GdVCUgS8Ycjrg9qz
```

---

## Gate before any GPU spend

After CC pushes, the build will run (it touches `app/**`, `scripts/**`,
`.github/workflows/**`). Before submitting a single job:

1. Confirm the workflow actually ran and succeeded, and note the image digest.
2. Confirm the endpoint's `templateId` and the template's image match that digest —
   `runpodctl serverless get $EID --include-template -o json`.
3. Pull the image on any CPU box and run:
   ```
   python -c "import app.boot as b; b.apply_cuda_shim()"
   ```
   The INFO line must list `wan.modules.model.flash_attention` among the patched
   bindings. If it does not, stop — the fork differs and the dispatch's assumption
   needs revisiting before spending anything.
4. Only then boot a worker.

## Still open — Phase 2 and 3, NOT in this dispatch

- **Weights.** Every cold worker re-downloads ~20 GB from HF onto ephemeral container
  disk, billed at GPU rate, against a 1800 s execution timeout. Plan: RunPod host-side
  model cache (`--model-reference`) — not DC-locked, unlike a network volume. Needs
  `HF_HOME=/runpod-volume/huggingface-cache` and `models.py` moved onto the plain HF cache.
- **Output path.** `S3_BUCKET` is unset, so the handler returns the video as base64, which
  will exceed RunPod's job-output limit. There is also a dead branch that sets
  `result["video"] = None` and then fails the `"video" not in result` guard.
- **Payload keys.** RUNBOOK §4.5 sends `base_num_frames` / `num_frames` / `sample_steps` /
  `cfg_scale`; `handler.py` reads `frame_num` / `steps` / `guide_scale`. None of the four
  match, so `steps` has been silently falling back to the config default (40–50) on every
  run, not the 20 the runbook believes it is capping at.
- **GPU pinning.** `gpuId` is a single SKU (RTX 4090). TI2V-5B at 480p also runs on L4,
  A5000, L40S, A40. Pinning one SKU is itself a capacity-wait generator.
- **Container disk.** 200 GB is sized for the per-job download; drops once weights move.
