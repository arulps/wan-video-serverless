<#
.SYNOPSIS
  VACE shot: submit ONE reference-to-video job (vace-14B, 1-6 reference images +
  a text prompt, no start frame) to the RunPod serverless endpoint and save the
  result.

  - zero-resubmit rule: throws if any job is already queued/in-progress on the
    endpoint before submitting (never piles jobs on top of each other)
  - one selftest (unless -SkipSelftest) that also gates on a cached model
    snapshot being present on the endpoint, so a cold job never triggers an
    unbudgeted ~75 GB weights download
  - never resubmits: a FAILED/TIMED_OUT job is reported once, not retried
  - saves the full error text to a file next to the (missing) output
  - polls to a terminal state, saves the mp4 + a .json sidecar (video_b64
    excluded), prints a one-line summary
  - waits for workers to drain to 0 at the end so you can see billing has
    stopped

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\vace_shot.ps1 `
    -Refs "C:\refs\front.png","C:\refs\back.png" -Label minnu-v2c `
    -PromptFile prompts\mazhai\V2c-minnu-impatience.txt
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string[]]$Refs,
  [Parameter(Mandatory = $true)][string]$Label,
  [string]$Prompt = "",
  [string]$PromptFile = "",
  [string]$NegativePrompt = "",
  [string]$NegativePromptFile = "",
  [string]$Task = "vace-14B",
  [string]$Size = "1280*720",
  [int]$Frames = 81,
  [int]$Steps = 50,
  [double]$GuideScale = 5.0,
  [double]$Shift = 5.0,
  [double]$ContextScale = 1.0,
  [int]$Seed = 30313,
  [int]$SelftestTimeoutMin = 25,
  [int]$JobTimeoutMin = 60,
  [int]$PollSec = 20,
  [switch]$SkipSelftest,
  [string]$OutDir = "",
  [string]$EndpointKey = "WAN_VACE_ENDPOINT_ID"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$envPath = Join-Path $root ".env"
if (-not (Test-Path $envPath)) { throw ".env not found at $envPath" }

if (-not $Refs -or $Refs.Count -lt 1 -or $Refs.Count -gt 6) { throw "-Refs must have 1 to 6 paths (got $($Refs.Count)); a two-shot takes both characters' refs" }
foreach ($r in $Refs) {
  if (-not (Test-Path $r)) { throw "reference image not found: $r" }
  $rext = [IO.Path]::GetExtension($r).ToLower()
  if ($rext -notin ".png", ".jpg", ".jpeg") { throw "reference image must be .png/.jpg/.jpeg: $r" }
}

if (-not $Prompt -and -not $PromptFile) { throw "give exactly one of -Prompt or -PromptFile" }
if ($Prompt -and $PromptFile) { throw "give exactly one of -Prompt or -PromptFile, not both" }
if ($PromptFile) {
  if (-not (Test-Path $PromptFile)) { throw "prompt file not found: $PromptFile" }
  $Prompt = (Get-Content -Raw -Encoding UTF8 $PromptFile).Trim()
}
if ($NegativePrompt -and $NegativePromptFile) { throw "give at most one of -NegativePrompt or -NegativePromptFile" }
if ($NegativePromptFile) {
  if (-not (Test-Path $NegativePromptFile)) { throw "negative prompt file not found: $NegativePromptFile" }
  $NegativePrompt = (Get-Content -Raw -Encoding UTF8 $NegativePromptFile).Trim()
}
# NegativePrompt left "" on purpose when neither switch is given: an empty
# n_prompt tells the worker to fall back to Wan's own tuned default negative
# prompt rather than us re-typing (and possibly mis-typing) it here.

if (-not $OutDir) { $OutDir = Join-Path $root "outputs\vace" }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Get-EnvValue([string]$name) {
  # Take the LAST non-empty matching line, not the first: this .env has
  # duplicate keys near the top left over from earlier scaffolding whose
  # values are blank, and Select-Object -First 1 (step_ladder's approach)
  # silently picked those up instead of the real value further down.
  $lines = Get-Content $envPath | Where-Object { $_ -match "^\s*$name=" }
  foreach ($line in $lines) {
    $val = (($line -split '=', 2)[1]).Trim().Trim('"').Trim("'")
    if ($val) { $result = $val }
  }
  if (-not $result) { return $null }
  return $result
}
$KEY = Get-EnvValue "RUNPOD_API_KEY"
$EID = (Get-EnvValue $EndpointKey)
if ($EID) { $EID = $EID.Trim('/') }
if (-not $KEY -or -not $EID) { throw "RUNPOD_API_KEY / $EndpointKey missing in .env" }
$base = "https://api.runpod.ai/v2/$EID"
$headers = @{ Authorization = "Bearer $KEY"; "Content-Type" = "application/json" }

function Invoke-Api([string]$method, [string]$path, $body = $null, [int]$retries = 4) {
  $uri = "$base/$path"
  for ($i = 0; $i -lt $retries; $i++) {
    try {
      if ($null -ne $body) {
        $json = $body | ConvertTo-Json -Depth 10 -Compress
        return Invoke-RestMethod -Method $method -Uri $uri -Headers $headers -Body $json -TimeoutSec 180
      }
      return Invoke-RestMethod -Method $method -Uri $uri -Headers $headers -TimeoutSec 120
    } catch {
      if ($i -eq $retries - 1) { throw "API $method $path failed: $($_.Exception.Message)" }
      Write-Host ("  transient API error ({0}); retrying in 10s" -f $_.Exception.Message)
      Start-Sleep -Seconds 10
    }
  }
}
function Show-Health([string]$label) {
  $h = Invoke-Api GET "health"; $w = $h.workers; $j = $h.jobs
  Write-Host ("[{0}] workers idle={1} init={2} ready={3} running={4} | jobs inQueue={5} inProgress={6} completed={7} failed={8}" -f `
    $label, $w.idle, $w.initializing, $w.ready, $w.running, $j.inQueue, $j.inProgress, $j.completed, $j.failed)
  return $h
}
function Wait-Terminal([string]$jobId, [int]$timeoutMin, [string]$label) {
  $deadline = (Get-Date).AddMinutes($timeoutMin); $last = ""
  while ((Get-Date) -lt $deadline) {
    $s = Invoke-Api GET "status/$jobId"
    $extra = if ($s.status -eq "IN_PROGRESS" -and ($s.output -is [string])) { " :: " + $s.output } else { "" }
    $line = ("{0} {1} {2}{3}" -f (Get-Date -Format HH:mm:ss), $label, $s.status, $extra)
    if ($line -ne $last) { Write-Host $line; $last = $line }
    if ($s.status -in @("COMPLETED", "FAILED", "CANCELLED", "TIMED_OUT")) { return $s }
    Start-Sleep -Seconds $PollSec
  }
  try { Invoke-Api POST "cancel/$jobId" | Out-Null } catch { }
  throw "$label timed out after $timeoutMin minutes"
}

# ---------------------------------------------------------------- reference images -> data URIs
Add-Type -AssemblyName System.Drawing
$dataUris = New-Object System.Collections.Generic.List[string]
$n = 0
foreach ($ref in $Refs) {
  $n++
  $src = [System.Drawing.Image]::FromFile($ref)
  $hasAlpha = [System.Drawing.Image]::IsAlphaPixelFormat($src.PixelFormat)

  $longSide = [Math]::Max($src.Width, $src.Height)
  $scale = if ($longSide -gt 1600) { 1600.0 / $longSide } else { 1.0 }
  $dw = [int]([Math]::Round($src.Width * $scale)); $dh = [int]([Math]::Round($src.Height * $scale))

  $canvas = New-Object System.Drawing.Bitmap $dw, $dh
  $g = [System.Drawing.Graphics]::FromImage($canvas)
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  if ($hasAlpha) {
    # The VACE preprocessor pads references onto a WHITE canvas, and a plain
    # PIL convert("RGB") on an RGBA source turns transparent pixels BLACK, not
    # white, which would inject a black halo/background the model was never
    # asked for. Flatten onto white here so the reference already matches
    # what the preprocessor expects.
    $g.Clear([System.Drawing.Color]::White)
  }
  $g.DrawImage($src, 0, 0, $dw, $dh)
  $g.Dispose(); $src.Dispose()

  $outPng = Join-Path $OutDir ("{0}-ref{1}.png" -f $Label, $n)
  $canvas.Save($outPng, [System.Drawing.Imaging.ImageFormat]::Png)
  $canvas.Dispose()

  $bytes = [IO.File]::ReadAllBytes($outPng)
  $dataUri = "data:image/png;base64," + [Convert]::ToBase64String($bytes)
  $dataUris.Add($dataUri)
  $mb = [Math]::Round($dataUri.Length / 1MB, 2)
  Write-Host ("ref{0}: {1} -> {2} ({3}x{4}, {5} MB as base64)" -f $n, $ref, $outPng, $dw, $dh, $mb)
}
$totalBytes = ($dataUris | ForEach-Object { $_.Length } | Measure-Object -Sum).Sum
$totalMb = [Math]::Round($totalBytes / 1MB, 2)
Write-Host ("total ref payload: {0} MB as base64 (RunPod /run payload cap is 10 MB)" -f $totalMb)
if ($totalBytes -gt 9MB) { throw "reference payload too large ($totalMb MB); downscale the refs (fewer refs, or smaller source images) and try again" }

# ---------------------------------------------------------------- 0. health
$h0 = Show-Health "before"
if ($h0.jobs.inProgress -gt 0 -or $h0.jobs.inQueue -gt 0) { throw "jobs already in flight; not submitting (zero-resubmit rule)" }

# ---------------------------------------------------------------- 1. selftest (money gate)
if (-not $SkipSelftest) {
  Write-Host "`n== selftest =="
  $r = Invoke-Api POST "run" @{ input = @{ op = "selftest"; task = $Task } }
  $st = Wait-Terminal $r.id $SelftestTimeoutMin "selftest"
  $o = $st.output
  if ($st.status -ne "COMPLETED" -or -not $o.ok) { throw "selftest failed: $($st.status) $($o.error)" }
  if (-not $o.weights.runpod_cached_snapshot) {
    throw "no cached snapshot for $Task on this endpoint; a 75 GB download would be billed - STOP"
  }
  Write-Host ("selftest OK: gpu={0} vram_total_gb={1} cached_snapshot={2}" -f $o.gpu, $o.vram_total_gb, $o.weights.runpod_cached_snapshot)
  if ($o.tasks) { Write-Host ("tasks: {0}" -f ($o.tasks | ConvertTo-Json -Compress -Depth 4)) }
}

# ---------------------------------------------------------------- 2. build + submit the job
$refImages = [string[]]$dataUris.ToArray()
$payload = @{ input = @{
    task = $Task; prompt = $Prompt; n_prompt = $NegativePrompt; ref_images = $refImages
    size = $Size; frame_num = $Frames; steps = $Steps; guide_scale = $GuideScale
    shift = $Shift; context_scale = $ContextScale; seed = $Seed } }

# ConvertTo-Json unrolls a single-element array into a bare scalar unless the
# property is strongly typed as an array (hence [string[]] above); verify the
# actual wire JSON still has ref_images as an array before we spend a job on it.
$payloadJson = $payload | ConvertTo-Json -Depth 10 -Compress
if ($payloadJson -notmatch '"ref_images":\[') { throw "ref_images did not serialize as a JSON array; payload: $payloadJson" }

$stamp = Get-Date -Format "yyyyMMdd-HHmm"
Write-Host "`n== submit =="
$r = Invoke-Api POST "run" $payload
Write-Host ("submitted {0} refs, label={1} -> job {2}" -f $refImages.Count, $Label, $r.id)

# ---------------------------------------------------------------- 3. poll to terminal
$s = Wait-Terminal $r.id $JobTimeoutMin $Label

$file = $null
if ($s.status -eq "COMPLETED") {
  $o = $s.output
  if ($o.status -ne "complete") {
    $errText = ($o.error | Out-String).Trim()
    $errFile = Join-Path $OutDir ("{0}-{1}-seed{2}-error.txt" -f $stamp, $Label, $Seed)
    [IO.File]::WriteAllText($errFile, $errText)
    Write-Host ("handler error: {0}`n  (full error: {1})" -f $errText, $errFile)
  } else {
    $file = Join-Path $OutDir ("{0}-{1}-seed{2}-{3}f-{4}s.mp4" -f $stamp, $Label, $o.seed, $Frames, $Steps)
    if ($o.video) { Invoke-WebRequest -Uri $o.video -OutFile $file -TimeoutSec 600 }
    elseif ($o.video_b64) { [IO.File]::WriteAllBytes($file, [Convert]::FromBase64String($o.video_b64)) }
    else { throw "job completed but no video in output" }
    $meta = $o | Select-Object * -ExcludeProperty video_b64
    ($meta | ConvertTo-Json -Depth 6) | Set-Content -Path ($file -replace '\.mp4$', '.json')
    Write-Host ("SAVED: {0} ({1:N0} B)" -f $file, (Get-Item $file).Length)
    Write-Host ("meta: gpu={0} dit_dtype={1} t_load_s={2} t_sample_s={3} t_total_s={4} vae_decode_dtype={5} delivery={6} raw_bytes={7}" -f `
      $meta.gpu, $meta.dit_dtype, $meta.t_load_s, $meta.t_sample_s, $meta.t_total_s, $meta.vae_decode_dtype, $meta.delivery, $meta.video_bytes)
  }
} else {
  $errText = ($s.error | Out-String).Trim()
  $errFile = Join-Path $OutDir ("{0}-{1}-seed{2}-error.txt" -f $stamp, $Label, $Seed)
  [IO.File]::WriteAllText($errFile, $errText)
  $tail = $errText.Substring([Math]::Max(0, $errText.Length - 700))
  Write-Host ("{0}: ...{1}`n  (full error: {2})" -f $s.status, $tail, $errFile)
}

# ---------------------------------------------------------------- 4. summary + drain
Write-Host "`n== summary ($Label, seed $Seed, $Frames f, $Size, $Steps steps) =="
Write-Host ("  status={0}  {1}" -f $s.status, $file)

Write-Host "`n== waiting for workers to drain (idleTimeout 300 s) =="
$deadline = (Get-Date).AddMinutes(7)
while ((Get-Date) -lt $deadline) {
  $h = Show-Health "drain"; $w = $h.workers
  if (($w.idle + $w.ready + $w.running + $w.initializing) -eq 0) { Write-Host "workers at 0 - not billing"; break }
  Start-Sleep -Seconds 30
}
Write-Host "done."
