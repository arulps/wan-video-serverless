# item-01 — prerequisites + install the upscaler inside the repo — DONE

Machine: `arulps-beast` · 2026-10-07 23:12 (local)

## Prerequisites
| Check | Result |
|---|---|
| Python | `py --version` → Python 3.12.10 |
| ffmpeg / ffprobe | 9.0.2-full_build-www.gyan.dev (both on PATH) |
| Repo | `C:\Projects\opencode\video_image` exists |
| `songs\a07-butterfly\cutplan.json` | exists; 48 shots → **33 distinct takes**, **10** of them `-splice.mp4`; all 33 present in `songs\a07-butterfly\out\` (0 missing) |
| Song folder | `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly` exists |
| Master WAVs | `butterfly (1).wav` (41,493,522 B), `butterfly english (1).wav` (42,668,562 B) |
| GPU | NVIDIA GeForce RTX 2080 Ti, driver 32.0.16.1088 |
| Free space C: | 702.2 GB (need ≥ 30 GB) |
| Old tool location `C:\tools\realesrgan-ncnn-vulkan` | not present on Beast (as expected) |

## Install
- Zip: `realesrgan-ncnn-vulkan-20220424-windows.zip` (xinntao/Real-ESRGAN v0.2.5.0), 45,474,481 B
  - sha256 `abc02804e17982a3be33675e4d471e91ea374e65b70167abc09e31acb412802d`
  - kept at `tools\_dl\r.zip` (git-ignored)
- Extracted flat (zip has no inner folder) to `tools\realesrgan-ncnn-vulkan\`:
  - `realesrgan-ncnn-vulkan.exe` — sha256 `07e49f7cbb4ede01ae4dd4c399d3a7e5846e3d2085c3128eff881e55cb7b1a0c`
  - `vcomp140.dll`, `vcomp140d.dll`, `README_windows.md`, sample `input.jpg`, `input2.jpg`, `onepiece_demo.mp4`
  - `models\`: `realesr-animevideov3-x2/x3/x4` (.param + .bin), `realesrgan-x4plus`, `realesrgan-x4plus-anime` (.param + .bin)

## .gitignore diff
```diff
@@ -13,3 +13,6 @@ nil
 **/_qc/
+
+# local binaries (Real-ESRGAN etc.) — installed per machine, never committed
+tools/
```
`git status --short` lists nothing under `tools/`.
