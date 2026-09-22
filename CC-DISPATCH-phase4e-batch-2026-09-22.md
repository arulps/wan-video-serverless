# CC-DISPATCH — Phase 4e: R2 model origin + batch runner, proven on a fresh pod (2026-09-22, rev 2)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (pod shell + API, headless).
**Outcome wanted:** a fresh pod in *any* datacenter is productive ~10 min after boot with nothing kept on RunPod
between batches, a whole shot list runs from one command, outputs land in R2, and the pod stops itself. Then Arul's
next song (planned with Opus into the `songs/<slug>/` format) is just `batch_runner.py`.
**Budget:** pod time ≈ 1.5 h (~$3–5 on A100/H100) + R2 storage ≈ $0.60/mo for 40 GB (zero egress). Hard stop 2 h.
**Rev 2 change:** the RunPod network volume from rev 1 is dropped — the existing Cloudflare R2 bucket (Phase 3c) is
the model origin instead. Cheaper ($0.60 vs $3/mo), no datacenter lock-in, and the old pod's disk is no longer
needed. A volume comes back only in Phase 4f (serverless one-offs), if at all.

## 0 · Phase 4d verdict (Fable, frame-checked — `outputs\vace\pod\_qc\phase4d-*.png`)
PASS. 4- and 6-step distilled clips hold identity and blocking as well as or better than the 30-step keeper; 4.3–5.5 min
warm on an A100 ≈ $0.15–0.20 per 720p clip. Deficits to handle here: the rain disappeared (cfg-1 adherence), arms drift
in the last frames, and SaveVideo's default encode is ~1.5 Mbps.

## 1 · What Fable wrote (all on disk; tested against mocks)
| file | purpose |
|---|---|
| `scripts/pod_bootstrap.sh` | **new** — `models-push` (once: manifest + upload the 4 model files to R2, size-verified), `pull` (every fresh pod: pull + verify sizes against the manifest, sync `wan/`, start ComfyUI if needed, wait until `UNETLoader` lists the VACE model, print boot-to-ready), `wan-push` (refresh `comfy/ prompts/ docs/ songs/` on R2 from the laptop), `out-push songs/<slug>` (batch outputs → R2). Uses the **same env names as the worker** (`S3_BUCKET`, `S3_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`); rclone reads them straight from env — no config file, nothing written to disk. Tested end to end against a fake rclone (push, pull on a fresh tree, byte-identical, corrupted file → refuses to start, missing env → clear error). |
| `docs/SHOT-LIST-SPEC.md` | the song folder + `shots.csv` + structured shot file (`ATMOSPHERE/ANGLE/SHOT/POSE/MOTION/NEGATIVE`) contract — what the planning session writes |
| `docs/PROMPT-PLAYBOOK.md` | every prompt lesson from 3d–4d, incl. the character lock lines the runner reads (§8) |
| `comfy/batch_runner.py` | `--song songs/<slug> --hosts <url,...> [--seed] [--only] [--retry-failed] [--dry-run] [--stop-cmd] [--max-minutes] [--timeout-min]`; one in-flight job per host (several pods = `--hosts a,b`), resumable via `status` in the CSV (atomic writes), sidecar JSON with the exact prompt, QC strips, summary with GPU-minutes, Ctrl-C / max-minutes interrupt + stop-cmd |
| `comfy/run_comfy.py` | refactored: `build_workflow()` / `submit_and_wait()` / `interrupt()`; **CC's two production fixes folded in** (browser User-Agent on every request for the RunPod proxy; flushed prints); no-ref shots drop the LoadImage node (text-to-video through VACE) |
| `comfy/make_ref_sheet.py` | builds 1280×720 white-padded reference sheets from 1–4 images |
| `songs/_selftest/` | format example: `world.txt` (line 1 = place clause), a structured V2c shot, a no-ref I0 shot, `shots.csv` |

`python comfy\batch_runner.py --song songs\_selftest --hosts http://x --dry-run` prints the assembled prompts with no
network — run it once to see the block order.

## 2 · Part A — R2 as the model origin (once)
R2 keys: the bucket/endpoint/token already in `.env` (Phase 3c). **Never print them; never put them in the repo, a
dispatch, or a Docker image.** They reach the pod only as pod environment variables.

1. **Push the models from the old pod** `99nzy9hhow6slc` (its disk still holds the four files):
   - Start it. In the RunPod console → pod → *Edit* → Environment Variables, add `S3_BUCKET`, `S3_ENDPOINT_URL`,
     `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` with the values from `.env` (Arul pastes them, or CC reads `.env`
     with the usual guard and sets them via the pod-update API — either way they are not echoed to chat/logs).
   - Copy `scripts/pod_bootstrap.sh` to the pod (`runpodctl send`, scp, or paste), then on the pod:
     `bash pod_bootstrap.sh models-push` (set `COMFY_ROOT` if the template's ComfyUI is not at `/workspace/ComfyUI`;
     the script auto-detects otherwise). Expect ~40 GB up; record the wall time. It writes `models/MANIFEST.txt`
     (size + path per file) and verifies every object size on R2 against it before saying done.
   - Also on the pod: `bash pod_bootstrap.sh wan-push` from a directory holding `comfy/ prompts/ docs/ songs/`
     (or run `wan-push` from the laptop after `winget install Rclone.Rclone` with the four env vars set in that shell —
     same command, same effect). Do **not** push `outputs/` — the refs the runner needs live in `songs/<slug>/refs/`.
   - Stop the old pod.
2. **Prove a cold boot from R2**: deploy a *fresh* ComfyUI-template pod (A100 80 GB or H100, any DC with
   availability, 100 GB container disk), set the same four env vars on it, copy `pod_bootstrap.sh` in, run
   `bash pod_bootstrap.sh pull`. It must end with `BOOT-TO-READY: models <n> s, total <m> s` and
   `/object_info/UNETLoader` listing `wan2.1_vace_14B_fp16.safetensors`. **Report both numbers** — this decides
   whether R2-only stays the plan (target: total ≤ 15 min) or a network volume is added in 4f.
   If `pull` reports `BAD` on any file, do not start a batch: rerun `pull` (rclone resumes) and report.
3. **Delete the old pod** `99nzy9hhow6slc` once step 2 passed on the fresh pod (R2 now holds the master copy).

## 3 · Part B — Mazhai shot list in the new format (Fable's job, but CC checks it)
Fable will write `songs/mazhai/` (world.txt from the runsheet WORLD + INTERIOR clause, the 12 shots as structured
files, refs from `outputs\vace\refs\`). Until it lands, use `songs/_selftest` to prove the plumbing.

## 4 · Part C — prove the batch on the fresh pod
```
cd /workspace/wan
python comfy/batch_runner.py --song songs/_selftest --hosts http://127.0.0.1:8188 --dry-run
python comfy/batch_runner.py --song songs/_selftest --hosts http://127.0.0.1:8188 --seed 30313 \
    --max-minutes 60 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/_selftest && runpodctl stop pod $RUNPOD_POD_ID"
```
(`runpodctl` on the pod needs `RUNPOD_API_KEY` in the pod env; if it is not available there, run the batch from the
laptop against the proxy URL with `--stop-cmd "runpodctl stop pod <id>"` and push `out/` afterwards — both paths are
supported. Note the stop-cmd pushes `out/` to R2 *before* stopping, so nothing is lost when the pod disk goes.)
Expect: I0 (no ref, text-to-video) and V2c (Minnu, structured prompt with ATMOSPHERE repeated) done in ~5 min each on
a warm model, `songs/_selftest/out/` populated, strips in `out/_qc/`, CSV statuses `done`,
`r2://<bucket>/songs/_selftest/out/` populated, pod stopped by the runner.
Laptop pull: `rclone copy r2:<bucket>/songs/_selftest/out/ songs\_selftest\out\` (or the R2 console).
**Report the V2c strip — Fable checks whether the rain is back.**
If the rain is still missing at 6 steps / cfg 1.0: rerun V2c only with `cfg` 1.5 in the CSV (`--retry-failed` after
clearing its status) and report both.

## 5 · Known limitation, deferred to Phase 5
Core `SaveVideo` has no quality control (verified in ComfyUI source: inputs are video / filename_prefix / format /
codec) — the ~1.5 Mbps encode stands for now. Phase 5's post step (RIFE 16→30 fps + 2× upscale) will take a PNG
frame sequence from ComfyUI instead and encode the 1080p master itself at crf 16; that is where the quality lives.

## 6 · Report back (numbers Fable needs)
- `models-push` wall time and the manifest (sizes only).
- Fresh-pod `BOOT-TO-READY` (models / total) and the DC + GPU used.
- Per-shot wall times from the batch summary; total pod minutes and $ for the phase.
- V2c and I0 strips; whether the pod stopped itself; whether `out/` arrived in R2.
- **Real token count** of the V2c prompt through ComfyUI's Wan tokenizer (on the pod, from `/workspace/ComfyUI`:
  `python -c "import sys;sys.path.insert(0,'.');from comfy.text_encoders.wan import WanT5Tokenizer as T;import json;t=T(embedding_directory=None);p=json.load(open('/workspace/wan/songs/_selftest/out/'+[f for f in __import__('os').listdir('/workspace/wan/songs/_selftest/out') if f.startswith('V2c') and f.endswith('.json')][0]))['prompt'];print(len(t.tokenize_with_weights(p)['t5xxl'][0]))"`
  — if that import path differs, any way of counting umt5 tokens for the sidecar's `prompt` is fine). The runner's
  `~tokens=` estimate (1.4/word) gets calibrated from this; it decides how many lock lines fit per shot.

## 7 · Commit
```
git add comfy/ docs/ scripts/pod_bootstrap.sh songs/_selftest CC-DISPATCH-phase4d-comfy-pod-2026-09-22.md CC-DISPATCH-phase4e-batch-2026-09-22.md outputs/vace/pod/_qc
git commit -m "phase4d/4e: ComfyUI VACE driver + batch runner, R2 model origin bootstrap, shot-list spec, prompt playbook, 4d QC"
git push
```
(`outputs/vace/pod/_qc` PNGs are small and are the evidence for the 4d decision; the mp4s stay untracked. Confirm
`git status` shows no `.env`, `logs.txt`, `nil`, or `songs/*/out/` before committing.)
