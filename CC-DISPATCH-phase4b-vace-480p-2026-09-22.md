# CC-DISPATCH — Phase 4b: fix the staging, test cheap at 480p (2026-09-22)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** Claude Code on the laptop.
**Endpoint:** `wan-vace-serverless` (`WAN_VACE_ENDPOINT_ID` in `.env`, already set). No deploy, no worker change.
**Cost:** two 832×480 / 30-step clips ≈ 6–10 min each on the H100 (~$0.5 each). Hard stop after both.

## 0 · What the V1a frame check said

`outputs\vace\_qc\v1a-openart-vs-vace-2026-09-22.png` + `v1a-vace-hand-zoom-2026-09-22.png`. Rendering is
OpenArt-grade: five clean fingers with motion blur, crisp cowlick, room matches the WORLD block. **Staging was wrong:**
VACE read "back three-quarters to camera, camera at child height" literally → over-the-shoulder shot, head cropped,
window far away, no palm press, face never visible. That is a prompt problem, and at 40 min / ~$2.9 per 720p clip
(t_sample 2423 s at 50 steps) we don't iterate prompts at 720p. Same method as the runsheet: block at 480p, shoot at 720p.

## 1 · New files (written by Fable)

- `prompts\mazhai\V1a-mintu-at-glass-v2.txt` — explicit camera ("stands across the room facing the window, child
  eye height, locked off"), explicit framing ("whole body head to shoes, room above the head, never crop the head"),
  explicit contact ("both palms already pressed flat on the inside of the glass"), face visible.
- `prompts\mazhai\V2c-minnu-impatience-v2.txt` — same treatment; head-to-knees framing, hands clasped, turn to camera.
- `prompts\mazhai\README.md` — note on the -v2 files.

Nothing to commit before running (prompts are data), but commit them with the results at the end.

## 2 · Run both at 480p, 30 steps

```
cd C:\Projects\opencode\video_image

powershell -ExecutionPolicy Bypass -File scripts\vace_shot.ps1 `
  -Refs "C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Mintu\Gemini_Generated_Image_fxwpvvfxwpvvfxwp.jpeg" `
  -Label v1a-mintu-480 -Size "832*480" -Steps 30 -PromptFile prompts\mazhai\V1a-mintu-at-glass-v2.txt -NegativePromptFile prompts\mazhai\NEGATIVE.txt

powershell -ExecutionPolicy Bypass -File scripts\vace_shot.ps1 -SkipSelftest `
  -Refs "C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\front.png","C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\back.png","C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\left.png","C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\right.png" `
  -Label v2c-minnu-480 -Size "832*480" -Steps 30 -PromptFile prompts\mazhai\V2c-minnu-impatience-v2.txt -NegativePromptFile prompts\mazhai\NEGATIVE.txt
```

Run them one after the other (workersMax is 2, but the second job would pay a second cold load; sequential reuses
the warm worker — cheaper). The first run's selftest is the only one needed.

`832*480` is in `SUPPORTED_SIZES['vace-14B']` upstream and `prepare_source` accepts that area (seq_len 32760), so
no worker change. If the handler rejects the size, report the error text verbatim and stop.

## 3 · Report, then stop

For each clip: meta (`gpu`, `t_sample_s`, `t_total_s`, `delivery`), path, and the 5-frame strip:
```
ffmpeg -y -i outputs\vace\<clip>.mp4 -vf "select='eq(n,0)+eq(n,20)+eq(n,40)+eq(n,60)+eq(n,80)',tile=5x1" -vsync 0 outputs\vace\_qc\<label>-strip.png
```
Arul/Fable judge blocking (camera across the room, whole body in frame, palms on glass / hands clasped) and, on V2c,
face identity vs `Turnarounds\Minnu\front.png` and OpenArt's `09_V2c_minnu-hands-clasped.mp4`. Whichever shots block
correctly get a 720p run next (50 steps if hands/faces need it, else 30) — that's a separate go.

## 4 · Housekeeping in the same session (no cost)

- `.env` append safety: yesterday's `Add-Content` glued `WAN_VACE_ENDPOINT_ID` onto the secret line because the
  file had no trailing newline. From now on append with a guaranteed newline first:
  `if ((Get-Content .env -Raw) -notmatch "\r?\n$") { Add-Content .env "" }; Add-Content .env "KEY=value"`.
  Verify `.env` now has each key exactly once and every line is `KEY=value` (report key names + value lengths only).
- Commit with the run: `git add prompts/mazhai CC-DISPATCH-phase4b-vace-480p-2026-09-22.md` ;
  `git commit -m "phase4b: VACE -v2 prompts (explicit camera/framing), 480p blocking runs"` ; `git push`.
  outputs/ stays untracked.

## 5 · Not in this dispatch

- 720p keepers, I1 two-shot, frame interpolation / upscaling (post step, after a shot is approved).
- Any change to steps/guide_scale/shift beyond the 30-step blocking runs.
