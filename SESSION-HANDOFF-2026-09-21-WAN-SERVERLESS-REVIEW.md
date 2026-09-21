# SESSION HANDOFF — Wan 2.2 serverless review + Phase 0/1 fixes (2026-09-21)

**Thread:** Cowork (Opus), linked to LAPTOP-05A4BDMR
**Repo under work:** `C:\Projects\opencode\video_image` → `github.com/arulps/wan-video-serverless`
**HEAD at handoff:** `7e9f193` · **working tree: DIRTY, nothing committed, nothing pushed**
**UPDATE 2026-09-21 ~12:00 (Fable):** Phase 0/1 is committed as `92b31d3` and deployed (CI run #14).
Phase 2 was committed and deployed ~12:30 and the cached model attached. First live job ran: sampling OK,
VAE decode OOM. Phase 2b (fix) is in the working tree — see §10; §9–§10 supersede §1–§2.
**No RunPod API calls were made. No GPU was spent.**

> This file is the local copy, kept beside `CC-DISPATCH-phase01-2026-09-21.md`.
> The same document lives in the Oviyan project at
> `claude/SESSION-HANDOFF-2026-09-21-WAN-SERVERLESS-REVIEW.md` and, from 2026-09-21, in the
> "Video serverles( Wan 2.2)" project under the same name.
> If you edit one, mirror the other.

---

## 1 · Where this stands in one paragraph

The endpoint has never produced a video. A full read of the repo (23 files + git history)
found the cause split in two: import-time bugs that kill the worker, and a deploy pipeline
that cannot be trusted to have shipped any fix. Both are now fixed in the working tree and
verified without spending money. The headline: **the SDPA fix in `6ae3fe74` never worked** —
it patched the wrong namespace, so every failure since has been the *original* flash-attn
bug, not a new one. Claude Code has a dispatch waiting to review, apply one protected-path
change by hand, commit and push.

## 2 · Next action

Run **`CC-DISPATCH-phase01-2026-09-21.md`** (repo root) in Claude Code on the laptop.
**Executor: Sonnet** — the work is fully specified, verified, and fenced away from any
RunPod call. Opus is for Phase 2.

The dispatch's own gate must be cleared before any job is submitted:
1. Confirm the workflow actually ran; note the image digest.
2. Confirm endpoint `templateId` → template image → that digest all agree.
3. On any CPU box: `python -c "import app.boot as b; b.apply_cuda_shim()"` — the INFO line
   must list `wan.modules.model.flash_attention` among the patched bindings.
4. Only then boot a worker.

## 3 · Findings, ranked by likelihood of being the blocker

| # | Finding | Status |
|---|---|---|
| 1 | `7e9f193` ("ci: marker - force redeploy") **triggered no workflow** — `DEPLOY.md` is not in the workflow's `paths:` filter. Every believed redeploy since was fiction. | verified · fixed in dispatch §3 |
| 2 | `deploy.sh`'s update path never passed `--template-id`, so the endpoint was never re-bound to the freshly upserted template. | verified · fixed |
| 3 | **The SDPA shim patched the wrong namespace.** `boot.py` rebound `wan.modules.attention.flash_attention`, but `wan/modules/model.py` from-imports it and keeps its own reference. Clearing the availability flag while `model.py` still calls the original is exactly what produces `model.py → attention.py:112 assert FLASH_ATTN_2_AVAILABLE`. | verified by test · fixed |
| 4 | `local_dir_use_symlinks` was removed in huggingface_hub 1.0; `requirements.txt` says `>=0.24` with no ceiling, so a current build gets 1.x and raises `TypeError` on the first job — boots clean, accepts the job, dies. | **unverified** (package absent from review env) · kwarg removed anyway |
| 5 | Every cold worker re-downloads ~20 GB from HF onto ephemeral container disk, GPU-billed, against a 1800 s execution timeout. `BAKE_TI2V` defaults to 0. This is the ~$10-for-zero-videos mechanism. | verified · Phase 2 |
| 6 | RUNBOOK §4.5 sends `base_num_frames`/`num_frames`/`sample_steps`/`cfg_scale`; `handler.py` reads `frame_num`/`steps`/`guide_scale`. **None match**, so steps silently fell back to the config default (40–50), not the 20 the runbook thinks it is capping at. | verified · Phase 3 |
| 7 | `S3_BUCKET` unset → handler returns video as base64, which exceeds RunPod's job-output limit. Dead branch also sets `result["video"] = None` then fails the `"video" not in result` guard. | verified · Phase 3 |
| 8 | `deploy.sh` did a substring `grep` for the GPU name against the whole endpoint JSON and, on mismatch, **deleted and recreated the endpoint** — new id, stale `.env`. Almost certainly the origin of the endpoint-id confusion in STATUS.md and the 404s in RUNBOOK §6. | verified · fixed |
| 9 | `inspect_now.ps1` reads `$envl` but never assigns it → empty key/id → the `no_credentials` error sitting in `./nil`. | verified · fixed |
| 10 | Both shim log lines were `log.debug` while the template sets `LOG_LEVEL=INFO`. **RUNBOOK §4 step 4 ("confirm the SDPA lines in the boot logs") could never have passed on any image.** | verified · fixed |

## 4 · The verification that matters

A fake `wan` package mirroring Wan2.2's layout (`modules/attention.py` defining both
functions, `modules/model.py` doing the from-import) was built and the real
`_force_sdpa_attention()` run against it:

```
--- before patch ---
model.self_attn_forward -> FLASH
BOOT: ... patched 3 binding(s): wan.modules.attention.attention,
      wan.modules.attention.flash_attention, wan.modules.model.flash_attention
--- after patch ---
model.self_attn_forward -> SDPA

--- control: what the OLD shim did ---
AssertionError from attention.py -- production traceback reproduced.
```

The control reproduces the production failure exactly. Treat this as the strongest
evidence available that finding #3 was the blocker.

## 5 · Working tree — what is changed and uncommitted

| file | change |
|---|---|
| `app/boot.py` | identity-based sweep over all loaded `wan.*` modules; INFO logging with the patched-binding list; `report_failure` exc_info fixed; `utcnow()` → timezone-aware |
| `app/models.py` | dropped `local_dir_use_symlinks` |
| `scripts/deploy.sh` | `--template-id` on update; delete-and-recreate removed → warning only; `\|\| true` removed from create; worker rotation (scale 0 → drain → restore) added, `ROTATE_WORKERS=0` to skip |
| `scripts/inspect_now.ps1` | `$envl = Get-Content "$root\.env"` added |
| `CC-DISPATCH-phase01-2026-09-21.md` | new |
| `SESSION-HANDOFF-2026-09-21-WAN-SERVERLESS-REVIEW.md` | new (this file) |

**NOT applied — CC must do this by hand:** `.github/workflows/deploy.yml` is a protected
path for remote writes. The one-line addition (`- "DEPLOY.md"` under `on.push.paths`) is in
dispatch §3 with the exact YAML. Without it, marker commits keep triggering nothing.

Checks run: `bash -n` clean, `py_compile` clean on all touched Python, workflow YAML parses,
every edit diffed against its original, `.env` never read or written.

## 6 · Decisions taken this session

- **Goal is unlimited clips at no marginal cost** — removing the credit ceiling, not saving
  per clip. Per-clip the gap is small (~$0.11 self-hosted vs $0.25–0.50 hosted); the value
  is that a 200-clip burst becomes GPU-seconds instead of impossible.
- **No RunPod network volume.** RunPod's own docs warn a single volume constrains workers to
  that volume's datacenter. Same trap as the EU-CZ-1 pod.
- **Phase 2 route is RunPod host-side model cache (`--model-reference`)** — host-distributed,
  explicitly not DC-locked, no billing for download time, needs runpodctl ≥2.4.0 (deploy.sh
  already pulls 2.14.0). Fallbacks if it won't take a 20 GB diffusion repo: multi-DC volumes
  (now supported, no auto-sync), or baking the image (blocked by ~14 GB free disk on
  `ubuntu-latest` — needs a disk-reclaim step).
- **Model split for future dispatches:** Phase 0/1 → Sonnet. Phase 2 → Opus (real unknowns,
  money at stake). Phase 3 → Sonnet for wiring, Opus for the first live job.

## 7 · Open — Phase 2 and 3, not started

- **Weights.** Wire model cache; `HF_HOME=/runpod-volume/huggingface-cache`; move
  `models.py` onto the plain HF cache (this also permanently settles finding #4); drop
  `containerDiskGb` from 200.
- **Output.** Configure S3/R2; fix the `video: None` dead branch; `MAX_B64_MB=90` is far
  above RunPod's real output limit.
- **Payload keys.** Align RUNBOOK §4.5 with what `handler.py` actually reads.
- **GPU pinning.** `gpuId` is a single SKU (RTX 4090). TI2V-5B at 480p also runs on L4,
  A5000, L40S, A40 — pinning one SKU is itself a capacity-wait generator.
- **Quality caveat to carry:** self-hosting gets **Wan 2.2 TI2V-5B**, the small consumer
  model, while the hosted service runs **3.0**. Suggested shape: self-host the ambience/
  B-roll shots (the lullaby was 5 of 7 clips with no characters), keep identity-critical
  hero shots on 3.0 until a stronger self-hosted model is viable.

## 8 · Also settled earlier in this session (MinMini production side)

- **Wan hosted pricing, measured live in-product:** billing is linear per second —
  480p = 2 credits/s, 720p = 3 credits/s. 1080p is members-only. Free tier output is
  watermarked, so it is unusable for the channel regardless of credits. Pro (300/mo) ≈ 1.3
  songs; Premium (1200/mo) ≈ 5 songs.
- **Cadence recommendation:** one song/week, fixed day, two finished videos banked. Not a
  volume problem — the bottleneck is edit hours.
- **YouTube reality check:** MinMini videos are "made for kids", so autoplay-on-home, the
  notification bell, comments, playlists and end screens are all **disabled**. Uploading more
  does not compound. The levers that do work: thumbnail/metadata trust signals, YouTube Kids
  app approval, a 24/7 live stream of the sleep loops, and multi-language audio tracks (which
  would also collapse the two-channel double-upload — cheapest to decide now, at 4 videos).
- **Still pending from before:** Mazhai edit (13-entry timeline), lullaby loop (trim `02_A2`
  to its last ~2.5 s, build the 130 s cycle), Rainbow finished but unpublished.

---

## 9 · Fable session 2026-09-21 (11:00–12:00) — review of `92b31d3`, Phase 2 written, first-video runner

**Thread:** Cowork (Fable 5.1), linked to LAPTOP-05A4BDMR, folder `C:\Projects\opencode\video_image`.
**No RunPod API calls were made. No GPU was spent.** Everything was verified offline.

### 9.1 Gate from §2 — cleared

| gate step | result |
|---|---|
| 1. workflow ran | CI run #14 for `92b31d3`, **success** (build 2m52s, deploy 43s) |
| 2. template/endpoint agree | template `25514mi5ae` → `ghcr.io/arulps/wan-video-serverless:92b31d3…`; endpoint `wv9oneserd7vj6` → `templateId 25514mi5ae`; rotate step ran; final `workersMin 0 / workersMax 3` |
| 3. boot check in the image | replaced by the `selftest` job (below) — proves the patch on the *actual worker* before any weights load, for the price of a boot |
| hf_hub version | PyPI today: 1.32.0, kwarg removed (finding #4 confirmed real). But Wan pins `transformers<=4.51.3` → `huggingface-hub<1.0`, so the image most likely has 0.3x. Either way harmless now; the boot log prints the version. |

### 9.2 New finding — the SDPA shim was numerically wrong (both versions)

Wan's `flash_attention` takes `[B, L, heads, D]`; torch SDPA takes `[B, heads, L, D]`. Neither the
`6ae3fe74` shim nor the `92b31d3` one transposed. Consequence on a real run: self-attention attends
across heads (noise video, job "succeeds"); cross-attention (`Lq≠Lk`) raises a shape error after
the ~11-min download+load. **The first sample job today would have failed or produced noise.**
Fixed in `app/boot.py::make_sdpa_flash_attention` (mirrors upstream's `attention()` fallback:
transpose in/out, q_scale, softmax_scale, k_lens mask, both kwarg spellings). Verified:
`tests/test_sdpa_numeric.py` (4e-7 fp32 / 5e-3 bf16 vs reference; old shim shown to crash and
to be off by 2.35) and `tests/test_sweep_fake_wan.py` (real sweep against a fake package that
mirrors upstream's import graph, end-to-end through `model.py`'s binding).

Also confirmed from upstream `main` (`1ea34ff4`, what the Dockerfile clones): `WanModel.forward`
sets `context_lens = None` and self-attention passes `k_lens = seq_lens` (== L at batch 1), so
the SDPA path with the mask is *exactly* flash semantics for our batch-1 jobs.

### 9.3 Phase 2 written (working tree, uncommitted) — `CC-DISPATCH-phase2-2026-09-21.md`

- `app/boot.py` corrected shim + `SHIM_REPORT` + hf_hub version log
- `app/models.py` RunPod cached-model resolution (`/runpod-volume/huggingface-cache/hub/models--Wan-AI--Wan2.2-TI2V-5B/snapshots/<hash>/`), validated; fallback to billed download unchanged
- `app/generator.py` effective params + timings returned; size validated per task; `n_prompt` passed; `save_video` output verified
- `app/storage.py` S3-compatible (R2), `compact_mp4()`
- `handler.py` `op=selftest`; refuses jobs when the patch didn't reach `wan.modules.model`; key aliases; seed reported; output sized against RunPod's 10 MB `/run` cap; dead `video=None` branch removed
- `scripts/first_video.ps1` bounded selftest → one job → save → drain; never resubmits
- `tests/` four offline test files, all passing; `RUNBOOK.md` §4.5 keys fixed + §9; `.dockerignore`

### 9.4 Decisions / facts verified today (docs.runpod.io, 2026-09-21)

- **Cached models** (the Phase-2 weights route): host-side, unbilled download, mounted at
  `/runpod-volume/huggingface-cache/hub/` in HF layout, one model per endpoint, public/gated/private
  HF repos; custom workers resolve the path themselves. `runpodctl serverless update --model-reference`
  exists (v2.14.0 release notes). Not DC-locked like a network volume. Repo size is **~34 GB**, not 20.
- **Output caps:** `/run` 10 MB, `/runsync` 20 MB. `MAX_B64_MB=90` was never going to work.
- **GPU list:** REST `gpuTypeIds` is a priority list; runpodctl takes comma-separated ids. Deferred to Phase 3.
- **Template update triggers a rolling release** of endpoint workers (Templates API doc); the
  FlashBoot-serves-stale-image claim in RUNBOOK §8 is unverified and was not the cause of the 10:01 failure.

### 9.5 Next action

Run `CC-DISPATCH-phase2-2026-09-21.md`: Part A commit/push/watch CI (no cost) → attach the cached
model via `runpodctl serverless update <eid> --model-reference https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B:main` → Part B `scripts\first_video.ps1` (≈$0.30 worst case, one run).
Report the selftest JSON, the job meta JSON, and the mp4.

### 9.6 Open after the first video (Phase 3)

Object storage (S3/R2) in the template env; `--model-reference` in `deploy.sh`; GPU priority list;
container disk down from 200 GB; production step/frame defaults from measured `t_sample_s`;
executionTimeout review for 121f/50-step jobs.

---

## 10 · Fable session 2026-09-21 (12:00–13:15) — first live run, VAE-decode OOM, Phase 2b

**Money spent:** selftest + one job ≈ $0.10. **No resubmits.**

### 10.1 What the run proved (all previously open)
- Cached model works: `/runpod-volume/huggingface-cache/hub/models--Wan-AI--Wan2.2-TI2V-5B/snapshots/921dbaf3…`, 30 s, unbilled.
- The corrected SDPA shim is right in practice: 20/20 steps at 1280×704×81f in ≈5.5 min on a 4090, no errors.
- `huggingface_hub` in the image is 0.36.2 (kwarg present) — Phase-1 item closed.
- Selftest gate works as designed (patched bindings incl. `wan.modules.model.flash_attention`, `wan.modules.flash_attention`, `wan.distributed.ulysses.flash_attention`).

### 10.2 Failure and diagnosis
`vae.decode` → `vae2_2.py:40 F.pad` OOM: 2.60 GiB requested, 18.35 GiB allocated, 4.17 GiB reserved-but-unallocated,
509 MiB free. Upstream already offloads the DiT before decode; the tenant is the fp32 decoder (160 channels at full
704p → ~2.6 GiB per 4-frame activation) plus `torch.cat`-per-latent-frame output growth that fragments the allocator.

### 10.3 Phase 2b (working tree) — `CC-DISPATCH-phase2b-2026-09-21.md`
- `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` in `Dockerfile` (last layer) and `config/endpoint.json` template env.
- `app/generator.py::_install_decode_guard` — cache clear before decode; on OOM retry in bf16 with latents in hand.
- selftest reports `alloc_conf`; `first_video.ps1` refuses the real job if it is unset; result carries `vae_decode_dtype`/`vae_decode_retried`.
- `tests/test_decode_guard.py` added; all five test files pass.

### 10.4 Next action
CC: run Phase 2b Part A (commit/push/CI), confirm the cached-model reference survived the deploy, then Part B (one run).
Report `vae_decode_retried` — it decides whether bf16 decode becomes the default.

### 10.5 If it fails again at decode (do not loop)
bf16 decode by default → 48 GB GPU first in `gpuTypeIds` (L40S) → tiled VAE decode.
