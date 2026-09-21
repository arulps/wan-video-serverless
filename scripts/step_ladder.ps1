<#
.SYNOPSIS
  Step ladder: the SAME start frame + prompt + seed rendered at several step counts,
  so production defaults can be chosen by eye. Image-to-video (ti2v-5B, image input).

  - one selftest (unless -SkipSelftest), then all ladder jobs are submitted at once
    (workersMax=3 -> three run in parallel, the rest queue; the warm workers reuse the
    loaded pipeline so the 148 s load is paid at most three times)
  - polls every job to a terminal state, saves each mp4 + json sidecar to .\outputs\ladder\
  - never resubmits; a FAILED rung is reported and the others continue
  - waits for workers to drain to 0 at the end

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\step_ladder.ps1 `
    -Image "C:\Channel Contents\MinMiniKids\charecter bible\generation-refs-2026-08-31\Minnu\body-relaxed-neutral.jpg" `
    -Label minnu -Prompt "She waves and smiles, gentle breeze in her pigtails, camera steady"
  powershell -ExecutionPolicy Bypass -File scripts\step_ladder.ps1 -Image ... -Label mintu -Steps 20,40
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$Image,
  [Parameter(Mandatory = $true)][string]$Label,
  [string]$Prompt = "The child slowly turns to look at the camera and smiles warmly, blinks once, hair sways in a gentle breeze; slow natural motion, soft matte children's picture-book look, camera steady, no text",
  [string]$NegativePrompt = "text, watermark, logo, subtitles, blurry, deformed, extra limbs, extra fingers, realistic photo, dark, horror, fast motion, camera shake",
  [int[]]$Steps = @(30),
  [string]$Size = "1280*704",
  [int]$Frames = 81,
  [double]$GuideScale = 5.0,
  [int]$Seed = 30313,
  [int]$SelftestTimeoutMin = 20,
  [int]$JobTimeoutMin = 50,
  [int]$PollSec = 20,
  [switch]$SkipSelftest,
  # Wan's I2V path takes the OUTPUT aspect ratio from the start frame
  # (wan/utils/utils.py best_output_size), so a square turnaround ref would yield a
  # ~928x928 video. By default the ref is composited onto a 1280x704 canvas first.
  [switch]$NoFitToFrame,
  [string]$CanvasColor = "#F6EFE3",
  [double]$SubjectHeightFrac = 0.90,
  # Optional crop of the source before fitting, "x,y,w,h" in source pixels (e.g. to take one
  # panel out of a multi-view turnaround sheet).
  [string]$CropPx = "",
  # Framing. Full-figure refs left the character ~40% of frame height, so a hand was
  # ~40 px and the model smeared it while moving (2026-09-21 ladders). "waist" keeps the
  # top TopFrac of the (cropped) source and fills the canvas with it; "full" is the old
  # behaviour. Use waist/close for anything with hand or face motion.
  [ValidateSet("full", "waist", "close")][string]$Framing = "waist",
  [double]$TopFrac = 0.58
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$envPath = Join-Path $root ".env"
if (-not (Test-Path $envPath)) { throw ".env not found at $envPath" }
if (-not (Test-Path $Image)) { throw "start frame not found: $Image" }

function Get-EnvValue([string]$name) {
  $line = Get-Content $envPath | Where-Object { $_ -match "^\s*$name=" } | Select-Object -First 1
  if (-not $line) { return $null }
  return (($line -split '=', 2)[1]).Trim().Trim('"').Trim("'")
}
$KEY = Get-EnvValue "RUNPOD_API_KEY"
$EID = (Get-EnvValue "WAN_ENDPOINT_ID").Trim('/')
if (-not $KEY -or -not $EID) { throw "RUNPOD_API_KEY / WAN_ENDPOINT_ID missing in .env" }
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

# ---------------------------------------------------------------- start frame -> 16:9 canvas
$outDir = Join-Path $root "outputs\ladder"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
if (-not $NoFitToFrame) {
  Add-Type -AssemblyName System.Drawing
  $src = [System.Drawing.Image]::FromFile($Image)
  if ($CropPx) {
    $c = $CropPx -split "," | ForEach-Object { [int]$_.Trim() }
    if ($c.Count -ne 4 -or $c[2] -le 0 -or $c[3] -le 0 -or ($c[0] + $c[2]) -gt $src.Width -or ($c[1] + $c[3]) -gt $src.Height) { throw "bad -CropPx `"$CropPx`" for a $($src.Width)x$($src.Height) image (want x,y,w,h inside the image)" }
    $rect = New-Object System.Drawing.Rectangle $c[0], $c[1], $c[2], $c[3]
    $cropped = ([System.Drawing.Bitmap]$src).Clone($rect, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $src.Dispose(); $src = $cropped
    Write-Host ("cropped source to {0}x{1} at {2},{3}" -f $c[2], $c[3], $c[0], $c[1])
  }
  if ($Framing -ne "full") {
    # Trim the margins so the figure, not the padding, sets the scale. Background =
    # the mean of the four corner pixels (refs are ~245 grey or transparent, not pure
    # white); a pixel is figure if alpha>16 and any channel differs from that by >24;
    # rows/cols need >=2 such pixels (4-px stride; GetPixel is slow in PowerShell) so stray
    # noise cannot stretch the box.
    $bmp = [System.Drawing.Bitmap]$src
    $cs = @($bmp.GetPixel(0,0), $bmp.GetPixel($bmp.Width-1,0), $bmp.GetPixel(0,$bmp.Height-1), $bmp.GetPixel($bmp.Width-1,$bmp.Height-1))
    $bgR = ($cs | Measure-Object -Property R -Average).Average
    $bgG = ($cs | Measure-Object -Property G -Average).Average
    $bgB = ($cs | Measure-Object -Property B -Average).Average
    $rowCount = New-Object int[] $bmp.Height; $colCount = New-Object int[] $bmp.Width
    for ($y = 0; $y -lt $bmp.Height; $y += 4) {
      for ($x = 0; $x -lt $bmp.Width; $x += 4) {
        $px = $bmp.GetPixel($x, $y)
        if ($px.A -gt 16) {
          $d = [Math]::Max([Math]::Abs($px.R - $bgR), [Math]::Max([Math]::Abs($px.G - $bgG), [Math]::Abs($px.B - $bgB)))
          if ($d -gt 24) { $rowCount[$y]++; $colCount[$x]++ }
        }
      }
    }
    $rows = 0..($bmp.Height-1) | Where-Object { $rowCount[$_] -ge 2 }
    $cols = 0..($bmp.Width-1)  | Where-Object { $colCount[$_] -ge 2 }
    if (-not $rows -or -not $cols) { throw "could not find the figure's bounding box in the start frame" }
    $minY = ($rows | Measure-Object -Minimum).Minimum; $maxY = ($rows | Measure-Object -Maximum).Maximum
    $minX = ($cols | Measure-Object -Minimum).Minimum; $maxX = ($cols | Measure-Object -Maximum).Maximum
    if ($maxX -le $minX -or $maxY -le $minY) { throw "could not find the figure's bounding box in the start frame" }
    $keep = if ($Framing -eq "close") { [Math]::Min($TopFrac, 0.40) } else { $TopFrac }
    $bh = [int](($maxY - $minY) * $keep)
    $rect = New-Object System.Drawing.Rectangle $minX, $minY, ($maxX - $minX), $bh
    $part = $bmp.Clone($rect, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $src.Dispose(); $src = $part
    Write-Host ("framing={0}: figure bbox {1},{2}-{3},{4}; keeping top {5:P0} -> {6}x{7}" -f $Framing, $minX, $minY, $maxX, $maxY, $keep, $src.Width, $src.Height)
    $SubjectHeightFrac = 0.96
  }
  $cw, $ch = 1280, 704
  $canvas = New-Object System.Drawing.Bitmap $cw, $ch
  $g = [System.Drawing.Graphics]::FromImage($canvas)
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.Clear([System.Drawing.ColorTranslator]::FromHtml($CanvasColor))
  $scale = [Math]::Min(($ch * $SubjectHeightFrac) / $src.Height, ($cw * 0.9) / $src.Width)
  $dw = [int]($src.Width * $scale); $dh = [int]($src.Height * $scale)
  $dx = [int](($cw - $dw) / 2); $dy = [int](($ch - $dh) / 2)
  $g.DrawImage($src, $dx, $dy, $dw, $dh)   # alpha composites onto the canvas colour
  $g.Dispose(); $src.Dispose()
  $fitted = Join-Path $outDir ("{0}-startframe-1280x704.jpg" -f $Label)
  $enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq "image/jpeg" }
  $ep = New-Object System.Drawing.Imaging.EncoderParameters 1
  $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality, [long]92)
  $canvas.Save($fitted, $enc, $ep); $canvas.Dispose()
  Write-Host ("start frame fitted to 1280x704 -> {0}  (subject {1}x{2} at {3},{4})" -f $fitted, $dw, $dh, $dx, $dy)
  $Image = $fitted
}

# ---------------------------------------------------------------- start frame -> data URI
$bytes = [IO.File]::ReadAllBytes($Image)
$ext = [IO.Path]::GetExtension($Image).ToLower()
$mime = if ($ext -eq ".png") { "image/png" } elseif ($ext -in ".jpg", ".jpeg") { "image/jpeg" } else { throw "use a .png or .jpg start frame" }
$dataUri = "data:$mime;base64," + [Convert]::ToBase64String($bytes)
$mb = [Math]::Round($dataUri.Length / 1MB, 2)
Write-Host ("start frame {0} -> {1} MB as base64 (RunPod /run payload cap is 10 MB)" -f $Image, $mb)
if ($dataUri.Length -gt 9MB) { throw "start frame too large for the /run payload; downscale it to <= 1280 px wide first" }

# ---------------------------------------------------------------- 0. health + selftest
$h0 = Show-Health "before"
if ($h0.jobs.inProgress -gt 0 -or $h0.jobs.inQueue -gt 0) { throw "jobs already in flight; not submitting (zero-resubmit rule)" }

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

if (-not $SkipSelftest) {
  Write-Host "`n== selftest =="
  $r = Invoke-Api POST "run" @{ input = @{ op = "selftest"; task = "ti2v-5B" } }
  $st = Wait-Terminal $r.id $SelftestTimeoutMin "selftest"
  $o = $st.output
  if ($st.status -ne "COMPLETED" -or -not $o.ok) { throw "selftest failed: $($st.status) $($o.error)" }
  if ($o.alloc_conf -notlike "*expandable_segments:True*") { throw "stale worker (no expandable_segments) - STOP" }
  Write-Host ("selftest OK: gpu={0} cached_snapshot={1}" -f $o.gpu, $o.weights.runpod_cached_snapshot)
}

# ---------------------------------------------------------------- 1. submit the whole ladder
$stamp = Get-Date -Format "yyyyMMdd-HHmm"
$jobs = @()
foreach ($n in $Steps) {
  $payload = @{ input = @{
      task = "ti2v-5B"; prompt = $Prompt; n_prompt = $NegativePrompt; image = $dataUri
      size = $Size; frame_num = $Frames; steps = $n; guide_scale = $GuideScale; seed = $Seed } }
  $r = Invoke-Api POST "run" $payload
  Write-Host ("submitted steps={0} -> job {1}" -f $n, $r.id)
  $jobs += [pscustomobject]@{ steps = $n; id = $r.id; status = "SUBMITTED"; file = $null; meta = $null }
}

# ---------------------------------------------------------------- 2. poll all
$deadline = (Get-Date).AddMinutes($JobTimeoutMin)
while (((Get-Date) -lt $deadline) -and ($jobs | Where-Object { $_.status -notin "COMPLETED", "FAILED", "CANCELLED", "TIMED_OUT" })) {
  foreach ($j in $jobs) {
    if ($j.status -in "COMPLETED", "FAILED", "CANCELLED", "TIMED_OUT") { continue }
    $s = Invoke-Api GET "status/$($j.id)"
    $extra = if ($s.status -eq "IN_PROGRESS" -and ($s.output -is [string])) { " :: " + $s.output } else { "" }
    $line = ("{0} steps={1} {2}{3}" -f (Get-Date -Format HH:mm:ss), $j.steps, $s.status, $extra)
    if ($line -ne $j.last) { Write-Host $line; $j | Add-Member -Force NoteProperty last $line }
    if ($s.status -eq "COMPLETED") {
      $o = $s.output
      if ($o.status -ne "complete") { $j.status = "FAILED"; $j.meta = $o; Write-Host ("steps={0} handler error: {1}" -f $j.steps, $o.error); continue }
      $file = Join-Path $outDir ("{0}-{1}-seed{2}-{3}f-{4}steps.mp4" -f $stamp, $Label, $o.seed, $Frames, $j.steps)
      if ($o.video) { Invoke-WebRequest -Uri $o.video -OutFile $file -TimeoutSec 600 }
      elseif ($o.video_b64) { [IO.File]::WriteAllBytes($file, [Convert]::FromBase64String($o.video_b64)) }
      else { $j.status = "FAILED"; Write-Host "steps=$($j.steps): no video in output"; continue }
      $meta = $o | Select-Object * -ExcludeProperty video_b64
      ($meta | ConvertTo-Json -Depth 6) | Set-Content -Path ($file -replace '\.mp4$', '.json')
      $j.status = "COMPLETED"; $j.file = $file; $j.meta = $meta
      Write-Host ("SAVED steps={0}: {1} ({2:N0} B) t_sample={3}s t_total={4}s vae={5}" -f $j.steps, $file, (Get-Item $file).Length, $meta.t_sample_s, $meta.t_total_s, $meta.vae_decode_dtype)
    } elseif ($s.status -in "FAILED", "CANCELLED", "TIMED_OUT") {
      $j.status = $s.status; $j.meta = $s
      $errText = ($s.error | Out-String).Trim()
      $errFile = Join-Path $outDir ("{0}-{1}-{2}steps-error.txt" -f $stamp, $Label, $j.steps)
      [IO.File]::WriteAllText($errFile, $errText)
      $tail = $errText.Substring([Math]::Max(0, $errText.Length - 700))
      Write-Host ("steps={0} {1}: ...{2}`n  (full error: {3})" -f $j.steps, $s.status, $tail, $errFile)
    }
  }
  Start-Sleep -Seconds $PollSec
}
foreach ($j in $jobs) { if ($j.status -notin "COMPLETED", "FAILED", "CANCELLED", "TIMED_OUT") { try { Invoke-Api POST "cancel/$($j.id)" | Out-Null } catch { }; $j.status = "TIMED_OUT" } }

# ---------------------------------------------------------------- 3. summary + drain
Write-Host "`n== ladder summary ($Label, seed $Seed, $Frames f, $Size) =="
$jobs | ForEach-Object {
  $t = if ($_.meta -and $_.meta.t_sample_s) { "{0}s sample / {1}s total" -f $_.meta.t_sample_s, $_.meta.t_total_s } else { "-" }
  Write-Host ("  steps={0,-3} {1,-10} {2}  {3}" -f $_.steps, $_.status, $t, $_.file)
}
($jobs | Select-Object steps, id, status, file | ConvertTo-Json -Depth 4) | Set-Content -Path (Join-Path $outDir "$stamp-$Label-ladder.json")

Write-Host "`n== waiting for workers to drain (idleTimeout 300 s) =="
$deadline = (Get-Date).AddMinutes(7)
while ((Get-Date) -lt $deadline) {
  $h = Show-Health "drain"; $w = $h.workers
  if (($w.idle + $w.ready + $w.running + $w.initializing) -eq 0) { Write-Host "workers at 0 - not billing"; break }
  Start-Sleep -Seconds 30
}
Write-Host "done."
