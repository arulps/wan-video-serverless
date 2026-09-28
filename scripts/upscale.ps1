# One-command 4K upscale on this laptop (no NVIDIA GPU needed).
#   powershell -ExecutionPolicy Bypass -File scripts\upscale.ps1 "C:\path\clip.mp4"            -> C:\path\clip-4K.mp4
#   ... -Fps 30        also interpolate to 30 fps (RIFE)      ... -Height 1080   1080p instead of 4K
# Uses realesrgan-ncnn-vulkan + rife-ncnn-vulkan (Vulkan: runs on Intel Iris Xe / AMD / NVIDIA).
# Install once: unzip the Windows releases to C:\tools\realesrgan-ncnn-vulkan\ and C:\tools\rife-ncnn-vulkan\
# (see CC-DISPATCH-phase6b). They are added to PATH for this run automatically.
param(
  [Parameter(Mandatory=$true)][string]$Src,
  [string]$Dst = "",
  [int]$Height = 2160,
  [int]$Fps = 0,
  [string]$Backend = "auto"
)
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (-not (Test-Path $Src)) { throw "source not found: $Src" }
if ($Dst -eq "") {
  $suffix = if ($Height -ge 2160) { "-4K" } else { "-$($Height)p" }
  $Dst = Join-Path (Split-Path -Parent $Src) ([IO.Path]::GetFileNameWithoutExtension($Src) + $suffix + ".mp4")
}
foreach ($d in @("C:\tools\realesrgan-ncnn-vulkan", "C:\tools\rife-ncnn-vulkan")) {
  if (Test-Path $d) { $env:PATH = "$d;$env:PATH" } else { Write-Warning "$d not found -- that tool will be skipped (CPU / minterpolate fallback)" }
}
$pyArgs = @((Join-Path $repo "scripts\upscale_video.py"), $Src, $Dst, "--height", $Height, "--backend", $Backend)
if ($Fps -gt 0) { $pyArgs += @("--fps", $Fps) }
Write-Host "-> $Dst"
& py @pyArgs
if ($LASTEXITCODE -ne 0) { throw "upscale failed (exit $LASTEXITCODE)" }
Write-Host "DONE: $Dst  (see $Dst.json for backend and timings)"
