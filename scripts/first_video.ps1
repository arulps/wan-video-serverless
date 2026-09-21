<#
.SYNOPSIS
  Bounded, money-safe "first video" run against the wan-video-serverless endpoint.

  1. reads RUNPOD_API_KEY + WAN_ENDPOINT_ID from .env (never typed by hand)
  2. /health snapshot (must be idle)
  3. selftest job  -> proves SDPA patch reached wan.modules.model, GPU present,
                      where the weights will come from (RunPod cache or download)
                      Costs one worker boot, loads NO weights.
  4. ONE real job  -> polls to a terminal state, saves the mp4 to .\outputs\
  5. waits for workers to drain back to 0 (workersMin=0, idleTimeout=300 s)

  It never resubmits, never recreates anything, never calls runpodctl.
  Stop conditions are explicit; nothing here loops on failure.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\first_video.ps1
  powershell -ExecutionPolicy Bypass -File scripts\first_video.ps1 -Prompt "..." -Steps 20 -Frames 81 -Seed 30313
  powershell -ExecutionPolicy Bypass -File scripts\first_video.ps1 -SelftestOnly
#>
[CmdletBinding()]
param(
  [string]$Prompt = "A cheerful cartoon duckling in a tiny yellow raincoat splashes through a puddle on a rainy village lane, soft matte children's picture-book look, warm colours, gentle slow camera push-in, no text",
  [string]$NegativePrompt = "text, watermark, logo, subtitles, blurry, deformed, extra limbs, realistic photo, dark, horror",
  [string]$Task = "ti2v-5B",
  [string]$Size = "1280*704",
  [int]$Frames = 81,
  [int]$Steps = 20,
  [double]$GuideScale = 5.0,
  [int]$Seed = 30313,
  [int]$SelftestTimeoutMin = 20,
  [int]$JobTimeoutMin = 35,
  [int]$PollSec = 15,
  [switch]$SelftestOnly,
  [switch]$SkipSelftest
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$envPath = Join-Path $root ".env"
if (-not (Test-Path $envPath)) { throw ".env not found at $envPath" }

function Get-EnvValue([string]$name) {
  $line = Get-Content $envPath | Where-Object { $_ -match "^\s*$name=" } | Select-Object -First 1
  if (-not $line) { return $null }
  return (($line -split '=', 2)[1]).Trim().Trim('"').Trim("'")
}

$KEY = Get-EnvValue "RUNPOD_API_KEY"
$EID = Get-EnvValue "WAN_ENDPOINT_ID"
if (-not $KEY) { throw "RUNPOD_API_KEY is empty in .env" }
if (-not $EID) { throw "WAN_ENDPOINT_ID is empty in .env" }
$EID = $EID.Trim('/')
Write-Host ("endpoint id = [{0}]  key length = {1}" -f $EID, $KEY.Length)

$base = "https://api.runpod.ai/v2/$EID"
$headers = @{ Authorization = "Bearer $KEY"; "Content-Type" = "application/json" }

function Invoke-Api([string]$method, [string]$path, $body = $null, [int]$retries = 4) {
  $uri = "$base/$path"
  for ($i = 0; $i -lt $retries; $i++) {
    try {
      if ($null -ne $body) {
        $json = $body | ConvertTo-Json -Depth 10 -Compress
        return Invoke-RestMethod -Method $method -Uri $uri -Headers $headers -Body $json -TimeoutSec 120
      }
      return Invoke-RestMethod -Method $method -Uri $uri -Headers $headers -TimeoutSec 120
    } catch {
      $msg = $_.Exception.Message
      if ($i -eq $retries - 1) { throw "API $method $path failed: $msg" }
      Write-Host ("  transient API error ({0}); retrying in 10s" -f $msg)
      Start-Sleep -Seconds 10
    }
  }
}

function Show-Health([string]$label) {
  $h = Invoke-Api GET "health"
  $w = $h.workers; $j = $h.jobs
  Write-Host ("[{0}] workers idle={1} initializing={2} ready={3} running={4} throttled={5} unhealthy={6} | jobs inQueue={7} inProgress={8} completed={9} failed={10}" -f `
    $label, $w.idle, $w.initializing, $w.ready, $w.running, $w.throttled, $w.unhealthy, $j.inQueue, $j.inProgress, $j.completed, $j.failed)
  return $h
}

function Wait-RunpodJob([string]$jobId, [int]$timeoutMin, [string]$label) {
  $deadline = (Get-Date).AddMinutes($timeoutMin)
  $last = ""
  while ((Get-Date) -lt $deadline) {
    $s = Invoke-Api GET "status/$jobId"
    $state = $s.status
    $extra = ""
    if ($state -eq "IN_PROGRESS" -and $s.output -and ($s.output -is [string])) { $extra = " :: " + $s.output }
    $line = ("{0} {1} {2}{3}" -f (Get-Date -Format HH:mm:ss), $label, $state, $extra)
    if ($line -ne $last) { Write-Host $line; $last = $line }
    if ($state -in @("COMPLETED", "FAILED", "CANCELLED", "TIMED_OUT")) { return $s }
    Start-Sleep -Seconds $PollSec
  }
  Write-Host ("{0} exceeded {1} min - cancelling job {2}" -f $label, $timeoutMin, $jobId)
  try { Invoke-Api POST "cancel/$jobId" | Out-Null } catch { }
  throw "$label timed out after $timeoutMin minutes"
}

# ---------------------------------------------------------------- 0. health
$h0 = Show-Health "before"
if ($h0.jobs.inProgress -gt 0 -or $h0.jobs.inQueue -gt 0) {
  throw "endpoint already has jobs in flight; not submitting another (zero-resubmit rule)"
}

# ---------------------------------------------------------------- 1. selftest
if (-not $SkipSelftest) {
  Write-Host "`n== selftest job (boots a worker, loads no weights) =="
  $r = Invoke-Api POST "run" @{ input = @{ op = "selftest"; task = $Task } }
  $st = Wait-RunpodJob $r.id $SelftestTimeoutMin "selftest"
  $out = $st.output
  Write-Host ($out | ConvertTo-Json -Depth 8)
  if ($st.status -ne "COMPLETED") { throw "selftest job ended $($st.status): $($st.error)" }
  if (-not $out.ok) { throw "selftest reports NOT ok: $($out.error)" }
  if (-not $out.shim.model_binding_patched) { throw "SDPA patch did not reach wan.modules.model - STOP" }
  Write-Host ("selftest OK: gpu={0} vram_free={1}GB hf_hub={2} cached_snapshot={3} alloc_conf={4}" -f `
    $out.gpu, $out.vram_free_gb, $out.huggingface_hub, $out.weights.runpod_cached_snapshot, $out.alloc_conf)
  if ($out.alloc_conf -notlike "*expandable_segments:True*") {
    throw "worker is running WITHOUT PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True - the image/template is stale (the VAE decode OOM fix is not on this worker). STOP."
  }
  if (-not $out.weights.runpod_cached_snapshot -and -not $out.weights.local_copy) {
    Write-Host "NOTE: no cached weights on this worker - the real job will download ~34 GB first (billed). Attach the model to the endpoint (Model field: Wan-AI/Wan2.2-TI2V-5B) to avoid this next time."
  }
  if ($SelftestOnly) { Show-Health "after selftest" | Out-Null; exit 0 }
}

# ---------------------------------------------------------------- 2. one job
$payload = @{
  input = @{
    task = $Task; prompt = $Prompt; n_prompt = $NegativePrompt
    size = $Size; frame_num = $Frames; steps = $Steps; guide_scale = $GuideScale; seed = $Seed
  }
}
Write-Host "`n== submitting ONE job =="
Write-Host (($payload.input | ConvertTo-Json -Compress))
$r = Invoke-Api POST "run" $payload
Write-Host ("job id = {0}" -f $r.id)
$st = Wait-RunpodJob $r.id $JobTimeoutMin "job"

if ($st.status -ne "COMPLETED") {
  Write-Host "JOB $($st.status)"
  Write-Host ($st | ConvertTo-Json -Depth 6)
  Write-Host "`nSTOP. Read the error above / worker container logs. Do NOT resubmit without a root cause."
  Show-Health "after failure" | Out-Null
  exit 1
}

$out = $st.output
$meta = $out | Select-Object * -ExcludeProperty video_b64
Write-Host ($meta | ConvertTo-Json -Depth 6)
if ($out.status -ne "complete") { throw "handler returned status=$($out.status): $($out.error)" }

$outDir = Join-Path $root "outputs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$file = Join-Path $outDir ("{0}-{1}-seed{2}-{3}f-{4}s.mp4" -f $stamp, $Task, $out.seed, $Frames, $Steps)
if ($out.video) {
  Invoke-WebRequest -Uri $out.video -OutFile $file -TimeoutSec 600
} elseif ($out.video_b64) {
  [IO.File]::WriteAllBytes($file, [Convert]::FromBase64String($out.video_b64))
} else {
  throw "no video in output (keys: $($out.PSObject.Properties.Name -join ', '))"
}
$bytes = (Get-Item $file).Length
Write-Host ("`nSAVED {0} ({1:N0} bytes)  seed={2} steps={3} frames={4} fps={5} t_total={6}s  vae_decode={7} retried={8}" -f $file, $bytes, $out.seed, $out.steps, $out.frame_num, $out.fps, $out.t_total_s, $out.vae_decode_dtype, $out.vae_decode_retried)
if ($bytes -lt 10000) { Write-Host "WARNING: file is suspiciously small - inspect before trusting" }

# meta sidecar for the review
($meta | ConvertTo-Json -Depth 6) | Set-Content -Path ($file -replace '\.mp4$', '.json')

# ---------------------------------------------------------------- 3. drain
Write-Host "`n== waiting for workers to drain (workersMin=0, idleTimeout=300s) =="
$deadline = (Get-Date).AddMinutes(7)
while ((Get-Date) -lt $deadline) {
  $h = Show-Health "drain"
  $w = $h.workers
  if (($w.idle + $w.ready + $w.running + $w.initializing) -eq 0) { Write-Host "workers at 0 - not billing"; break }
  Start-Sleep -Seconds 30
}
Write-Host "done."
