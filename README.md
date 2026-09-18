# Wan 2.2 Stateless Serverless on RunPod

On-demand, stateless video generation. Workers boot from a container image, pull weights
to their own container disk on first use, serve jobs, and are destroyed on scale-down.
No network volumes, no datacenter binding — RunPod's scheduler places workers anywhere.

## Architecture

```
push to main
   │
   ▼
GitHub Actions ──build──▶ ghcr.io/…/wan-video-serverless:{sha}
   │
   ▼  deploy job (runpodctl, idempotent upsert)
template (serverless) ──▶ endpoint (GPU pool, workers, scaling, flashboot)
   │
   ▼
POST https://api.runpod.ai/v2/{endpoint}/runsync   ← your app calls this
```

- Models download to `/models` (container disk) on first worker boot; `HF_HOME` cached
  across jobs on the same worker. `BAKE_TI2V=1` build arg pre-downloads TI2V-5B into the
  image instead.
- Weights come from the official Hugging Face repos: `Wan-AI/Wan2.2-TI2V-5B`,
  `Wan-AI/Wan2.2-T2V-A14B`, `Wan-AI/Wan2.2-I2V-A14B`. The Wan 2.2 inference repo is cloned
  at build time and imported directly (no ComfyUI).

## One-time setup (the only manual steps)

1. Give this repo a GHCR image: set `template.image` in `config/endpoint.json` to
   `ghcr.io/<owner>/wan-video-serverless:latest` (Actions pushes there automatically).
2. GitHub repo Settings → Secrets and variables → Actions:
   - `RUNPOD_API_KEY` — your RunPod key (console.runpod.io → Settings → API Keys)
   - `HF_TOKEN` *(optional)* — lets workers download weights without HF rate limits,
     injected as `HF_TOKEN` into the template env at deploy time.
3. Push to `main`. The `build-deploy` workflow builds, pushes, and creates the template +
   endpoint for you. No pip, no local runpodctl, no console clicks.

## Usage

Once the endpoint exists (`workflow_run` output or `runpodctl serverless list`):

```bash
export RUNPOD_API_KEY=...

python client/generate.py \
  --endpoint <endpoint-id> \
  --task ti2v-5B \
  --prompt "two anthropomorphic cats in boxing gear fight on a stage" \
  --size 1280*704 --frame-num 81 --out demo.mp4
```

I2V (image → video), pass `--image <http-url-or-s3-uri-or-base64>`.

Raw request:

```bash
curl -H "Authorization: Bearer $RUNPOD_API_KEY" \
  https://api.runpod.ai/v2/<endpoint-id>/runsync \
  -d '{"input":{"prompt":"a cat surfing","task":"ti2v-5B","frame_num":81}}'
```

Response: `{"video": "<presigned S3 URL>"}` if `S3_BUCKET` is configured (recommended for
large outputs), otherwise `{"video_b64": "..."}`. Configure S3 via worker env
(`s3` under template env, or `S3_BUCKET`/`AWS_*` in `config/endpoint.json`).

## Config

Everything lives in `config/endpoint.json`. Sensible starting point:

- `template.env.DEFAULT_TASK: "ti2v-5B"` (5B fits 24 GB, good default quality)
- `endpoint.gpuPool: "ADA_24"` (RTX 4090). For 14B FP8/GGUF use `ADA_48` (L40S/RTX 6000),
  for full-precision 14B 720p use `HOPPER_80` (H100). Check pools with
  `runpodctl gpu list`.
- `workersMin: 0`, `workersMax: N` → zero idle cost, bounded burst.
- `flashBoot: true` → first request on a cold worker is much faster (resumes a cached
  container). Still stateless — there is no volume.
- `idleTimeoutSec: 300`, `executionTimeoutSec: 1800` (30 min cap; 14B 720p can take
  15–25 min).

Deploy settings for a run are overridable without editing files:

- `TEMPLATE_IMAGE=…` env → image tag to deploy (used by CI to pin `:{sha}`)
- `TPL_ENV_<NAME>=…` env → any extra template env vars at deploy time

## Deploy from your machine

`scripts/deploy.sh` is the same path CI uses and is idempotent (create or update). Run it
on macOS/Linux/WSL with `RUNPOD_API_KEY` set; it auto-installs `runpodctl` if missing.

```bash
RUNPOD_API_KEY=... bash scripts/deploy.sh
```

Notes:

- Changing `gpuPool` after creation triggers endpoint recreate (delete + create) —
  GPU type cannot be changed in place on RunPod.
- Verify the endpoint has a ready worker: `runpodctl serverless health <id>`.

## Supported jobs

`task` (request or `DEFAULT_TASK`): `ti2v-5B` (T2V + I2V, 24 GB), `t2v-A14B`, `i2v-A14B`
(40+ GB). Inputs: `prompt` (required), `image`, `size`, `frame_num` (4n+1), `steps`,
`shift`, `guide_scale`, `seed`, `offload`, `solver`, `n_prompt`, `output_key`.

## Costs

Serverless bills per second, only while workers run. With `workersMin: 0` an idle endpoint
costs nothing; the first request pays cold-start (~2–20 min: image pull + model download +
model load). `min_workers=1` or `BAKE_TI2V=1` trade idle cost / build size for latency.
A ~81-frame 720p TI2V-5B video runs a few minutes on a 4090.