# CC-REPORT — Phase 6c: YT Short L01 "Peekaboo", 480p vs 720p × quick vs full (2026-09-28)

**Result: A–E done end to end. 4/4 rows rendered, 4/4 upscaled to vertical 4K30, comparisons built and copied, committed `106906b`. Pod $1.38.**

## Part A — preflight
- Dry-run `songs\shorts-loops`: 4 rows, ~498 tokens each, no REF MISSING, no OVER BUDGET.
- **RunPod balance $22.56** (above the $5 stop).
- **Pods:** one pod already existed. It was not ours, so it was left alone:
  - `ih3eiv5oyprlh6` **`oviyan-blender-dev-3d1b`** (oviyan render node image), RUNNING, $0.74/h, up ~92 min at 04:00 UTC.
  - At ~06:00 UTC `pod list` was empty, so someone else stopped or removed it.
- `wan-push` done.

## Part B — render
- **Pod `rtf1wcj5o7oks5`:** A100-SXM4-80GB, community cloud, **$1.39/h** (H100 community: no instances).
  - Created 04:02:33 UTC. Stopped itself at 05:02:14 UTC via the stop-cmd, after out-push.
  - Deleted after confirming `EXITED`; `pod get` now 404.
  - **~59.7 min ≈ $1.38.** The laptop backstop (05:32) was not needed.
- **`pull`:** the env import worked (no "missing env").
  - First pull: `BOOT-TO-READY: models 441 s, total 450 s`. Phantom was verified from R2.
    `WanVaceToVideoMultiRef` was MISSING (the template's ComfyUI was already running).
  - After one restart: `BOOT-TO-READY: models 6 s, total 27 s`, all three nodes OK.
- The batch ran in the foreground of a tmux session, with the literal pod id in the stop-cmd.

| row | size | mode | wall s | expected |
|---|---|---|---|---|
| L01_480q | 480×832 | distilled 6 | **90.0** | ~2 min |
| L01_720q | 720×1280 | distilled 6 | **230.1** | ~4 min |
| L01_480f | 480×832 | full 30 | **560.3** | ~11 min |
| L01_720f | 720×1280 | full 30 | **2150.8** | ~39 min |

- The runner reported 50.5 GPU-min. `grep -c "lora key not loaded" comfyui.log` → **0**. No traceback, no OOM.
- `shots.csv`: the four `status` cells were set to `done`, matching the pod's copy (cells edited, not restored).

## Part C — upscale to vertical 4K @ 30 fps (laptop, Intel Iris Xe via Vulkan)
- The two quick clips were copied straight from the pod (same bytes as R2 later) and upscaled while the full rows rendered.
- My first loop's shell quoting wrote both quick outputs to a literal `4K$c-4K30.mp4`. Each finished file was renamed to its
  correct name before the next one overwrote it, and the `dst` field in each sidecar was corrected. Both files are complete.

| clip | output | backend | interpolation | seconds (decode / upscale incl. RIFE / encode) | Real-ESRGAN only |
|---|---|---|---|---|---|
| L01_480q | 2216×3840 @ 30, 152 f | ncnn | rife-ncnn-vulkan rife-v4.6 81->152 frames | 1.6 / 1272.2 / 176.1 | 285.7 s (3.53 s/frame) |
| L01_720q | 2160×3840 @ 30, 152 f | ncnn | rife-ncnn-vulkan rife-v4.6 81->152 frames | 2.6 / 1613.3 / 87.6 | 727.5 s (8.98 s/frame) |
| L01_480f | 2216×3840 @ 30, 152 f | ncnn | rife-ncnn-vulkan rife-v4.6 81->152 frames | 1.2 / 1089.9 / 97.2 | 305.7 s (3.77 s/frame) |
| L01_720f | 2160×3840 @ 30, 152 f | ncnn | rife-ncnn-vulkan rife-v4.6 81->152 frames | 1.5 / 1391.6 / 84.7 | 608.7 s (7.51 s/frame) |

No clip failed. Each upscale took ~20–28 min end to end.

## Part D — comparison files
- Grid (frame 40, native renders): 1480×2560.
  - Top row: quick 480 | quick 720.
  - Bottom row: full 480 | full 720.
- Side-by-side videos: 2188×1920 each.
  - Left: 480p→4K. Right: 720p→4K.
- Mid-frame 4K stills (frame 75): 2216×3840 for 480f, 2160×3840 for 720f.
- **Copied** (not moved) to `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\`: the four 4K mp4s and the two side-by-sides.

## Part E — commit
- **`106906b`** "shorts: songs/shorts-loops (9:16 loop Shorts on Phantom), L01 Peekaboo 480p/720p x quick/full A/B [skip ci]".
- Pushed `eb9250f..106906b`, and no deploy run started.
- The add set was exactly the dispatch list: `minnu-body-9x16.png` via `-f`, with no `.env`, `out/` or `outputs/`.
- `songs\_ab6-2026-09-27-setplate\REVIEW-2026-09-27.md` (Fable's) is still untracked; it was not in this dispatch's list.

## Paths
Native renders — `C:\Projects\opencode\video_image\songs\shorts-loops\out\`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L01_480q-seed30313-s6.mp4` · `...\out\L01_480q-seed30313-s6.json` · `...\out\_qc\L01_480q-strip.png`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L01_720q-seed30313-s6.mp4` · `...\out\L01_720q-seed30313-s6.json` · `...\out\_qc\L01_720q-strip.png`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L01_480f-seed30313-s30.mp4` · `...\out\L01_480f-seed30313-s30.json` · `...\out\_qc\L01_480f-strip.png`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\L01_720f-seed30313-s30.mp4` · `...\out\L01_720f-seed30313-s30.json` · `...\out\_qc\L01_720f-strip.png`
- Logs: `C:\Projects\opencode\video_image\songs\shorts-loops\out\_debug\batch_6c.log`, `...\out\_debug\comfyui.log`

Upscaled — `C:\Projects\opencode\video_image\songs\shorts-loops\out\4K\`
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\4K\L01_480q-seed30313-s6-4K30.mp4` (+ `.mp4.json`)
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\4K\L01_720q-seed30313-s6-4K30.mp4` (+ `.mp4.json`)
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\4K\L01_480f-seed30313-s30-4K30.mp4` (+ `.mp4.json`)
- `C:\Projects\opencode\video_image\songs\shorts-loops\out\4K\L01_720f-seed30313-s30-4K30.mp4` (+ `.mp4.json`)

Comparisons
- Grid: `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L01-grid-f40.png`
- Side-by-side: `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L01-full-480vs720-4K.mp4`, `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L01-quick-480vs720-4K.mp4`
- 4K stills: `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L01_480f-4K-f75.png`, `C:\Projects\opencode\video_image\songs\shorts-loops\out\_qc\L01_720f-4K-f75.png`

Review copies — `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\L01_480q-seed30313-s6-4K30.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\L01_720q-seed30313-s6-4K30.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\L01_480f-seed30313-s30-4K30.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\L01_720f-seed30313-s30-4K30.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\L01-full-480vs720-4K.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\L01-quick-480vs720-4K.mp4`

## Cost
Pod $1.38. Parts A, C, D and E $0. **Total: $1.38** (budget ≤ $1.75).

## Not judged
Fable checks:
- Minnu on-model at each size.
- The hide → pop → hide actually happens.
- The last frame is close enough to the first to loop.
- 480p→4K vs 720p→4K detail on the face, hair, hands and the curtain edge.
