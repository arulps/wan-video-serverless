# CC-DISPATCH — Phase 5a: 720p → 4K upscale utility, first real test on an OpenArt clip (2026-09-23)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC. **Budget: 20 min pod time on the cheapest GPU
that has ≥ 16 GB (RTX 4090 ≈ $0.35/h, L40S/A100 fine) ≈ $0.15–0.50.** No Wan models needed — this pod does NOT
run `pod_bootstrap.sh pull`; it only needs torch + ffmpeg (any PyTorch template) and the 16 MB Real-ESRGAN weights,
which the script downloads itself. Self-stop / delete the pod when done. Context: OpenArt is production this week;
this utility makes its 720p output into 4K/30 fps masters, and later takes our own 720p keepers the same way.

## 1 · What Fable wrote (CPU smoke-tested end to end: decode → upscale → interpolate → encode + sidecar JSON)
`scripts/upscale_video.py` — self-contained (no basicsr/realesrgan packages; the network is in the file):
```
python scripts\upscale_video.py in.mp4 out-4k.mp4                  # 3840x2160, source fps, h264 crf 16, audio copied
python scripts\upscale_video.py in.mp4 out.mp4 --fps 30             # + interpolation (rife-ncnn-vulkan if on PATH, else ffmpeg minterpolate)
python scripts\upscale_video.py in.mp4 out.mp4 --height 1080        # 1080p
python scripts\upscale_video.py in.mp4 out.mp4 --codec hevc         # HEVC master
python scripts\upscale_video.py in.mp4 out.mp4 --limit 24           # first 24 frames only (timing test)
```
Model: `realesr-animevideov3` (Real-ESRGAN's animation-video model, ×4 then lanczos to the exact target). Writes
`out.mp4.json` with source/output probe, per-stage seconds, device.

## 2 · Steps
1. Laptop, no GPU, 2 minutes: `python scripts\upscale_video.py <any 480p clip in songs\twinkle-twinkle\out> C:\tmp\smoke.mp4 --height 1080 --limit 8 --device cpu`
   → must print `DONE … 1920x1080`. (Needs `pip install torch numpy pillow` if missing — CPU torch is fine.)
2. Pick the test clip: **`C:\Channel Contents\MinMiniKids\songs\Mazhai- rain rain go away\`** — the OpenArt 720p clip
   `01_I1_opening-backview…` (the first Mazhai shot, characters from behind, rain on glass: fine detail to judge).
   Copy it to the pod with the script (runpodctl send / scp).
3. On the pod (GPU):
   ```
   pip install -q numpy pillow          # torch is in the template
   python upscale_video.py 01.mp4 01-4k.mp4                    # 4K, source fps
   python upscale_video.py 01.mp4 01-4k-30.mp4 --fps 30        # 4K + 30 fps (minterpolate unless rife-ncnn-vulkan is installed)
   python upscale_video.py 01.mp4 01-1080.mp4 --height 1080
   ```
   Optional if quick: `apt-get install -y rife-ncnn-vulkan` is NOT a package — skip RIFE this round; minterpolate is the
   baseline, RIFE is the follow-up if the motion looks smeared.
4. Bring the three outputs + their `.json` sidecars back to
   `C:\Projects\opencode\video_image\outputs\upscale-test-2026-09-23\` and report the **full paths**, the per-stage
   seconds from the JSONs (this gives the $/song number: a 151 s song ≈ 2,400 frames), GPU used, and file sizes.
   Delete the pod.
5. Commit `scripts/upscale_video.py` + this dispatch: `scripts: upscale_video.py — 720p→4K/30fps master utility (Real-ESRGAN animevideov3 + interpolation)`.

## 3 · What Fable checks
Frame crops of source vs 4K (edges, the rain streaks, skin gradients — animevideov3 can over-smooth); 30 fps motion
on the camera move (minterpolate ghosting → RIFE next). Then the $/song number decides whether upscaling runs on a
pod per song (~$0.30 expected) or on Arul's machine overnight.
