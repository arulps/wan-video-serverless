# CC-REPORT — Phase 6e: Wan 3.0 through Alibaba Model Studio (engine=wan3), first test (2026-09-28)

Run as CC queue `queue\2026-09-28-wan3-setup` (items 01–03; the per-item reports are in that folder).
**Result: 3/3 Twinkle rows rendered through the API, upscaled to 4K, comparisons built and copied. L01_w3 was skipped
(no keyframe). Estimate $1.50 at list price.** No pod, no RunPod calls.

## A — prerequisites
- **A1:** `credentials present: True`. The region line `DASHSCOPE_REGION=ap-southeast-1` (Singapore, as item-01 specifies) is present: `True`.
- **A2:** `C:\Channel Contents\MinMiniKids\YT Shorts\keyframes\` has only `L01-KEYFRAME-BRIEF.md`, so **L01_w3 was skipped**.

## B — tests + commit
- `test_flf2v_mock.py`: PASS.
- `test_wan3_mock.py`: **PASS only with `PYTHONUTF8=1`.**
  - As written, it fails on Windows: the subprocess output is decoded as cp1252, a `UnicodeDecodeError` leaves stdout as `None`,
    and the test ends in a `TypeError`.
  - The cause is the test harness, not the wan3 logic. Fix: `encoding="utf-8"` in its `subprocess.run`.
- `py_compile` ×4 OK, `bash -n` OK.
- Dry-runs: `_ab7` est $1.50 (3 rows); `L01_w3` est $0.50 with KEYFRAME MISSING.
- **Commit `aa6ccb8`** `[skip ci]`, pushed `106906b..aa6ccb8`.
  - The push also published three earlier local commits not made by CC: `c2a5ee6`, `754d930`, `b11accb` ("3D queue / 3D-C").
  - `754d930` already contained this dispatch's `pod_bootstrap.sh` / `upscale_video.py` changes.
  - `gh run list --workflow deploy.yml -L 1` still shows `a3ea33b` (09-23): **no run** for this commit.

## C — render
- Run window: **15:18:03 → 15:20:44 UTC** (11:18:03 → 11:20:44 Toronto EDT). The actual charge is in the console, under Usage & Billing.
- Model `wan3.0-video`, 720P 16:9, 5 s, seed 30313. Three tasks ran in parallel; no errors.

| row | task id | wall s | usage | est (list) |
|---|---|---|---|---|
| T04_w3 | `cea3ca0c-2174-44c1-ae5f-b8103302129f` | 151.5 | duration 5.0, output_video_duration 5.0, fps 30, video_count 1, SR 720, ratio 16:9 | $0.50 |
| T07_w3 | `38371c07-f182-4f21-bfb4-4c196b3953ab` | 152.6 | same | $0.50 |
| T08_w3 | `8195eb38-99c7-4e19-9698-fb1a324fdbd3` | 153.0 | same | $0.50 |

- **Total estimate: $1.50 at list price**, ~$1.05 with the 30% launch discount (cap $2.10).
- Outputs are 1280×720 @ 30 fps, 150 frames.
- No URL or key in any sidecar (grepped).

## D — upscale + comparison (laptop, Intel Iris Xe via Vulkan)
All three used the ncnn backend with **`ncnn scale x3`** (console) → 3840×2160 @ 30 fps, 150 frames, interpolation `none`.

| clip | decode / upscale / encode s | s/frame (Real-ESRGAN) |
|---|---|---|
| T04_w3 | 7.0 / 1094.4 / 169.5 | 7.30 |
| T08_w3 | 6.6 / 873.9 / 62.7 | 5.83 |
| T07_w3 | 6.4 / 1000.3 / 118.1 | 6.67 |

- The comparison stills are taken at t = 2.5 s: Wan 3.0 on the left, Phantom on the right, each 720 high.

## Paths
Native renders
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\T04_w3-seed30313-w3.mp4`, `...\out\T04_w3-seed30313-w3.json`, `...\out\_qc\T04_w3-strip.png`
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\T07_w3-seed30313-w3.mp4`, `...\out\T07_w3-seed30313-w3.json`, `...\out\_qc\T07_w3-strip.png`
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\T08_w3-seed30313-w3.mp4`, `...\out\T08_w3-seed30313-w3.json`, `...\out\_qc\T08_w3-strip.png`
- Log: `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\batch_6e.log`

4K
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\4K\T04_w3-seed30313-w3-4K.mp4` (+ `.mp4.json`)
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\4K\T07_w3-seed30313-w3-4K.mp4` (+ `.mp4.json`)
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\4K\T08_w3-seed30313-w3-4K.mp4` (+ `.mp4.json`)

Comparisons
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\_qc\T04-wan3-vs-phantom720.png`
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\_qc\T07-wan3-vs-phantom480.png`
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\_qc\T08-wan3-vs-phantom720.png`

Copies in `C:\Channel Contents\MinMiniKids\songs\Twinkle Twinkle\wan3-test\`
- `...\wan3-test\T04_w3-seed30313-w3-4K.mp4`, `...\wan3-test\T07_w3-seed30313-w3-4K.mp4`, `...\wan3-test\T08_w3-seed30313-w3-4K.mp4`
- `...\wan3-test\T04-wan3-vs-phantom720.png`, `...\wan3-test\T07-wan3-vs-phantom480.png`, `...\wan3-test\T08-wan3-vs-phantom720.png`

L01: nothing rendered, so nothing went to `YT Shorts\renders\L01\wan3\`.

## E — commit
- Statuses: `songs/_ab7-2026-09-28-wan3/shots.csv`, 3× `done`, written by the runner.
- `songs/shorts-loops/shots.csv` is unchanged (L01_w3 was not run).
- The commit hash is in `queue\2026-09-28-wan3-setup\item-03.report.md` and `LOG.md`.

## Not judged
Fable checks:
- Same house as the plate.
- Minnu, Mintu and Minmini on-model vs their refs.
- Two distinct children; mouths.
- Framing size.
- Wan 3.0 vs Phantom side by side.
