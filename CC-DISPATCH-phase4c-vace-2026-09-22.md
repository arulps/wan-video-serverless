# CC-DISPATCH — Phase 4c: V2c to 720p, V1a pose fix at 480p (2026-09-22)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** Claude Code on the laptop. Endpoint `wan-vace-serverless`.
**Cost:** V2c-v3 at 720p / 30 steps (~20–25 min H100, ~$1.5–1.8) + V1a-v3 at 480p / 30 steps (~8 min, ~$0.55).
No deploy, no worker change. Stop after both.

## 0 · What the 4b frame check said (`outputs\vace\_qc\phase4b-*.png`)

- **V2c-minnu-480 blocks correctly**: starts on a back view at the window, turns to camera, hands clasped, pigtails
  with red bows, dungarees, white shoes, room per WORLD — the same beat as OpenArt's V2c. Identity holds (pigtails,
  bows, dungarees, face shape); only flaw: her eyes are downcast mid-clip. → shoot it at 720p now.
- **V1a-mintu-480 blocks wrong in a new way**: face visible, whole body in frame, identity excellent (cowlick, two
  front teeth, dinosaur print) — but he faces the camera with arms spread and never touches the glass. The single
  T-pose reference is leaking its pose. → one more 480p try with a pose lock, a V1a-specific negative, and a second
  reference that carries the *pose*: OpenArt's own V1a frame (Mintu at the glass, profile), saved at
  `outputs\vace\refs\oa-v1a-mintu-at-glass-f50.png`.
- Timings: 480p/30 steps = 397 s (1 ref) and 482 s (4 refs) sampling on the H100.

## 1 · Files (written by Fable, on disk)

- `prompts\mazhai\V2c-minnu-impatience-v3.txt` — v2 + "looks straight into the camera with big open eyes".
- `prompts\mazhai\V1a-mintu-at-glass-v3.txt` — v2 + explicit pose lock (NOT facing camera, arms NOT spread, palms flat
  on the pane at shoulder height, three-quarter profile).
- `prompts\mazhai\NEGATIVE-v1a.txt` — NEGATIVE + "T-pose, arms spread wide, arms outstretched, facing the camera,
  looking at the camera, standing away from the window".
- `outputs\vace\refs\oa-v1a-mintu-at-glass-f50.png` — OpenArt V1a frame 50 (1280×720), used as reference #2 for V1a.

## 2 · Run

```
cd C:\Projects\opencode\video_image

# keeper candidate: V2c at 720p, 30 steps (30 was clean at 480p; 50 only if faces come back soft)
powershell -ExecutionPolicy Bypass -File scripts\vace_shot.ps1 `
  -Refs "C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\front.png","C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\back.png","C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\left.png","C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Minnu\right.png" `
  -Label v2c-minnu-720 -Size "1280*720" -Steps 30 -PromptFile prompts\mazhai\V2c-minnu-impatience-v3.txt -NegativePromptFile prompts\mazhai\NEGATIVE.txt

# blocking retry: V1a at 480p with the pose reference and the V1a negative
powershell -ExecutionPolicy Bypass -File scripts\vace_shot.ps1 -SkipSelftest `
  -Refs "C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Mintu\Gemini_Generated_Image_fxwpvvfxwpvvfxwp.jpeg","outputs\vace\refs\oa-v1a-mintu-at-glass-f50.png" `
  -Label v1a-mintu-480-v3 -Size "832*480" -Steps 30 -PromptFile prompts\mazhai\V1a-mintu-at-glass-v3.txt -NegativePromptFile prompts\mazhai\NEGATIVE-v1a.txt
```

Sequential, same warm worker. `-JobTimeoutMin 60` default covers the 720p run.

## 3 · Report, then stop

Per clip: meta (`t_sample_s`, `t_total_s`), path, 5-frame strip into `outputs\vace\_qc\` (same ffmpeg line as 4b).
Fable does the frame check. Then commit: `git add prompts/mazhai CC-DISPATCH-phase4c-vace-2026-09-22.md` ; commit
`"phase4c: v3 prompts, V1a pose lock + negative, V2c 720p"` ; push. `outputs/` stays untracked (the refs frame lives
under outputs/ on purpose — it is OpenArt output, not repo material).

## 4 · Not in this dispatch

- I1 two-shot; flash-attn wheel in the image (Phase 4d — the speed/cost lever, after the keepers exist);
  post-process step (RIFE 16→30 fps + upscale) — Phase 5, once a 720p keeper is approved.
