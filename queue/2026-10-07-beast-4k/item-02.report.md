# item-02 — scripts find the in-repo tool — DONE

## Diff
```diff
diff --git a/scripts/song_4k.ps1 b/scripts/song_4k.ps1
index e8d9bfb..21b8ccc 100644
--- a/scripts/song_4k.ps1
+++ b/scripts/song_4k.ps1
@@ -1,7 +1,7 @@
 # 4K master for a song: upscale every chosen take (resumable), then build the Tamil + English 4K cuts.
 #   powershell -ExecutionPolicy Bypass -File scripts\song_4k.ps1 -Song songs\rowboat -Tag V2-4K
 # Safe to stop (close the window) and run again: finished clips are skipped (out_4k\<take> + .json sidecar).
-# Needs C:\tools\realesrgan-ncnn-vulkan (see CC-DISPATCH-phase6b). Laptop (Iris Xe): ~4 s/frame -> ~4-5 h per song.
+# Needs tools\realesrgan-ncnn-vulkan in the repo (git-ignored; see queue\2026-10-07-beast-4k) or C:\tools\... Laptop (Iris Xe): ~4 s/frame -> ~4-5 h per song.
 param(
   [Parameter(Mandatory=$true)][string]$Song,
   [string]$Tag = "V2-4K",
diff --git a/scripts/upscale_song.py b/scripts/upscale_song.py
index 8c2a8af..1e1c8e2 100644
--- a/scripts/upscale_song.py
+++ b/scripts/upscale_song.py
@@ -9,7 +9,8 @@ Each take goes through scripts/upscale_video.py (Real-ESRGAN realesr-animevideov
 lanczos to 3840x2160, same 30 fps, h264 crf 16). A take counts as done only when its out_4k .mp4 AND .mp4.json sidecar
 exist (the sidecar is written last), so an interrupted run resumes at the clip it was on; a half-written mp4 is redone.
 Forces --backend ncnn: on a laptop without CUDA the torch-CPU fallback is ~29 s/frame (a song would take >30 h), so if
-the Vulkan tool is missing it stops instead. C:\\tools\\realesrgan-ncnn-vulkan is put on PATH when it exists.
+the Vulkan tool is missing it stops instead. The first of <repo>\\tools\\realesrgan-ncnn-vulkan (git-ignored, installed
+per machine) or C:\\tools\\realesrgan-ncnn-vulkan (old location) that exists is put on PATH.
 Then: python comfy/song_cuts.py songs/<slug> cut --src out4k --height 2160 --tag V2-4K --lang both
 """
 import argparse, json, os, shutil, subprocess, sys, time
@@ -35,11 +36,13 @@ def main():
         if (only and s["id"] not in only) or s["take"] in seen:
             continue
         seen.add(s["take"]); takes.append((s["id"], s["take"]))
-    for d in (r"C:\tools\realesrgan-ncnn-vulkan",):
-        if os.path.isdir(d):
-            os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]
+    tool_dirs = (HERE.parent / "tools" / "realesrgan-ncnn-vulkan", Path(r"C:\tools\realesrgan-ncnn-vulkan"))
+    for d in tool_dirs:
+        if d.is_dir():
+            os.environ["PATH"] = str(d) + os.pathsep + os.environ["PATH"]
+            break
     if not a.dry and not shutil.which("realesrgan-ncnn-vulkan"):
-        sys.exit("realesrgan-ncnn-vulkan not found (expected in C:\\tools\\realesrgan-ncnn-vulkan) -- stopping")
+        sys.exit("realesrgan-ncnn-vulkan not found (expected in %s or %s) -- stopping" % tool_dirs)
     dst_dir = song / "out_4k"; dst_dir.mkdir(exist_ok=True)
     todo = []
     for sid, take in takes:
```

## `py scripts\upscale_song.py songs\a07-butterfly --dry`
No "not found". Summary line: **`to do: 33 clips, 5217 frames`**
```
to do: 33 clips, 5217 frames
   I1 I1-seed30313-w3.mp4 210 frames
   I2 I2-seed30313-w3.mp4 150 frames
   RA RA-seed30313-w3.mp4 240 frames
   RB RB-seed30313-w3.mp4 240 frames
   CH3 CH3-seed30313-w3.mp4 150 frames
   CH4 CH4-seed30313-w3.mp4 150 frames
   V1a V1a-seed30313-w3.mp4 150 frames
   V1b V1b-seed30313-w3-splice.mp4 140 frames
   V1c V1c-seed30313-w3-splice.mp4 142 frames
   V1d V1d-seed30313-w3.mp4 150 frames
   V2a V2a-seed30313-w3-splice.mp4 149 frames
   V2b V2b-seed30313-w3-splice.mp4 139 frames
   V2c V2c-seed30313-w3-splice.mp4 137 frames
   V2d V2d-seed30313-w3.mp4 150 frames
   V3a V3a-seed30313-w3-splice.mp4 139 frames
   V3b V3b-seed30313-w3.mp4 150 frames
   V3c V3c-seed30313-w3.mp4 150 frames
   V3d V3d-seed30313-w3.mp4 150 frames
   BRKb BRKb-seed30313-w3.mp4 150 frames
   V4a V4a-seed30313-w3-splice.mp4 139 frames
   V4b V4b-seed30313-w3-splice.mp4 139 frames
   V4c V4c-seed30313-w3.mp4 150 frames
   V4d V4d-seed30313-w3.mp4 150 frames
   V5a V5a-seed30313-w3.mp4 150 frames
   V5b V5b-seed30313-w3.mp4 150 frames
   V5c V5c-seed30313-w3.mp4 150 frames
   V5d V5d-seed30313-w3.mp4 150 frames
   V6a V6a-seed30313-w3.mp4 150 frames
   V6b V6b-seed30313-w3-splice.mp4 139 frames
   V6c V6c-seed30313-w3.mp4 150 frames
   V6d V6d-seed30313-w3.mp4 150 frames
   O3 O3-seed30313-w3-splice.mp4 204 frames
   O4 O4-seed30313-w3.mp4 210 frames
```
