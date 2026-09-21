# CC-DISPATCH — wan-video-serverless Phase 2 + first sample video (2026-09-21)

**Repo:** `C:\Projects\opencode\video_image` → `github.com/arulps/wan-video-serverless`
**Branch:** `main` (HEAD at dispatch time: `92b31d3`, pushed; CI run #14 green)
**Executor:** Claude Code on the laptop. Part A (review + commit + push) is mechanical — any
model. Part B submits real GPU jobs — read it fully before running; it is one bounded script.
**Role of CC:** review the working-tree changes, commit, push, watch CI, attach the cached model
to the endpoint (§3, one `runpodctl serverless update`), then run the bounded first-video script
and report. Cowork (Fable) made and verified the edits; CC owns git and the
laptop-side run.

**Prepared by:** Fable review session 2026-09-21. Everything below was verified offline in a
CPU container against a copy of the repo and the current Wan2.2 `main`
(`1ea34ff4`, the same ref the Dockerfile clones).

---

## 0 · Why this dispatch exists (read this even if you skip the rest)

Phase 0/1 (`92b31d3`) fixed the *reach* of the SDPA patch. Reviewing the patched function
itself against upstream `wan/modules/attention.py` found that **it was numerically wrong in
both the old and the new version**:

- Wan calls `flash_attention(q, k, v, ...)` with tensors shaped `[B, L, heads, D]`.
- `torch.nn.functional.scaled_dot_product_attention` expects `[B, heads, L, D]`.
- The shim passed them straight through. For self-attention that computes attention *across
  the 24 heads inside each token* instead of across tokens — no crash, a noise video, a full
  GPU job wasted. For cross-attention (`Lq` = video tokens ≠ `Lk` = 512 text tokens) it raises
  `RuntimeError: The size of tensor a must match the size of tensor b` — job FAILED after the
  ~11-minute download + load.
- Upstream's own non-flash fallback (`attention()`) does `q.transpose(1, 2)` in and
  `out.transpose(1, 2)` back out. The new shim does exactly that, plus `q_scale`,
  `softmax_scale` and a `k_lens` key-padding mask, and accepts both `version=` (flash_attention's
  kwarg) and `fa_version=` (attention()'s kwarg).

`tests/test_sdpa_numeric.py` checks the new function against an explicit per-head softmax
reference (max abs err 4e-7 in fp32, 5e-3 in bf16, masks included) and demonstrates the old
shim's crash / 2.35 max abs error. `tests/test_sweep_fake_wan.py` runs the real
`_force_sdpa_attention()` against a fake `wan` package that mirrors upstream's import graph
(`modules/__init__` re-export, `model.py` from-import, `distributed/ulysses.py`,
`sequence_parallel` alias import, and a module imported only *after* the sweep) and then calls
the model's attention end to end.

Without this fix, the first job today would have burned ~$0.30 and 20 minutes for nothing.

---

## 1 · Changes in the working tree (all written by Cowork; nothing committed)

| file | change |
|---|---|
| `app/boot.py` | `make_sdpa_flash_attention()` — correct SDPA replacement (transposes, q_scale, softmax_scale, k_lens mask, both kwarg spellings, `window_size≠(-1,-1)` raises instead of silently ignoring). `SHIM_REPORT` dict (patched bindings, `model_binding_patched`) for the selftest. `_log_hf_hub()` prints the `huggingface_hub` version + whether `local_dir_use_symlinks` exists, at INFO — closes the open Phase-1 question from the boot log. `report_failure` uploads via `storage._s3()` (R2-aware). |
| `app/models.py` | **RunPod cached-model resolution**: looks for `/runpod-volume/huggingface-cache/hub/models--Wan-AI--Wan2.2-TI2V-5B/snapshots/<hash>/` first (RunPod docs: custom workers must resolve this path themselves), validates it holds the T5 + VAE checkpoints, then an existing local copy, then downloads to `/models/<task>` (billed) with a loud warning. `weights_status()` for the selftest. Download result is validated instead of trusted. |
| `app/generator.py` | returns `(mp4_path, info)` with the *effective* parameters (steps/shift/guide_scale after defaults, fps, seed, checkpoint dir, timings); validates `size` against `SUPPORTED_SIZES[task]` (ti2v-5B: `1280*704` / `704*1280` only); passes `n_prompt` to ti2v/i2v (was dropped); checks `save_video` actually produced a file (upstream swallows exceptions and logs at INFO); progress callbacks. |
| `app/storage.py` | S3-compatible: `S3_ENDPOINT_URL` (Cloudflare R2), `S3_PUBLIC_BASE_URL`, `S3_PRESIGN_SECONDS`, `ContentType=video/mp4`. `compact_mp4()` — ffmpeg libx264 crf 23 yuv420p faststart. |
| `handler.py` | `op: "selftest"` (no weights loaded; returns shim report, GPU/VRAM, hf_hub version, weights location, disk, ffmpeg, output config). Refuses real jobs if `model_binding_patched` is false. Key aliases (`num_frames`/`base_num_frames`/`sample_steps`/`cfg_scale`/`sample_shift`/`negative_prompt`/`sample_solver`/`resolution`/…). Seed drawn when `-1` and reported. Output: S3 URL if configured, else compact re-encode + base64 **only if ≤ `MAX_OUTPUT_MB` (9; RunPod `/run` cap is 10 MB)**, else an explicit error — the `result["video"] = None` dead branch is gone. Temp files always cleaned. |
| `scripts/first_video.ps1` | **new** — the bounded run (Part B). |
| `tests/test_sdpa_numeric.py`, `tests/test_sweep_fake_wan.py`, `tests/test_handler.py`, `tests/test_models.py` | **new** — all pass offline (torch CPU). Not run in CI; documented so the next session can re-run them. |
| `RUNBOOK.md` | §4.5 payload keys corrected; new §9 (today's state, cost model, output path). |
| `.dockerignore` | `+tests`, `+outputs` |
| `CC-DISPATCH-phase2-2026-09-21.md`, `SESSION-HANDOFF-2026-09-21-WAN-SERVERLESS-REVIEW.md` | this file; handoff updated (§9 appended) |

**Not changed:** `Dockerfile`, `requirements.txt`, `config/endpoint.json`, `.github/workflows/deploy.yml`,
`.env`, `client/generate.py`. The image contents change only through `app/**` and `handler.py`, which
the workflow's `paths:` filter already covers.

**Checks Cowork ran:** `py_compile` clean on every touched `.py`; four test files pass; every
edit was written against the file as read from the laptop at 10:57 (mtimes recorded).

---

## 2 · Part A — review, commit, push, watch CI  (no RunPod calls, no cost)

1. `git status` — expect exactly the files in §1 modified/untracked (plus the pre-existing
   untracked `logs.txt`, `nil`, `STATUS.md`, `CC-DISPATCH-phase01-2026-09-21.md`,
   `SESSION-HANDOFF-…`). Leave `logs.txt` and `nil` untracked as before.
2. `git diff app/boot.py` — the important hunk is `make_sdpa_flash_attention`. Confirm the two
   `transpose(1, 2)` calls bracket the SDPA call. That is the whole point of this dispatch.
3. Parse-check the PowerShell script (no Python needed):
   `powershell -NoProfile -Command "[void][scriptblock]::Create((Get-Content -Raw scripts/first_video.ps1)); 'ps1 parses'"`
4. Stage specific files (never `git add .`):
   ```
   git add app/boot.py app/models.py app/generator.py app/storage.py handler.py .dockerignore RUNBOOK.md scripts/first_video.ps1 tests/test_sdpa_numeric.py tests/test_sweep_fake_wan.py tests/test_handler.py tests/test_models.py CC-DISPATCH-phase2-2026-09-21.md SESSION-HANDOFF-2026-09-21-WAN-SERVERLESS-REVIEW.md CC-DISPATCH-phase01-2026-09-21.md
   ```
   (the phase01 dispatch is committed now for the record; it is what `92b31d3` implemented.)
5. Commit with the message in §5. Push `main`.
6. `gh run watch` (or `gh run list --workflow build-deploy --limit 1` → `gh run view <id> --log`).
   Both jobs must succeed. In the deploy log note:
   - `"imageName": "ghcr.io/arulps/wan-video-serverless:<new sha>"` on template `25514mi5ae`
   - `"templateId": "25514mi5ae"` on endpoint `wv9oneserd7vj6`
   - the rotate step ending with `"workersMax": 3, "workersMin": 0`
   If any of those differ, stop and report — do not run Part B.

---

## 3 · Before Part B — attach the cached model (CC, via runpodctl; this is the ONE RunPod write in this dispatch)

RunPod "cached models" pre-stage a Hugging Face repo on the host, **unbilled**, mounted at
`/runpod-volume/huggingface-cache/hub/…` (docs: docs.runpod.io/serverless/endpoints/model-caching).
`models.py` now looks there first. Without it every cold worker downloads ~34 GB at GPU rates
(~$0.15–0.25 per cold start, 5–10 min). Attaching it costs nothing and changes no other
endpoint setting.

Value format (verified from RunPod's own runpodctl reference, `reference/model-caching.md`):
the **full HF URL with a revision suffix**, e.g. `https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct:main`.
Needs runpodctl ≥ 2.4.0; `--model-reference`/`--clear-models` on `serverless update` were
fixed for GPU endpoints in v2.14.0, so use ≥ 2.14.0.

1. Pick the binary. The laptop copy is `C:\Users\arulp\AppData\Local\Temp\opencode\runpodctl.exe`;
   check `runpodctl.exe version`. If it is < 2.14.0 or missing, download
   `https://github.com/runpod/runpodctl/releases/download/v2.14.0/runpodctl-windows-amd64.exe`
   (same release the CI deploy job installs) to that path.
2. Export the key from `.env` without printing it (PowerShell):
   ```powershell
   $envl = Get-Content C:\Projects\opencode\video_image\.env
   $env:RUNPOD_API_KEY = (($envl | Where-Object { $_ -match '^RUNPOD_API_KEY=' } | Select-Object -First 1) -split '=',2)[1]
   $eid = (($envl | Where-Object { $_ -match '^WAN_ENDPOINT_ID=' } | Select-Object -First 1) -split '=',2)[1]
   ```
3. Attach:
   ```powershell
   $ctl = "C:\Users\arulp\AppData\Local\Temp\opencode\runpodctl.exe"
   & $ctl serverless update $eid --model-reference "https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B:main"
   ```
   Expected: the endpoint JSON echoes back (like the CI deploy log) — confirm `templateId` is
   still `25514mi5ae` and workers are still `0 / 3`. If the command errors on the flag, print
   `& $ctl serverless update --help` and stop; do NOT fall back to delete/recreate.
4. Verify: `& $ctl serverless get $eid -o json` — look for a model / cached-model field carrying
   the Wan URL. The selftest in Part B reports `weights.runpod_cached_snapshot` once RunPod
   has finished staging (34 GB; may take a while the first time — RunPod holds the worker
   start, unbilled, until it is there).

No token needed (public repo). One cached model per endpoint. If it cannot be attached,
Part B still works — the worker falls back to downloading, and the selftest says so.

**Order matters:** do this AFTER Part A's CI deploy has finished. `deploy.sh` runs
`serverless update` without `--model-reference`; whether that clears the reference is not
documented, so attach last, and re-check it with `serverless get` after any future push
(making `deploy.sh` pass it is a Phase-3 item in §6).

---

## 4 · Part B — the first sample video (ONE bounded run, ~$0.30 worst case)

Preconditions: Part A green; endpoint idle (`/health` shows 0 workers, 0 jobs — the script
checks and refuses otherwise).

```
cd C:\Projects\opencode\video_image
powershell -ExecutionPolicy Bypass -File scripts\first_video.ps1
```

What it does, in order, and where it stops:

1. Reads key + endpoint id from `.env` (never typed). Prints `/health`.
2. **selftest job** (`{"input":{"op":"selftest"}}`): boots a worker, loads no weights, returns
   the shim report. **Stops** unless `ok=true` and `shim.model_binding_patched=true`. Prints the
   GPU, free VRAM, `huggingface_hub` version (closes the Phase-1 open item) and whether the
   RunPod cached snapshot was found.
3. **One real job**: `ti2v-5B`, `1280*704`, 81 frames (3.4 s @ 24 fps), 20 steps, guide 5.0,
   seed 30313, a MinMini-style prompt (override with `-Prompt "..."`). Polls `/status` every
   15 s with progress lines (`resolving weights` → `loading pipeline` → `sampling …` →
   `encoding` → `compacting`), 35-minute cap (cancels the job if exceeded).
4. On `COMPLETED`: writes `outputs\<stamp>-ti2v-5B-seed30313-81f-20s.mp4` and a `.json`
   sidecar with the effective parameters and timings. On `FAILED`: prints the traceback the
   handler returned and **exits 1 — no resubmit.**
5. Waits (up to 7 min) for `/health` workers to drain to 0 and says so.

Expected timings on a cold 4090 without cached weights: selftest 1–4 min; job ≈ 8–15 min of
which 5–10 min is the download. With cached weights: job ≈ 4–6 min.

Report back: the selftest JSON, the job's meta JSON, the mp4 path + size, and the final
`/health` line. If the video plays and shows the prompt's subject with coherent motion, the
endpoint has produced its first video and Phase 3 (S3/R2, GPU list, container disk) can be
planned against real numbers.

**If the job fails:** paste the `error` text. Do not change code and re-run; the next step is a
diagnosis in Cowork.

---

## 5 · Suggested commit

```
fix: correct SDPA attention semantics, add selftest op, cached-model lookup, sized output

The SDPA replacement installed by boot.py passed Wan's [B, L, heads, D] tensors
straight into torch.scaled_dot_product_attention, which expects [B, heads, L, D].
Self-attention silently attended across heads (noise output); cross-attention
raised a shape error once Lq != Lk. Replace it with a wrapper that transposes in
and out, applies q_scale/softmax_scale, builds a k_lens key mask, and accepts
both the flash_attention and attention() kwarg spellings. Verified against a
reference implementation (tests/test_sdpa_numeric.py) and end to end through a
fake wan package mirroring upstream's import graph (tests/test_sweep_fake_wan.py).

Also:
- handler: op=selftest (shim report, GPU, hf_hub version, weights location)
  without loading weights; refuse real jobs when the patch did not reach
  wan.modules.model; accept the payload key aliases used by the runbook;
  report the seed; deliver via S3 URL or a compact libx264 re-encode inline
  only when under RunPod's 10 MB /run output cap; remove the video=None branch.
- models: resolve RunPod cached models at /runpod-volume/huggingface-cache/hub
  before falling back to a billed download; validate what was found.
- generator: return effective parameters and timings; validate size per task;
  pass n_prompt to ti2v/i2v; verify save_video wrote a file.
- storage: S3-compatible endpoint (R2), public base URL, compact_mp4().
- scripts/first_video.ps1: bounded selftest + one job + drain, never resubmits.
- RUNBOOK: correct payload keys; section 9 state.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01K74qgLLkw1m2TCrreoB84E
```

---

## 6 · Still open — Phase 3, NOT in this dispatch

- **Object storage.** Pick S3 or Cloudflare R2, set `S3_BUCKET`/`S3_ENDPOINT_URL`/`AWS_*` in the
  template env (`TPL_ENV_*` in CI secrets or `config/endpoint.json`). Inline base64 is fine for
  review clips, not for 200-clip bursts.
- **`deploy.sh` model reference.** Once the cached model is confirmed working, add
  `--model-reference` to the template/endpoint upsert so a recreate keeps it.
- **GPU list.** `gpuIds` is a single SKU (RTX 4090). REST supports a priority list
  (`gpuTypeIds`); runpodctl takes comma-separated ids. Candidates that fit TI2V-5B at 720p: L40S,
  A40, RTX A5000 (slower). Do this after one clean run so timing comparisons mean something.
- **Container disk.** 200 GB is sized for the in-container download; once the cached model is
  in use it can drop (the image itself is ~10 GB).
- **`executionTimeoutSec` 1800.** 121-frame / 50-step jobs at 720p may approach it on a 4090;
  revisit with measured `t_sample_s` from the job meta.
- **Quality ladder.** First clip is 81f/20 steps to prove the path. Production defaults for
  MinMini should be re-derived from `t_sample_s` (50 steps ≈ 2.5× the sampling time).
