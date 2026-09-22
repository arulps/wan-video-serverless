# CC-DISPATCH — Phase 4e: network volume + batch runner, proven on the Mazhai shot list (2026-09-22)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (pod shell + API, headless).
**Outcome wanted:** a fresh pod is productive 2 minutes after boot, a whole shot list runs from one command, and the
pod stops itself. Then Arul's next song (planned with Opus into the `songs/<slug>/` format) is just `batch_runner.py`.
**Budget:** pod time ≈ 1.5 h (~$3–5 on A100/H100) + network volume ($0.07/GB/mo ≈ $3/mo for 40 GB). Hard stop 2 h.

## 0 · Phase 4d verdict (Fable, frame-checked — `outputs\vace\pod\_qc\phase4d-*.png`)
PASS. 4- and 6-step distilled clips hold identity and blocking as well as or better than the 30-step keeper; 4.3–5.5 min
warm on an A100 ≈ $0.15–0.20 per 720p clip. Deficits to handle here: the rain disappeared (cfg-1 adherence), arms drift
in the last frames, and SaveVideo's default encode is ~1.5 Mbps.

## 1 · What Fable wrote (all on disk; tested against a mock ComfyUI server)
| file | purpose |
|---|---|
| `docs/SHOT-LIST-SPEC.md` | the song folder + `shots.csv` + structured shot file (`ATMOSPHERE/ANGLE/SHOT/POSE/MOTION/NEGATIVE`) contract — what the planning session writes |
| `docs/PROMPT-PLAYBOOK.md` | every prompt lesson from 3d–4d, incl. the character lock lines the runner reads (§8) |
| `comfy/batch_runner.py` | `--song songs/<slug> --hosts <url,...> [--seed] [--only] [--retry-failed] [--dry-run] [--stop-cmd] [--max-minutes] [--timeout-min]`; one in-flight job per host, resumable via `status` in the CSV (atomic writes), sidecar JSON with the exact prompt, QC strips, summary with GPU-minutes, Ctrl-C / max-minutes interrupt + stop-cmd |
| `comfy/run_comfy.py` | refactored: `build_workflow()` / `submit_and_wait()` / `interrupt()`; **CC's two production fixes folded in** (browser User-Agent on every request for the RunPod proxy; flushed prints); no-ref shots drop the LoadImage node (text-to-video through VACE) |
| `comfy/make_ref_sheet.py` | builds 1280×720 white-padded reference sheets from 1–4 images |
| `songs/_selftest/` | format example: `world.txt` (line 1 = place clause), a structured V2c shot, a no-ref I0 shot, `shots.csv` |

`python comfy\batch_runner.py --song songs\_selftest --hosts http://x --dry-run` prints the assembled prompts with no
network — run it once to see the block order.

## 2 · Part A — network volume (once)
1. RunPod → Storage → new **network volume**, 60 GB, same datacenter as the stopped pod `99nzy9hhow6slc` (a volume is
   datacenter-bound; pick the DC that has H100/A100 availability).
2. Start the stopped pod with the volume attached at `/workspace` **or** start a fresh ComfyUI pod with the volume and
   copy the four model files into `/workspace/ComfyUI/models/...` (from the old pod: `runpodctl send/receive`, or
   re-download — 40 GB on a pod is ~10–20 min). Verify sizes byte-exact as in 4d.
3. Also put `comfy/`, `prompts/`, `docs/PROMPT-PLAYBOOK.md`, `songs/` on the volume (`/workspace/wan/`), so the
   runner can run on the pod itself against `http://127.0.0.1:8188` — no proxy, no 403s, no laptop dependency.
4. Confirm: stop pod → start a *new* pod with the volume → ComfyUI sees the models (`/object_info/UNETLoader` lists
   `wan2.1_vace_14B_fp16.safetensors`) within ~2 min of boot. Record the boot-to-ready time.
5. Delete the old pod `99nzy9hhow6slc` once the volume is verified (its 50 GB disk was the only reason to keep it).

## 3 · Part B — Mazhai shot list in the new format (Fable's job, but CC checks it)
Fable will write `songs/mazhai/` (world.txt from the runsheet WORLD + INTERIOR clause, the 12 shots as structured
files, refs from `outputs\vace\refs\`). Until it lands, use `songs/_selftest` to prove the plumbing.

## 4 · Part C — prove the batch on the pod
```
cd /workspace/wan
python comfy/batch_runner.py --song songs/_selftest --hosts http://127.0.0.1:8188 --dry-run
python comfy/batch_runner.py --song songs/_selftest --hosts http://127.0.0.1:8188 --seed 30313 \
    --max-minutes 60 --stop-cmd "runpodctl stop pod $RUNPOD_POD_ID"
```
(`runpodctl` on the pod needs the API key in env; if it is not available on the pod, run the batch from the laptop
against the proxy URL with `--stop-cmd "runpodctl stop pod <id>"` there — both paths are supported.)
Expect: I0 (no ref, text-to-video) and V2c (Minnu, structured prompt with ATMOSPHERE repeated) done in ~5 min each on
a warm model, `songs/_selftest/out/` populated, strips in `out/_qc/`, CSV statuses `done`, pod stopped by the runner.
Bring `out/` to the laptop. **Report the V2c strip — Fable checks whether the rain is back.**
If the rain is still missing at 6 steps / cfg 1.0: rerun V2c only with `cfg` 1.5 in the CSV (`--retry-failed` after
clearing its status) and report both.

## 5 · Known limitation, deferred to Phase 5
Core `SaveVideo` has no quality control (verified in ComfyUI source: inputs are video / filename_prefix / format /
codec) — the ~1.5 Mbps encode stands for now. Phase 5's post step (RIFE 16→30 fps + 2× upscale) will take a PNG
frame sequence from ComfyUI instead and encode the 1080p master itself at crf 16; that is where the quality lives.

## 6 · Commit
```
git add comfy/ docs/ songs/_selftest CC-DISPATCH-phase4d-comfy-pod-2026-09-22.md CC-DISPATCH-phase4e-batch-2026-09-22.md outputs/vace/pod/_qc
git commit -m "phase4d/4e: ComfyUI VACE driver + batch runner, shot-list spec, prompt playbook, 4d QC"
git push
```
(`outputs/vace/pod/_qc` PNGs are small and are the evidence for the 4d decision; the mp4s stay untracked.)
