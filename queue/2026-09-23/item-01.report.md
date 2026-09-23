# item-01 report — VACE separate references (WanVaceToVideoMultiRef), T17 + T07 at 480p

## Pod
- id `v3tenww5xyms9f`, name `queue-0923-item1`, **A100-SXM4-80GB**, community cloud, $1.39/h (H100 had **no community-cloud
  capacity** at request time — `podFindAndDeployOnDemand` returned `SUPPLY_CONSTRAINT` for `NVIDIA H100 80GB HBM3`; fell back
  to A100 per the item's own instruction).
- Created fresh (not reused) because the existing stopped H100 pod (`zpa248yp3ghrzp`) only has 60 GB container disk, not the
  100 GB this item specifies.
- Rented 05:28:30 UTC → stopped ~06:10:25 UTC = **41.9 min uptime ≈ $0.97**.
- Pod **terminated** (`runpodctl`/API `podTerminate`) after confirming stopped, per step 5.

## Two process issues, both caught and fixed before any GPU batch ran
1. I first fetched `pod_bootstrap.sh` via `curl` from the GitHub `main` branch — but this item's script changes
   (`install_custom_nodes`, `model-get`, `model-push`) are **uncommitted, laptop-only** per the item's own "nothing
   committed" note. Caught it because the first `pull` produced no `node OK`/`node MISSING` lines at all. Re-copied
   the correct local `scripts/pod_bootstrap.sh` via `scp` and re-ran `pull`.
2. That re-run then showed ComfyUI's `nohup python main.py ...` failing instantly: **`nohup: failed to run command
   'python': No such file or directory`** — this pod's image has no `python` → `python3` alias. Created
   `/usr/local/bin/python -> /usr/bin/python3` and started ComfyUI manually; the same `pull` invocation's
   `wait_ready` loop picked it up normally afterward.
3. The SSH connection to this pod's host dropped silently twice during long-running commands (once right after a
   `pkill`, once mid-batch during the 720s+ full-sampling jobs) — no error on the local end, just the stream going
   quiet. Both times the remote process (verified via a fresh connection) was alive and unaffected; I switched to
   polling `shots.csv`'s `status` column directly over fresh SSH connections rather than relying on one long-lived
   tail. No GPU time or shots were lost either time.

## Pull result
```
[05:38:29] custom nodes installed: wan_vace_multiref.py
[05:38:29] starting ComfyUI
[05:43:46] ComfyUI ready on :8188 (UNETLoader lists the VACE model)
[05:43:46]   node OK   WanVaceToVideoMultiRef
[05:43:46]   node OK   WanPhantomSubjectToVideo
[05:43:46]   node OK   ImageBatch
[05:43:46] BOOT-TO-READY: models 5 s, total 327 s
```
(models 5s because the first, discarded pull attempt already cached them; total 327s includes the ComfyUI-restart
detour above, not just a clean boot.)

## Batch result — 3/3 done, 0 failed, 25.7 GPU-minutes (runner-reported)
Note: the runner processed `--only T17_vsep_d,T17_vsep,T07_vsep` in **CSV row order**, not the order listed in
`--only` — so the two expensive full-sampling rows (`T17_vsep`, `T07_vsep`) ran *before* the cheap distilled row
(`T17_vsep_d`), not after it as the item's "cheap row first" plan intended. Flagging this since it means the
fail-fast validation the item wanted didn't actually happen — worth knowing for future `--only` lists.

| row | status | wall_s | mp4 | qc strip | json |
|---|---|---|---|---|---|
| T17_vsep | done | 730.2 | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T17_vsep-seed30313-s30.mp4` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\_qc\T17_vsep-strip.png` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T17_vsep-seed30313-s30.json` |
| T07_vsep | done | 720.3 | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T07_vsep-seed30313-s30.mp4` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\_qc\T07_vsep-strip.png` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T07_vsep-seed30313-s30.json` |
| T17_vsep_d | done | 90.0 | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T17_vsep_d-seed30313-s6.mp4` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\_qc\T17_vsep_d-strip.png` | `C:\Projects\opencode\video_image\songs\_ab4-2026-09-23\out\T17_vsep_d-seed30313-s6.json` |

No `EXECUTION ERROR`, no `Traceback`, on any of the three rows.

**QC strip observations, factually (not the pass/fail call — that's Fable's):**
- **T07_vsep** (full, "both children head to knees, side by side"): both children clearly visible and distinct in
  all 5 frames — pigtailed girl in violet dungarees on the left, boy in green dinosaur shirt/blue shorts on the
  right. No hair-bleed, no merging.
- **T17_vsep_d** (distilled, "both lying on the mat"): both children also clearly visible and distinct in all 5
  frames — same correct identities as above, lying side by side.
- **T17_vsep** (full, same "both lying on the mat" composition as T17_vsep_d): only **one** child is visible in any
  of the 5 sampled frames (dark hair, green/striped top, lying on the mat near the door) — the second child does not
  appear distinctly. This is the same shot composition that worked in the distilled version, so the miss looks
  shot/seed-specific rather than "full sampling is worse" — 2/3 rows show clean separate-reference identity, 1/3
  does not.

## Cost so far this queue: **$0.97** (of the $6 hard limit)

## Known gap (my mistake, reporting rather than hiding it)
Item-01 step 6 asks for `grep -c "WanVaceToVideoMultiRef" /workspace/comfyui.log` **captured before the pod stops**.
I terminated the pod (per step 5) before running that grep — the container disk (and the log with it) is gone, so
this number cannot be recovered. During live troubleshooting I did view large stretches of `comfyui.log` (while
diagnosing the two issues above and confirming `T17_vsep_d`'s completion) and saw no `Error`/`Traceback` lines in
any of it, only normal `KSampler` progress and `Prompt executed` lines — but that was not a systematic grep across
the whole file, so I'm not presenting it as equivalent to the requested count.

## stop-cmd
`--stop-cmd exit code: 0`. `out/ pushed -> r2:minmini-wan/songs/_ab4-2026-09-23/out/` confirmed. Pod `desiredStatus`
verified `EXITED` via the RunPod API before terminating.
