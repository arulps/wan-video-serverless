# item-02 — start the 4K master in its own window ($0.00)

1. Pre-checks:
   - `tools\realesrgan-ncnn-vulkan\realesrgan-ncnn-vulkan.exe` exists;
   - `py -c "import numpy, PIL"` works;
   - `ffmpeg -version` prints a version.

   Report all three. Any one missing → **blocked**.
2. From the repo root, start the job in a **separate** PowerShell window so it outlives this session:
   ```
   Start-Process powershell -ArgumentList '-NoExit','-ExecutionPolicy','Bypass','-File','scripts\song_4k.ps1','-Song','songs\l05-urulai-w3','-Tag','V1-4K' -WorkingDirectory C:\Projects\opencode\video_image
   ```
3. Wait 2 minutes, then report the last 10 lines of `songs\l05-urulai-w3\upscale_4k.log`; it should be upscaling the first take. If
   the log shows an error → **blocked**, with the error verbatim. Write `item-02.done` once the job is running.
