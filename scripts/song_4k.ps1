# 4K master for a song: upscale every chosen take (resumable), then build the Tamil + English 4K cuts.
#   powershell -ExecutionPolicy Bypass -File scripts\song_4k.ps1 -Song songs\rowboat -Tag V2-4K
# Safe to stop (close the window) and run again: finished clips are skipped (out_4k\<take> + .json sidecar).
# Needs tools\realesrgan-ncnn-vulkan in the repo (git-ignored; see queue\2026-10-07-beast-4k) or C:\tools\... Laptop (Iris Xe): ~4 s/frame -> ~4-5 h per song.
param(
  [Parameter(Mandatory=$true)][string]$Song,
  [string]$Tag = "V2-4K",
  [string]$Lang = "both"
)
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repo
$log = Join-Path $Song "upscale_4k.log"
Write-Host "Step 1/2: upscaling takes -> $Song\out_4k   (log: $log)"
& py scripts\upscale_song.py $Song 2>&1 | Tee-Object -FilePath $log -Append
if ($LASTEXITCODE -ne 0) { throw "upscale stopped (exit $LASTEXITCODE) -- run this script again to resume" }
Write-Host "Step 2/2: building 4K cuts ($Lang, tag $Tag)"
& py comfy\song_cuts.py $Song cut --src out4k --height 2160 --tag $Tag --lang $Lang 2>&1 | Tee-Object -FilePath $log -Append
if ($LASTEXITCODE -ne 0) { throw "4K cut failed (exit $LASTEXITCODE)" }
Write-Host "DONE: 4K cuts are in the song folder's _cuts\ (see $log)"
