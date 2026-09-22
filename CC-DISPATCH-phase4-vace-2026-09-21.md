# CC-DISPATCH — Phase 4: VACE-14B reference-to-video on a second endpoint (2026-09-21)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** Claude Code on the laptop.
**Supersedes:** `CC-DISPATCH-phase3e-ab-2026-09-21.md` (do NOT run it — the 5B A/B no longer answers the question).
**Cost:** one CI build (~5 min, free) · one selftest on an 80 GB worker (~$0.05) · three 5 s clips at 50 steps,
each **15–35 min** of an H100/A100 (~$0.8–1.5 each; first one is the cold-cache measurement). Hard stop after the
first clip until Arul has looked at it.

## 0 · Why (read once)

Frame check against the OpenArt Mazhai shots (`outputs\ladder\_qc\openart-vs-ours-2026-09-21.png`): OpenArt's clips are
reference-conditioned — saved characters (Minnu built from 4 turnaround views, Mintu from 1 front view on the lawn) plus
the runsheet's ~150-word scene prompt. Frame 0 comes from the text (back views, arms down, push-ins), not from the
reference. The Wan 2.2 weights on the existing endpoint have no reference input at all (an image is only ever the first
frame), so the cut-out-on-a-canvas I2V pipeline cannot reproduce that. `Wan-AI/Wan2.1-VACE-14B` can: reference images +
text → 81 f @ 16 fps (5.06 s, same as OpenArt's 5 s) at 1280×720. Verified against upstream `wan/vace.py` and
`generate.py` (2026-09-21): `prepare_source([None],[None],[refs], 81, (1280,720))` then `generate(prompt, video, mask,
refs, ...)`; refs are padded onto a white canvas; `context_scale` 1.0; default 50 steps.

## 1 · What Fable wrote (all on disk, tests pass offline)

| file | change |
|---|---|
| `Dockerfile` | `ARG WAN_REPO=Wan2.2` (default) or `Wan2.1`; clones `github.com/Wan-Video/${WAN_REPO}`; the `wan/__init__.py` trim only applies to Wan2.2; `gradio` filtered from requirements like `flash_attn`; `ENV WAN_REPO` exported |
| `app/models.py` | task `vace-14B` → `Wan-AI/Wan2.1-VACE-14B`; required files incl. `diffusion_pytorch_model.safetensors.index.json` |
| `app/generator.py` | task table built from what the image's `wan` exposes; `_force_bf16_from_pretrained` (VACE shards are ~63 GB fp32 → load as bf16 ≈ 34 GB); `_flatten_reference` (alpha → white); vace branch calling `prepare_source` + `generate` exactly as upstream; `cache_video`/`save_video` name tolerance (Wan2.1 vs 2.2); guards (vace needs `ref_images`, refuses `image`; non-vace refuses `ref_images`); result adds `wan_repo`, `dit_dtype`, `ref_images`, `context_scale` |
| `app/storage.py` | unique temp names for every decoded/downloaded input (multi-ref jobs no longer overwrite `input.png`); base64 validated before any file is created |
| `handler.py` | `ref_images` / `context_scale` aliases, `_resolve_refs` (list or single string, ≤ 8, every entry must resolve), cleanup of refs and `-flat.png`; selftest adds `wan_repo`, `tasks`, `host_ram_gb` |
| `config/endpoint-vace.json` | second endpoint `wan-vace-serverless`, image tag `:vace`, `DEFAULT_TASK=vace-14B`, `WAN_REPO=Wan2.1`, 80 GB GPU priority list, `executionTimeoutSec 5400`, workersMax 2, model reference VACE-14B |
| `scripts/deploy.sh` | `ENDPOINT_CONFIG=<path>` selects the config (default unchanged) |
| `scripts/vace_shot.ps1` | one reference-to-video job: `-Refs` (1–6 paths, alpha flattened to white, ≤ 1600 px, saved as `<Label>-refN.png`), `-PromptFile`/`-NegativePromptFile` (UTF-8), selftest **money gate** (refuses without `weights.runpod_cached_snapshot`), `.env` key `WAN_VACE_ENDPOINT_ID`, output `outputs\vace\`, drain wait |
| `prompts/mazhai/` | `I1-opening-backview.txt`, `V1a-mintu-at-glass.txt`, `V2c-minnu-impatience.txt`, `NEGATIVE.txt` (runsheet negative + Wan's default Chinese negative), `README.md` |
| `tests/test_generator_vace.py` (new), `tests/test_handler.py`, `tests/test_models.py` | wiring, bf16 load, flattening, guards, multi-ref cleanup, selftest fields, VACE snapshot detection |
| `RUNBOOK.md` §10 | the above, in runbook form |

Run the tests first (all six must pass, no GPU): `python tests\test_sdpa_numeric.py`, `test_sweep_fake_wan.py`,
`test_models.py`, `test_decode_guard.py`, `test_handler.py`, `test_generator_vace.py`.

## 2 · Part A — CI workflow for the VACE image (protected path: write by hand)

Create `.github/workflows/build-deploy-vace.yml`. **`workflow_dispatch` only** — it must not run on every push, because
its deploy step rotates the VACE endpoint's workers. Content:

```yaml
name: build-deploy-vace

on:
  workflow_dispatch:

env:
  IMAGE: ghcr.io/${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    outputs:
      image: ${{ env.IMAGE }}:vace-${{ github.sha }}
    steps:
      - uses: actions/checkout@v4
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and push (Wan2.1 / VACE)
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ${{ env.IMAGE }}:vace
            ${{ env.IMAGE }}:vace-${{ github.sha }}
          build-args: |
            WAN_REPO=Wan2.1
            BAKE_TI2V=0

  deploy:
    runs-on: ubuntu-latest
    needs: build
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - name: Install runpodctl
        run: |
          curl -fsSL https://github.com/runpod/runpodctl/releases/download/v2.14.0/runpodctl-linux-amd64 -o /usr/local/bin/runpodctl
          chmod +x /usr/local/bin/runpodctl
      - name: Upsert VACE template and endpoint
        env:
          RUNPOD_API_KEY: ${{ secrets.RUNPOD_API_KEY }}
          RUNPOD_REGISTRY_AUTH_ID: ${{ secrets.RUNPOD_REGISTRY_AUTH_ID }}
          ENDPOINT_CONFIG: config/endpoint-vace.json
          TEMPLATE_IMAGE: ${{ needs.build.outputs.image }}
          TPL_ENV_HF_TOKEN: ${{ secrets.HF_TOKEN }}
          TPL_ENV_S3_BUCKET: ${{ secrets.TPL_ENV_S3_BUCKET }}
          TPL_ENV_S3_ENDPOINT_URL: ${{ secrets.TPL_ENV_S3_ENDPOINT_URL }}
          TPL_ENV_AWS_REGION: ${{ secrets.TPL_ENV_AWS_REGION }}
          TPL_ENV_AWS_ACCESS_KEY_ID: ${{ secrets.TPL_ENV_AWS_ACCESS_KEY_ID }}
          TPL_ENV_AWS_SECRET_ACCESS_KEY: ${{ secrets.TPL_ENV_AWS_SECRET_ACCESS_KEY }}
        run: bash scripts/deploy.sh
```

Also fix the image name in `config/endpoint-vace.json` (`template.image`) to this repo's real GHCR path with tag `:vace`
(the existing `config/endpoint.json` shows the real org/name; TEMPLATE_IMAGE overrides it at deploy time anyway).

## 3 · Part B — GPU ids, then commit + push + run the workflow

**GPU ids.** `config/endpoint-vace.json` lists `gpuTypeIds` `["NVIDIA H100 80GB HBM3","NVIDIA H100 PCIe","NVIDIA A100 80GB
PCIe","NVIDIA A100-SXM4-80GB"]` and `gpuId "NVIDIA A100 80GB PCIe"` for the create call. These are the id strings as I
remember them — **verify before deploying**: `runpodctl` has no gpu-list command in 2.14, so query the REST API
(`curl -H "Authorization: Bearer $RUNPOD_API_KEY" https://rest.runpod.io/v1/gpus` — if that route is not there, look up the
exact ids in the RunPod console's GPU picker or `docs.runpod.io/references/gpu-types`). Correct the JSON to the exact
strings; keep 80 GB cards only. Do not put a 48 GB card in the list (34 GB DiT + 11 GB T5 + 720p activations).

```
git add Dockerfile app/models.py app/generator.py app/storage.py handler.py config/endpoint-vace.json scripts/deploy.sh scripts/vace_shot.ps1 prompts/mazhai tests/test_generator_vace.py tests/test_handler.py tests/test_models.py RUNBOOK.md CC-DISPATCH-phase4-vace-2026-09-21.md .github/workflows/build-deploy-vace.yml
git commit -m "phase4: Wan2.1 VACE-14B reference-to-video worker path, second endpoint config, vace_shot client, mazhai prompts"
git push
gh workflow run build-deploy-vace ; gh run watch
```

Expected in the deploy log: `== endpoint config: .../config/endpoint-vace.json ==`, template `wan-vace-serverless`
created, endpoint `wan-vace-serverless` **created** (first time → the `serverless create` branch with `--model-reference
https://huggingface.co/Wan-AI/Wan2.1-VACE-14B:main`), then the `Done. Endpoint: wan-vace-serverless (<id>)` line. Because
the endpoint is new, the REST PATCH block does not run on create — run it once by hand so the 5400 s timeout and the GPU
priority list are applied:

```
curl -sS -X PATCH -H "Authorization: Bearer $RUNPOD_API_KEY" -H "Content-Type: application/json" \
  https://rest.runpod.io/v1/endpoints/<id> -d '{"executionTimeoutMs":5400000,"gpuTypeIds":[<the verified list>]}'
```
(HTTP 200 expected.) Put `WAN_VACE_ENDPOINT_ID=<id>` in `.env` (append; `.env` stays untracked). Never delete/recreate
either endpoint.

**Model staging.** RunPod stages the 75 GB cached model on the host when the endpoint is created; the first worker can sit
in `initializing` for a long time (the 5B took ~20 min for 34 GB). That is unbilled. Don't poke it; poll `/health`.

## 4 · Part C — selftest (the money gate), one clip, stop

```
cd C:\Projects\opencode\video_image
powershell -ExecutionPolicy Bypass -File scripts\vace_shot.ps1 `
  -Refs "C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Mintu\Gemini_Generated_Image_fxwpvvfxwpvvfxwp.jpeg" `
  -Label v1a-mintu -PromptFile prompts\mazhai\V1a-mintu-at-glass.txt -NegativePromptFile prompts\mazhai\NEGATIVE.txt
```

That single command runs the selftest first. **It must show**: `ok`, `wan_repo: Wan2.1`, `tasks: ["vace-14B"]`, an 80 GB
`gpu`, `weights.runpod_cached_snapshot` set (else the script stops — do not override), `host_ram_gb` (report it: the
DiT is parked on the CPU during decode with offload, so < 64 GB is a risk worth knowing before the job), `alloc_conf`
set. Then it submits V1a with the single Mintu lawn reference (the same image OpenArt's Mintu character was built from).

Watch the RunPod worker log for the first job; the lines that matter, in order:
`VaceWanModel.from_pretrained now loads weights as torch.bfloat16` → `pipeline vace-14B loaded ... (dit dtype torch.bfloat16)`
→ the tqdm 50-step bar → `VAE decode start` → `uploading`. If `dit dtype` says float32, STOP (the bf16 wrap did not take;
the card will OOM) and report.

**Stop after this clip.** Report: the selftest block, the meta JSON (`gpu`, `dit_dtype`, `t_load_s`, `t_sample_s`,
`t_total_s`, `vae_decode_*`, `delivery`, `host_ram_gb`), the file path, and a 5-frame strip:
```
ffmpeg -y -i outputs\vace\<clip>.mp4 -vf "select='eq(n,0)+eq(n,20)+eq(n,40)+eq(n,60)+eq(n,80)',tile=5x1" -vsync 0 outputs\vace\_qc\v1a-strip.png
```
Arul judges it against `songs\Mazhai- rain rain go away\03_V1a_mintu-at-glass.mp4`. Only on his go: V2c and I1.

## 5 · The two follow-on clips (on Arul's go only)

```
powershell -ExecutionPolicy Bypass -File scripts\vace_shot.ps1 -SkipSelftest `
  -Refs "C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\front.png","C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\back.png","C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\left.png","C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\right.png" `
  -Label v2c-minnu -PromptFile prompts\mazhai\V2c-minnu-impatience.txt -NegativePromptFile prompts\mazhai\NEGATIVE.txt

powershell -ExecutionPolicy Bypass -File scripts\vace_shot.ps1 -SkipSelftest `
  -Refs "<Minnu front.png>","<Minnu back.png>","<Mintu Gemini_Generated_Image_fxwpvvfxwpvvfxwp.jpeg>" `
  -Label i1-opening -PromptFile prompts\mazhai\I1-opening-backview.txt -NegativePromptFile prompts\mazhai\NEGATIVE.txt
```
(Minnu's PNGs are 1600×1600 with a transparent background — the script flattens them to white, which is what VACE's
preprocessor expects. The 4 Minnu refs total ~3.5 MB base64; fine under the 9 MB payload cap.)

## 6 · If something breaks

- Import error at worker boot mentioning `WanTI2V`, `textimage2video`, `save_video`: the image was built from the wrong
  repo — check the workflow's `WAN_REPO=Wan2.1` build-arg and the selftest's `wan_repo`.
- Selftest `model_binding_patched: false`: the SDPA sweep did not reach `wan.modules.model` in Wan2.1 — report
  `shim.patched`; do not run a job.
- OOM during sampling on an 80 GB card with `dit dtype torch.bfloat16`: report the `VAE decode start` memory line and the
  OOM line; the next lever is `T5_CPU=1` in the template env (T5 encodes on the CPU, ~1 min slower), not a smaller GPU.
- Job takes > 60 min: the script cancels it at `-JobTimeoutMin 60`; report `t_load_s` if present. Don't resubmit.

## 7 · Not in this dispatch

- Any change to the 5B endpoint (it stays for previews and no-character shots).
- `Wan2.2-VACE-Fun-A14B` (alibaba-pai, VideoX-Fun codebase) — fallback only if 2.1 VACE's identity hold disappoints.
- Prompt extension (`--use_prompt_extend`, Qwen) — a later lever; the runsheet prompts are already dense.
