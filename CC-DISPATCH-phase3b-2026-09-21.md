# CC-DISPATCH — Phase 3b: L40S fallback + Minnu/Mintu step ladder (2026-09-21)

**Repo:** `C:\Projects\opencode\video_image` · **HEAD:** `cb44bf5` · **Executor:** Claude Code on the laptop.
**Cost:** Part A none (one CI deploy). Part B ≈ **$0.60–0.90** for two ladders (8 jobs, 3 in parallel; a
50-step rung ≈ 15.5 min sampling). Bounded by the script; nothing resubmits.
**Decisions taken by Arul:** (2) step ladder with Minnu and Mintu turnaround refs as start frames;
(3) L40S fallback. (1) R2 storage: agreed in principle — setup steps in §4, not required for this run.

---

## 1 · Changes in the working tree (uncommitted)

| file | change |
|---|---|
| `config/endpoint.json` | `gpuTypeIds: ["NVIDIA GeForce RTX 4090", "NVIDIA L40S"]` — priority order; RunPod rents the 4090 when one is free, else an L40S (48 GB, similar speed, ~2× $/s). Reaches the endpoint through the REST PATCH added in 3a.2. |
| `scripts/step_ladder.ps1` | **new** — image-to-video ladder. Same start frame + prompt + seed at `-Steps 20,30,40,50`; submits all rungs at once (3 run in parallel on `workersMax 3`, warm workers skip the 148 s load); saves `outputs\ladder\<stamp>-<label>-seed<seed>-81f-<n>steps.mp4` + `.json` per rung and a `<stamp>-<label>-ladder.json` summary; drains workers at the end. |
| `scripts/step_ladder.ps1` | **start-frame fitting (important):** Wan's I2V path derives the *output* aspect ratio from the start frame (`wan/utils/utils.py best_output_size`), so a square 1536² turnaround ref would produce a ~928×928 video. By default the script composites the ref onto a 1280×704 canvas (`-CanvasColor #F6EFE3`, subject 90 % of height, centred; transparent PNGs composite cleanly) and saves it as `outputs\ladder\<label>-startframe-1280x704.jpg`. `-NoFitToFrame` sends the file as-is. |

The handler already accepts `image` as a data URI (`_resolve_image` → `storage.write_b64`), and TI2V-5B
with `img` routes to upstream's `i2v()`. No worker code changes; **no image rebuild is needed** —
the deploy only re-PATCHes the endpoint.

## 2 · Part A — commit, push, watch CI (no GPU)

```
git add config/endpoint.json scripts/step_ladder.ps1 CC-DISPATCH-phase3b-2026-09-21.md
```
Commit (§5), push, `gh run watch`. In the deploy log confirm the PATCH body contains
`"gpuTypeIds": ["NVIDIA GeForce RTX 4090", "NVIDIA L40S"]` and `HTTP 200`. Then
`runpodctl serverless get wv9oneserd7vj6 -o json` → `gpuIds` lists both.
If the PATCH returns 4xx naming the GPU id, the exact RunPod id string for the L40S may differ —
paste the body; `runpodctl gpu list` prints the valid ids.

## 3 · Part B — the two ladders

Start frames come from the generation refs (folder per character; each has `face-front`,
`face-threequarter`, `body-relaxed` as transparent PNG + `-neutral.jpg`):
`C:\Channel Contents\MinMiniKids\charecter bible\generation-refs-2026-08-31\<Character>\`
Use the **body-relaxed transparent PNG** (whole figure; the script composites it) — list the folder
first (`Get-ChildItem`) and use the actual filename.

```
cd C:\Projects\opencode\video_image
powershell -ExecutionPolicy Bypass -File scripts\step_ladder.ps1 `
  -Image "C:\Channel Contents\MinMiniKids\charecter bible\generation-refs-2026-08-31\Minnu\<body-relaxed png>" `
  -Label minnu `
  -Prompt "Minnu looks at the camera, smiles and gives a small wave; her two high pigtails with red bows sway gently; soft matte children's picture-book look, camera steady, no text"

powershell -ExecutionPolicy Bypass -File scripts\step_ladder.ps1 `
  -Image "C:\Channel Contents\MinMiniKids\charecter bible\generation-refs-2026-08-31\Mintu\<body-relaxed png>" `
  -Label mintu -SkipSelftest `
  -Prompt "Mintu looks at the camera, grins and gives a small wave; the cowlick above his right brow stays in place; soft matte children's picture-book look, camera steady, no text"
```
Run the second ladder right after the first finishes so the workers are still warm (300 s idle
window) — that saves three 148 s loads. Keep the prompts motion-only as above: on I2V the image
carries identity, long character prose competes with it (Phase-0 finding).

Before submitting, open `outputs\ladder\minnu-startframe-1280x704.jpg` once and check the figure is
centred on the cream canvas with nothing cropped; if the ref is a head-and-shoulders crop rather than
a full figure, pass `-SubjectHeightFrac 0.8`.

**Report:** the ladder summary block for each character (steps, status, `t_sample_s`, `t_total_s`,
file), the two start-frame paths, and the final `/health`. Arul then reviews the eight mp4s side by
side — identity gate first (two pigtails + both bows / right-brow cowlick, same face at frame 81 as
frame 1), then detail vs steps — and picks the production default.

## 4 · R2 storage — setup when ready (Arul in Cloudflare, then CC), not needed for Part B

1. Cloudflare dashboard → R2 → Create bucket `minmini-wan` (Standard). Note the account id.
2. R2 → Manage API tokens → Create token, permission **Object Read & Write**, scoped to that bucket.
   Copy Access Key ID + Secret. The S3 endpoint is `https://<account-id>.r2.cloudflarestorage.com`.
3. CC: `gh secret set` for `TPL_ENV_S3_BUCKET=minmini-wan`, `TPL_ENV_S3_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com`,
   `TPL_ENV_AWS_REGION=auto`, `TPL_ENV_AWS_ACCESS_KEY_ID`, `TPL_ENV_AWS_SECRET_ACCESS_KEY`; then edit
   `.github/workflows/deploy.yml` (protected path — by hand) to pass them as `env:` on the deploy step
   like `TPL_ENV_HF_TOKEN`, and push. `deploy.sh` already forwards every `TPL_ENV_*` into the template env.
4. From then on job results carry `video` (a 24 h presigned URL) with the raw quality-8 file and
   `delivery: s3`; `first_video.ps1` / `step_ladder.ps1` download from the URL automatically.
   Pricing verified today: $0.015/GB-month, egress free, 10 GB + 1M writes + 10M reads free per month.

## 5 · Suggested commit

```
endpoint: L40S as second GPU choice; add image-to-video step ladder script

gpuTypeIds now lists NVIDIA L40S after the RTX 4090 so a batch does not queue
when no 4090 is free (applied via the REST PATCH in deploy.sh). Add
scripts/step_ladder.ps1: same start frame, prompt and seed at 20/30/40/50
steps, submitted together, saved with per-rung metadata; the turnaround ref is
composited onto a 1280x704 canvas first because Wan's I2V output takes its
aspect ratio from the start frame.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01K74qgLLkw1m2TCrreoB84E
```
