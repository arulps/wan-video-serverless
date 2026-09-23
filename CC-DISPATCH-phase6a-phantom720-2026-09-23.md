# CC-DISPATCH — Phase 6a: commit the multi-ref work, install RIFE, Phantom at 720p (2026-09-23)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC. Three parts, in order. **Budget: Part C ≤ 75 min pod
time (~$2 A100 secure / ~$3 H100), hard stop 90 min; Parts A and B are $0.** Same rules as the queue: one pod, stopped and
removed before reporting; no retakes, no extra seeds; never print `.env` values; edit `shots.csv` cells, never restore it.

## 0 · Decision this dispatch serves (Arul, 2026-09-23)
After `queue/2026-09-23` (Phantom held two look-alike children 3/3, VACE 2/3 with separate refs, ~1/2 with one sheet) Arul
decided: **no VACE — Phantom for every row** (character reference quality, and colours shift between engines). Everything so
far was 832×480; Part C is the bounded check at production size before a whole song is planned on Phantom. Fable's per-song
estimate on Phantom: ~$10–18 at 720p (A100 secure), depends on how many rows need full sampling.

## Part A — commit today's work ($0)
Everything from the queue is uncommitted. If `.git\index.lock` exists (0 bytes, stale), delete it first.
```
python comfy\batch_runner.py --song songs\_ab4-2026-09-23 --hosts http://x --dry-run            (6 rows, all "2 SEPARATE references")
python comfy\batch_runner.py --song songs\_ab5-2026-09-23-phantom720 --hosts http://x --dry-run  (3 rows; T08/T07 "2 SEPARATE"; REF MISSING for minmini-sideA is EXPECTED until Part C step 1)
python comfy\batch_runner.py --song songs\twinkle-twinkle --hosts http://x --dry-run             (4 pending, unchanged)
python -m py_compile comfy\custom_nodes\wan_vace_multiref.py comfy\run_comfy.py comfy\batch_runner.py scripts\build_song_refs.py
git status   -- confirm NO .env, logs.txt, nil, songs/*/out/, outputs/upscale-test-*/*.mp4, outputs/cutouts in the add set
git add comfy/custom_nodes/wan_vace_multiref.py comfy/phantom_s2v_api.json comfy/run_comfy.py comfy/batch_runner.py ^
        scripts/pod_bootstrap.sh scripts/build_song_refs.py docs/PROMPT-PLAYBOOK.md docs/SHOT-LIST-SPEC.md ^
        songs/_ab4-2026-09-23/README.md songs/_ab4-2026-09-23/shots.csv songs/_ab4-2026-09-23/style.txt songs/_ab4-2026-09-23/characters.txt songs/_ab4-2026-09-23/world.txt ^
        songs/_ab5-2026-09-23-phantom720 songs/twinkle-twinkle/refs/minnu-body-16x9.png songs/twinkle-twinkle/refs/mintu-front-16x9.png ^
        queue/2026-09-23 CC-DISPATCH-phase4k-twinkle-retakes-2026-09-23.md CC-DISPATCH-phase5a-upscale-2026-09-23.md CC-DISPATCH-phase6a-phantom720-2026-09-23.md ^
        songs/twinkle-twinkle/REVIEW-480p-2026-09-23.md songs/twinkle-twinkle/shots.csv songs/twinkle-twinkle/shots/T05.txt songs/twinkle-twinkle/shots/T09b.txt songs/twinkle-twinkle/shots/T10.txt songs/twinkle-twinkle/shots/T19.txt
git commit -m "multi-reference: Phantom-Wan-14B engine + VACE multi-ref node; two-child identity A/B (queue 2026-09-23)

runner: engine column (vace|phantom), ref = a.png|b.png separate reference images, per-engine workflows;
run_comfy: ImageBatch chain for N refs, node 9 switched to WanVaceToVideoMultiRef for >1 refs on VACE.
comfy/custom_nodes/wan_vace_multiref.py: VACE reference conditioning that encodes every image of the
batch on its own (core WanVaceToVideo uses only reference_image[:1]). comfy/phantom_s2v_api.json:
WanPhantomSubjectToVideo workflow (latent = output slot 3).
pod_bootstrap: installs custom nodes + checks /object_info, python||python3, model-get/model-push
(Phantom is on R2, manifest 5 files), out-push ships comfyui/batch logs to out/_debug/.
Result (songs/_ab4-2026-09-23, 832x480): Phantom held Minnu+Mintu 3/3, VACE separate refs 2/3.
Decision: Phantom for every row. queue/2026-09-23 = the overnight CC queue record ($4.27).
twinkle: 480p review + 4 retake edits (phase 4k, not yet run)."
git push
```
(`queue/2026-09-23/*.verdict` and `.done` markers are part of the record — commit them. `songs/_ab4-2026-09-23/out/` stays
untracked by `.gitignore`.)

## Part B — RIFE on the laptop ($0)
1. Download the latest `rife-ncnn-vulkan` Windows release zip from `https://github.com/nihui/rife-ncnn-vulkan/releases`
   (the `-windows.zip` asset); unzip to `C:\tools\rife-ncnn-vulkan\`; add that folder to the **user** PATH; open a new shell;
   `where rife-ncnn-vulkan` must print the exe. Report the version/asset name.
2. Find the interpreter phase 5a used (it reported `device: cuda`; item-03's `py` reported `cpu`):
   `py -0p` lists every Python; for each candidate run `<python> -c "import torch;print(torch.__version__, torch.cuda.is_available())"`
   and report the table. Use the one that prints `True` for step 3 — call it `PYCUDA` below.
3. Re-run the T16 interpolation test on CUDA with RIFE now available:
   ```
   <PYCUDA> scripts\upscale_video.py songs\twinkle-twinkle\out\T16-seed30313-s6.mp4 outputs\upscale-test-2026-09-23\T16-4k-30-rife.mp4 --fps 30
   ffmpeg -y -i outputs\upscale-test-2026-09-23\T16-4k-30-rife.mp4 -vf "select='between(n,60,63)',crop=1200:900:1300:500,tile=4x1" -vsync 0 -frames:v 1 outputs\upscale-test-2026-09-23\_qc\T16-4k-30-rife-crop60-63.png
   ```
   Report the sidecar's `interpolation` (must say rife), `device` (must be cuda), `seconds`, and the PNG path. Fable compares it
   with `_qc\T16-4k-30-crop60-63.png` (the minterpolate one, star edge smeared on frame 61).

## Part C — Phantom at 1280×720, three rows (`songs/_ab5-2026-09-23-phantom720/`)
1. Laptop: `python scripts\build_song_refs.py --song twinkle-twinkle --no-cut` → builds the new `minmini-sideA-16x9.png`
   (cutout already exists). Dry-run `_ab5` again: 3 rows, **no REF MISSING**. `bash scripts\pod_bootstrap.sh wan-push`.
2. Fresh pod (H100 if community has it, else A100 80 GB secure — same fallback order as the queue), R2 env vars, `pull`.
   `pull` must show the Phantom model verified from R2 (**no `model-get`** this time — it is in the manifest) and
   `node OK WanPhantomSubjectToVideo`. If ComfyUI needs the custom-node restart, do it (`pkill -f "main.py --listen"`; rerun `pull`).
3. Cheap row first (CSV order already is), logs preserved:
   ```
   cd /workspace/wan
   python3 comfy/batch_runner.py --song songs/_ab5-2026-09-23-phantom720 --hosts http://127.0.0.1:8188 --seed 30313 --dry-run
   python3 comfy/batch_runner.py --song songs/_ab5-2026-09-23-phantom720 --hosts http://127.0.0.1:8188 --seed 30313 \
       --max-minutes 70 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/_ab5-2026-09-23-phantom720; runpodctl stop pod $RUNPOD_POD_ID" 2>&1 | tee /workspace/batch_ab5.log
   ```
   Expect T04 ~4–5 min, T08 and T07 ~25 min each on the A100 (about 40 % less on an H100). If T04 fails (first row), Ctrl-C the
   runner (it runs the stop-cmd) and report — do not let the full rows spend on a broken setup. Watch VRAM in the log: 720p full
   sampling on Phantom fp16 is the first time we load it at this size; an OOM on T08 is a finding, not a retry.
4. Confirm stopped → remove pod. Pull `out/` (+ `_debug/`) to the laptop.
5. Report (`CC-REPORT-phase6a.md` in the repo root, or paste): pod id/GPU/rate, `BOOT-TO-READY`, per-row wall s, **full Windows
   paths** of the 3 mp4 + strips + json, `grep -c "lora key not loaded" comfyui.log`, peak VRAM if the log shows it, $ for the
   part and the total. **Do not judge the clips** — Fable frame-checks: T04 face on-model at 720p; T08 TV head / antennae / wings /
   lantern held, no orange body; T07 two distinct children with closed mouths.

## What Fable decides from Part C
- All three hold → the next song is planned on Phantom (Arul writes the beats, Fable drafts rows for his sign-off), budget
  ~$10–18 at 720p; the 4K/30 fps pass runs on the laptop with RIFE.
- T08 (mascot) fails → mascot shots get a third reference view and one more seed before anything else changes.
- T07 fails at 720p but passed at 480p → two-child rows render at 832×480 and go through the 4K upscaler (it held T16 well).
