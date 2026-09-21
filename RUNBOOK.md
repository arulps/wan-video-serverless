# wan-video-serverless — Operations Runbook (anti-cost-drain)

> **Read this FIRST.** The single most expensive failure mode of this project is **trial-and-error
> spending**: repeatedly submitting GPU jobs before the root cause is known, holding idle workers,
> and letting a stale image keep failing. Everything below exists to prevent that. Follow the
> guardrails before touching the RunPod account.

---

## 0) Money guardrails (non-negotiable)

| Rule | Why |
|---|---|
| **Never hand-type the endpoint id.** Read it from `.env` programmatically on *every* call and verify it against `runpodctl serverless list`. | Hand-written ids get corrupted (this project burned literal money on 404s from a mistyped id while still paying for worker boots). |
| **Scale to 0 workers when not actively submitting.** `runpodctl serverless update <EP_ID> --workers-min 0 --workers-max 0` then **confirm** ready workers reach 0. | Serverless bills **per active worker per second**, incl. *idle* ones holding a warmed `RTX 4090` (a min=1 idle worker ≈ $0.8–1.2/hr, all day = the ~$10 drain). Idle workers only add value if a job is about to run immediately. |
| **Do NOT resubmit the same job on a FAILED job without a root cause.** Each `ti2v-5B` run = model boot + flash-boot + ~GB download + inference on a rented GPU. A FAILED job still costs the boot + partial inference. | Repeated "submit → FAILED → submit again" is how the balance vanished. |
| **Confirm the worker actually has the FIXED image before trusting COMPLETED.** Read worker container logs at boot; the SDPA-fix image prints the SDPA-forcing shim lines and must NOT hit `assert FLASH_ATTN_2_AVAILABLE` (attention.py:112). | The endpoint can be bound to the *fixed template* while running *stale workers* that still boot the old flash-attn image. |
| **Prefer REST `runsync`/`status` via `runpodctl` over bespoke REST calls.** `runpodctl` handles auth + `-o json`; the raw `https://api.runpod.ai/v2/<eid>/...` GET can 404 while the endpoint is mid-CI-rotation even though it exists. | Prevents chasing phantom "endpoint gone" 404s (which also caused extra recreation attempts/spend). |
| **One bounded attempt at a time.** One submit → poll to terminal → download. No fire-and-forget + infinite polls. Set an explicit cost cap per session (see §5). | Bounds the burn. |

**Total cost so far to know:** roughly **$10** was spent with **zero videos produced** because of idle-minimum workers running all morning + repeated FAILED-job boot cycles + endpoint rebuilds during CI rotation. The *fix itself* was always in code; the leaks were (a) stale-worker boots and (b) the resubmit loop.

---

## 1) What this project is

Serverless **Wan2.2 → video ("ti2v-5B")** on RunPod Serverless.
- Repo/config dir: `C:\Projects\opencode\video_image` (git; pushes to GitHub; GH Actions builds the Docker image and upserts template+endpoint).
- API auth in `.env`: `RUNPOD_API_KEY`, `WAN_ENDPOINT_ID`, `TEMPLATE_IMAGE`, `GITHUB_REPO`, `TPL_*`, `GPU_POOL`.
- `runpodctl` binary (Windows): `C:\Users\arulp\AppData\Local\Temp\opencode\runpodctl.exe` (download if missing from runpodctl GitHub releases).

## 2) Architecture / current state (verified)

- Endpoint name: `wan-video-serverless`; endpoint id = **the** value of `WAN_ENDPOINT_ID` in `.env` (**read it; do not type**).
- Endpoint is bound to user template **`25514mi5ae`** (`wan-video-serverless`), whose image is currently:
  `ghcr.io/arulps/wan-video-serverless:6ae3fe74…` — **this is the SDPA-forcing image** (built+upserted by CI run `35453127770` @ 20:34, success).
- So the *template* carries the fix; the danger is **stale running workers** still booting the OLD flash-attn image.

## 3) The bug and the fix (so you don't re-diagnose it)

- **Symptom:** every job died with `assert FLASH_ATTN_2_AVAILABLE` (also `.FLASH_ATTN_3` / `flash_attn` not installed) at
  `/opt/wan/wan/modules/attention.py:112`, reached via `wan/modules/model.py:145/243/490` — i.e. the deployed worker did NOT have flash-attn, yet Wan code asserted it.
- **Fix (already merged, in HEAD `7e9f193`, code commit `6ae3fe74`):** the boot path now **forces Wan attention to `scaled_dot_product_attention` (SDPA)** by shimming/replacing the flash-attention call site at boot, so no `FLASH_ATTN_*_AVAILABLE` assert can fire that needs flash-attn. The reconstruction of the fix commit: `git log -1 --format='%H %s'` → `7e9f193… ci: marker - force redeploy…` w/ parent `6ae3fe74… boot: force Wan attention to scaled_dot_product_attention (SDPA)…`.
- **Do NOT re-diagnose this from scratch.** If you see that assert in container logs again, the image/worker is STALE — **force worker rotation** (§4), do not change code.

## 4) Correct procedure to get a video (bounded)

```powershell
$ctl = "C:\Users\arulp\AppData\Local\Temp\opencode\runpodctl.exe"
$envl = Get-Content "C:\Projects\opencode\video_image\.env"
$KEY  = (($envl|?? RUNPOD_API_KEY=)  -split '=',2)[1]
$EID  = (($envl|?? WAN_ENDPOINT_ID=) -split '=',2)[1]   # ALWAYS read; never type
$env:RUNPOD_API_KEY = $KEY
```

1. **Confirm current binding + worker health (authority only):**
   `& $ctl serverless get $EID --include-template -o json`  →  note `templateId`, `workers_ready`/`workers_total`.
2. **If `workers_ready = 0`** (CI rotation) — wait/poll short, don't recreate anything.
3. **Rotate workers onto the fixed image (the critical step deploy.sh does NOT do reliably):**
   `& $ctl serverless update $EID --workers-min 0 --workers-max 0`  → poll until `workers_total == 0`
   `& $ctl serverless update $EID --workers-min 1 --workers-max 1`  → poll until `workers_ready > 0`
   *Reason:* CI/deploy.sh updates the **template image** but the running worker containers keep the OLD image until scaled to 0/freshly booted locked answer
4. **Check boot logs of the fresh worker for the SDPA shim** (confirm it's the fixed image):
   `& $ctl serverless logs $EID --source container --tail 60` — must show SDPA-forcing lines and **no** `assert FLASH_ATTN_2_AVAILABLE`.
5. **Submit ONCE, poll to terminal, download** — or just run `scripts\first_video.ps1`, which does 1–6 bounded:
   - REST POST `https://api.runpod.ai/v2/$EID/run` `{input:{prompt, task:"ti2v-5B", size:"1280*704", frame_num:81, steps:20, guide_scale:5.0, seed:30313, n_prompt:"..."}}`
   - The handler's canonical keys are `frame_num` / `steps` / `guide_scale` / `shift` / `n_prompt` / `solver` / `size`.
     Since 2026-09-21 it also accepts the aliases `num_frames`, `base_num_frames`, `sample_steps`, `cfg_scale`,
     `sample_shift`, `negative_prompt`, `sample_solver`, `resolution` — the earlier payload in this section used
     keys the handler never read, so `steps` silently ran at the config default (50), not 20.
   - `{input:{op:"selftest"}}` is a cheap job (worker boot, no weights) that returns the SDPA-patch report,
     GPU, huggingface_hub version and where the weights will come from. Run it before the first real job.
   - poll `status/<job>` until `COMPLETED` or `FAILED` (this is a multi-minute inference job; use a poll cap).
   - `COMPLETED` → fetch `runsync/<job>` output → download the `.mp4` URL into `C:\Projects\opencode\video_image\outputs\`.
   - `FAILED` → pull the container-log traceback (authority), **then stop** (do not auto-resubmit).
6. **When done, scale to 0 again** to stop idle billing.

## 5) Session cost cap (set your own)

Default sensible budget per "get a video" attempt: **1 worker rotation + 1 submission + 1 poll + download**. If the fresh-SDPA worker job FAILS once, stop and read logs — do not loop.
Quick arithmetic: RTX 4090 serverless ≈ $0.99–1.19/GPU-hr + idle-minimum charge; a single ti2v-5B 81-frame run ≈ $0.10–0.50 depending on steps + boot. **Scale to 0 between attempts.**

## 6) Known traps / gotchas (learned the hard way)

- **`deploy.sh`'s upsert path** only bumps workers-min/max on an existing endpoint and does NOT force a worker reboot onto a newly-upserted template image → workers keep the old image. Always do the manual scale-0→1 rotation of §4 after a deploy.
- **RunPod REST GET (`/v2/<eid>`) returns 404 while the endpoint is mid-CI/auto-scaling rotation** yet `runpodctl serverless list` still shows it. Don't treat 404 as "endpoint deleted."
- **`ConvertFrom-Json` on native command output** in PowerShell frequently fails on runpodctl's stderr/2>&1; capture with `2>&1 | Out-String` and parse defensively.
- **Hand-typing `WAN_ENDPOINT_ID`** is the single most dangerous anti-pattern here. A single corrupt char → silent 404s while you keep paying for boots. Programmatic reads only.
- **Wan2.2 5B on 4090** is slow and memory-tight; keep the job at 81 frames/20 steps until a COMPLETED video is proven, then raise quality.

## 7) Quick reference

- Endpoint list (authority): `& $ctl serverless list -o json`
- Endpoint detail w/ template: `& $ctl serverless get $EID --include-template -o json`
- Templates (user): `& $ctl template list --type user -o json`
- Update workers: `& $ctl serverless update $EID --workers-min N --workers-max M`
- Submit+get: REST `api.runpod.ai/v2/$EID/{run,runsync,status,runsync}` w/ `Authorization: Bearer $RUNPOD_API_KEY`
- Pull worker logs: `& $ctl serverless logs $EID --source container --tail 100`

---

# 8) SESSION STATE — handoff 2026-09-21 ~10:15 (agency paused; reported laptop)

## Authority (verified via REST this session, do NOT re-derive)

- **Endpoint id**: `wv9oneserd7vj6` — but ALWAYS read the key + id from `.env` (`RUNPOD_API_KEY=`, `WAN_ENDPOINT_ID=`) programmatically; never trust hand-typed copies. (REST `GET /v2/<eid>` returns 404 for the endpoint ROOT — that route does not exist; only `/health`, `/run`, `/status`, `/runsync` do. **404 on `/v2/<eid>` is NORMAL, not a deleted endpoint.**)
- **Current scale = 0/0** → idle, not billing. Nothing should be submitting.
- **Template bound**: templateId `25514mi5ae` (`wan-video-serverless`) → image **`ghcr.io/arulps/wan-video-serverless:6ae3fe74d93e79d85731df058f5b9b5071320fac`** = the SDPA-fix image (commit `6ae3fe74d3…` "force scaled_dot_product_attention"). The fix IS in the image and the template IS bound. GPU: RTX 4090, idle-timeout 300s, workers 0.

## Refined root cause (this is the real blocker, now understood)

- One job submitted this session (job `5ecdd664-678c-4e01-a0e7-75b9d68fdc49-u1`, worker `9zri26q3sos4h6`, 10:01→10:12) ran ~11 min then **FAILED with the same `assert FLASH_ATTN_2_AVAILABLE` at `attention.py:112`**, even though the endpoint is bound to the SDPA-fix template.
- **Why:** `/health` returned 200 almost instantly after scale-to-1 → **RunPod flashboot served a WARM cached worker that had booted the OLD flash-attn image**. Warm-cached workers do NOT pick up template/image changes; only a true cold boot pulls `:6ae3fe74…`. My earlier "worker never ready" was actually instant-ready (200) on a stale cached container — so the old flash assert kept firing.
- Overlap between "scale to 0 then 1" does NOT clear the warm cache reliably (flashboot keeps a warm snapshot between scale events).

## Next session — EXACT money-safe procedure (in order)

1. **Confirm before spending anything**: read `.env` (key+eid) → `REST GET /v2/<eid>/health` should return 200 only when billed worker present; also `runpodctl serverless list -o json` to confirm workersTotal=0 now.
2. **Force a true cold boot of the SDPA image** (do NOT count on scale-to-1 alone):
   - Change a trivial template/env value on the endpoint (e.g. bump an env var or the template config) so flashboot's warm cache key invalidates → this forces a fresh container pull including `:6ae3fe74…`.
   - OR set `--workers 0`, wait until workersTotal=0 confirmed, then delete+recreate the endpoint from the SDPA template (recreate is the guaranteed way to kill the warm cache).
3. **Verify the BOOT before submitting any job**: after the new worker goes 200, pull boot logs and grep for the SDPA shim (no `assert FLASH_ATTN_2_AVAILABLE`, look for `scaled_dot_product_attention`/SDPA lines and absence of the flash assert at attention.py:112). Only submit if boot shows SDPA clean.
4. **One bounded submit + poll**: 5B, 81 frames, 20 steps, cfg 5, ~10-12 min. Poll REST `/status/<job>` → COMPLETED/FAILED. On COMPLETED download via `/runsync/<job>` → save mp4 to `outputs/`. On FAILED pull container logs for the traceback, then **STOP** (no blind retry).
5. **Always end by scaling to 0** (stop billing). Set a strict budget (e.g. one worker boot + one 11-min job ≈ $1-2 max) and halt if exceeded.

## Money lessons this session (they matter)

- ~$10 drained on 2026-09-21 morning from: warm-cached OLD-flash-attn workers repeatedly booting + failing jobs on a billed 4090, and idle workers held with workers-min>0. Every FAILED job still bills the worker boot + GPU uptime.
- **Zero-Zero policy now**: endpoint must sit at 0 workers whenever not actively polling a live job.
- Hand-typing the endpoint id caused repeated 404 confusion → read it from `.env` every time.

## Files/locations

- `.env` — `RUNPOD_API_KEY`, `WAN_ENDPOINT_ID` (authority; read programmatically)
- `scripts/deploy.sh` — upserts template + endpoint from CI
- `.github/workflows/deploy.yml` — CI build+deploy
- `app/boot.py` — SDPA-forcing shim (in image `:6ae3fe74…`)
- `app/modules/attention.py:112` — old flash assert location (fixed image removes it)
- `outputs/` — where downloaded mp4 goes
- runpodctl at `C:\Users\arulp\AppData\Local\Temp\opencode\runpodctl.exe`

---

# 9) SESSION STATE — 2026-09-21 ~12:00 (Fable review; supersedes §8 where they differ)

## What §8 got wrong (now understood)

- §8 blamed FlashBoot's warm cache for the 10:01 failure. The real cause: the SDPA shim in `6ae3fe74`
  patched `wan.modules.attention.flash_attention` only, while `wan/modules/model.py` from-imports the
  function and kept the original → the assert still fired **on the fixed image**. Worker rotation could
  never have fixed it. (Dispatch phase01 fixed the sweep; `92b31d3`.)
- **A second bug hid behind the first:** both shim versions passed Wan's `[B, L, heads, D]` tensors
  straight into `torch.scaled_dot_product_attention`, which expects `[B, heads, L, D]`. Self-attention
  would have returned garbage (attention across heads), cross-attention would have crashed on
  `Lq != Lk`. Fixed in `app/boot.py` (`make_sdpa_flash_attention`, transposes + key mask) and
  verified numerically against a reference implementation (`tests/test_sdpa_numeric.py`).
- The build/deploy pipeline is now trustworthy: run #14 built `:92b31d3…`, template `25514mi5ae`
  carries it, endpoint `wv9oneserd7vj6` is bound to it, workers were rotated by `deploy.sh`.

## Authority (verified from the CI log of run #14, 2026-09-21 ~10:40)

- Endpoint `wv9oneserd7vj6` → template `25514mi5ae` → `ghcr.io/arulps/wan-video-serverless:92b31d3…`
  (this will move to the Phase-2 sha once CC pushes; check the newest run's deploy log).
- GPU RTX 4090, workersMin 0 / workersMax 3, idleTimeout 300 s, executionTimeout 1800 s, flashboot on.
- Weights: not yet attached as a RunPod cached model → first job downloads ~34 GB (billed).
  The 10:01 job proved download + model load + sampling-start all work (~11 min to the failure point).

## Cost model for one bounded run (4090 ≈ $0.00031/s while a worker is up)

- selftest: boot only (image pull if cold) ≈ 1–4 min ≈ **$0.02–0.08**
- real job without cached weights: ~34 GB download (~5–10 min) + load (~1–2 min) + sampling
  (81f × 20 steps ≈ 3–5 min) + encode ≈ **$0.20–0.35**; with cached weights ≈ **$0.10**
- idle after job: 300 s ≈ $0.09 (workersMin=0 drains automatically)

## Output path

- No `S3_BUCKET` → the handler re-encodes to libx264 crf 23 (ffmpeg, in image) and returns
  `video_b64` only if the base64 string is ≤ `MAX_OUTPUT_MB` (9 MB; RunPod's `/run` output cap is
  10 MB). Over the cap → explicit error, never a silent `null`. 81 frames @ 1280×704 crf 23 ≈ 2–5 MB.
- For production set `S3_BUCKET` (+ `S3_ENDPOINT_URL` for Cloudflare R2, `AWS_REGION=auto`,
  `AWS_ACCESS_KEY_ID/SECRET`) in the template env; the result then carries a URL.
