# CC-DISPATCH — Phase 6c: YT Short L01 "Peekaboo", 480p vs 720p (+ quick vs full), upscaled to vertical 4K (2026-09-27)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine). Parts A → E run **in one go, end to end**: as soon as the pod is removed and `out/`
is on the laptop, start the upscaling (Part C) yourself, then D and E. Do not stop and wait for Fable between parts;
stop early only on a failure named below.
**Budget: Part B ≤ 75 min pod time (~$1.75 A100 community / ~$2.00 secure), `--max-minutes 70`, hard stop 90 min.
Parts A, C, D, E are $0 (laptop).**
Standing rules: one pod, fresh from R2, stopped and removed before reporting; no retakes, no extra seeds; never print
`.env` values; edit `shots.csv` cells, never restore it from git; report **full Windows paths** of everything produced.

## 0 · Why (Arul, 2026-09-27)
First YouTube Short from `C:\Channel Contents\MinMiniKids\YT Shorts\LOOP-SHORTS-RUNSHEET.md` (L01 Peekaboo, Minnu,
W1 living room, 9:16, 5 s loop), made on our Phantom pipeline instead of OpenArt. Arul wants 480p and 720p side by
side after upscaling, to settle the resolution question on a real shot. Fable added the quick (distilled) versions
of both sizes: they cost ~$0.12 together and tell us whether this kind of shot needs full sampling at all.
Note for the comparison: the same seed at a different size gives a different composition, so compare cleanliness and
detail (face, hair, hands, curtain edge), not identical pixels.

## 1 · On disk (Fable; dry-run verified on the laptop: 4 rows, ~498 tokens, no REF MISSING, no OVER BUDGET)
`songs/shorts-loops/` (new, the folder for all 20 loop Shorts):
| file | content |
|---|---|
| `style.txt` | runsheet STYLE, 9:16, + the anti-painterly/anti-choppy line that fixed the song clips |
| `world.txt` | line 1 place clause; W1 living room, dry version, trimmed to fit 512 tokens |
| `characters.txt` | Minnu, Mintu lock lines (same as twinkle) |
| `negative.txt` | runsheet NEGATIVE + camera-move terms + the proven style/motion negatives; no night terms; "open mouth" NOT negated (the shot wants a big open smile) |
| `shots/L01.txt` | structured shot (ATMOSPHERE/ANGLE/SHOT/POSE/MOTION/NEGATIVE) from the runsheet scene, loop clause in ANGLE + MOTION |
| `refs/minnu-body-9x16.png` | 720×1280, Minnu `body-relaxed-front.png` from the character bible on white (`make_ref_sheet.py --size 720x1280 --margin 60`) |
| `shots.csv` | 4 rows, seed 30313, Phantom, in cost order: `L01_480q` (480x832 quick), `L01_720q` (720x1280 quick), `L01_480f` (480x832 full), `L01_720f` (720x1280 full) |

## Part A — preflight ($0)
```
python comfy\batch_runner.py --song songs\shorts-loops --hosts http://x --dry-run     -> 4 rows, ~498 tokens, no REF MISSING, no OVER BUDGET
```
Report the RunPod balance; if it is under $5, stop and tell Arul. Confirm no pods exist. `bash scripts\pod_bootstrap.sh wan-push`.

## Part B — render on a pod (≤ 75 min)
1. Fresh pod: A100 80 GB community → A100 secure fallback (H100 if community has one). R2 env vars in the console; copy
   `scripts/pod_bootstrap.sh`; `bash pod_bootstrap.sh pull`; if a custom node says MISSING, restart ComfyUI once
   (`pkill -f "main.py --listen"`; `pull` again) until all three nodes say OK.
2. Run it in the foreground of a **tmux** session on the pod (as in 6b), literal pod id in the stop-cmd:
   ```
   cd /workspace/wan
   python3 comfy/batch_runner.py --song songs/shorts-loops --hosts http://127.0.0.1:8188 --seed 30313 --dry-run
   python3 comfy/batch_runner.py --song songs/shorts-loops --hosts http://127.0.0.1:8188 --seed 30313 \
       --max-minutes 70 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/shorts-loops; runpodctl stop pod <POD_ID>" 2>&1 | tee /workspace/batch_6c.log
   ```
   Expected on an A100: L01_480q ~2 min (incl. first model load), L01_720q ~4 min, L01_480f ~11 min, L01_720f ~39 min.
   Early stop: `touch /workspace/wan/songs/shorts-loops/STOP` from a second session. If the first row fails, STOP and report.
   Laptop-side backstop: stop the pod yourself at pod-start + 90 min if it is still running.
3. Confirm the pod stopped → delete it. Pull `songs/shorts-loops/out/` (+ `_debug/`) to the laptop.

## Part C — upscale all four to vertical 4K @ 30 fps on the laptop ($0, ~20 min per clip, ~80 min total) — starts automatically after Part B
Vertical 4K = height 3840. Run one at a time:
```
cd songs\shorts-loops\out
foreach ($c in "L01_480q-seed30313-s6","L01_720q-seed30313-s6","L01_480f-seed30313-s30","L01_720f-seed30313-s30") {
  powershell -ExecutionPolicy Bypass -File ..\..\..\scripts\upscale.ps1 "$c.mp4" -Dst "4K\$c-4K30.mp4" -Height 3840 -Fps 30
}
```
(`mkdir 4K` first. PowerShell. If one clip fails, note it and continue with the next; do not rerun the pod.) Each sidecar must say `backend: ncnn` and `rife-ncnn-vulkan rife-v4.6 81->152 frames`. Expected sizes:
the 720x1280 clips → 2160x3840; the 480x832 clips → 2216x3840 (832 is not exactly 16:9 of 480; fine for comparison,
the delivery crop comes later).

## Part D — comparison files ($0)
In `songs\shorts-loops\out\`:
```
mkdir _qc
# 1) 2x2 grid of the native renders, frame 40 (top: quick 480 | quick 720, bottom: full 480 | full 720)
ffmpeg -y -i L01_480q-seed30313-s6.mp4 -i L01_720q-seed30313-s6.mp4 -i L01_480f-seed30313-s30.mp4 -i L01_720f-seed30313-s30.mp4 -filter_complex "[0]select=eq(n\,40),scale=-2:1280,pad=740:1280:(ow-iw)/2:0:white[a];[1]select=eq(n\,40),scale=-2:1280,pad=740:1280:(ow-iw)/2:0:white[b];[2]select=eq(n\,40),scale=-2:1280,pad=740:1280:(ow-iw)/2:0:white[c];[3]select=eq(n\,40),scale=-2:1280,pad=740:1280:(ow-iw)/2:0:white[d];[a][b][c][d]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0" -frames:v 1 _qc\L01-grid-f40.png
# 2) side-by-side videos of the 4K versions (left 480p→4K, right 720p→4K), shown at 1920 high
ffmpeg -y -i 4K\L01_480f-seed30313-s30-4K30.mp4 -i 4K\L01_720f-seed30313-s30-4K30.mp4 -filter_complex "[0]scale=-2:1920[a];[1]scale=-2:1920[b];[a][b]hstack" -c:v libx264 -crf 16 -pix_fmt yuv420p _qc\L01-full-480vs720-4K.mp4
ffmpeg -y -i 4K\L01_480q-seed30313-s6-4K30.mp4 -i 4K\L01_720q-seed30313-s6-4K30.mp4 -filter_complex "[0]scale=-2:1920[a];[1]scale=-2:1920[b];[a][b]hstack" -c:v libx264 -crf 16 -pix_fmt yuv420p _qc\L01-quick-480vs720-4K.mp4
# 3) full-resolution 4K stills at the mid frame, for face detail
ffmpeg -y -i 4K\L01_480f-seed30313-s30-4K30.mp4 -vf "select=eq(n\,75)" -frames:v 1 _qc\L01_480f-4K-f75.png
ffmpeg -y -i 4K\L01_720f-seed30313-s30-4K30.mp4 -vf "select=eq(n\,75)" -frames:v 1 _qc\L01_720f-4K-f75.png
```
Then **copy** (not move) the four `4K\*.mp4` files and the two side-by-side videos to
`C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\` (create it), so Arul can review them next to the runsheet.

## Part E — commit ($0)
```
git status   -- confirm NO .env, logs.txt, nil, out/, outputs/ in the add set
git add songs/shorts-loops/shots.csv songs/shorts-loops/style.txt songs/shorts-loops/world.txt songs/shorts-loops/characters.txt songs/shorts-loops/negative.txt songs/shorts-loops/shots/L01.txt CC-DISPATCH-phase6c-shorts-L01-2026-09-27.md
git add -f songs/shorts-loops/refs/minnu-body-9x16.png
git commit -m "shorts: songs/shorts-loops (9:16 loop Shorts on Phantom), L01 Peekaboo 480p/720p x quick/full A/B [skip ci]"
git push
```
(The runner writes `status` into `shots.csv`; commit it as it is after the run.)

## Report — `CC-REPORT-phase6c.md` in the repo root
Pod id / GPU / rate; `pull` lines; per-row wall seconds; upscale sidecar values (backend, interpolation, seconds) per
clip; full Windows paths of: the 4 native mp4 + json + strips, the 4 upscaled mp4 + json, the grid PNG, the two
side-by-side videos, the two 4K stills, and the `YT Shorts\renders\L01\` copies; $ for the pod; commit hash.
**Do not judge the clips** — Fable checks: Minnu on-model at each size; hide → pop → hide actually happens; last frame
close enough to the first to loop; 480p→4K vs 720p→4K detail on face, hair, hands and the curtain edge.
