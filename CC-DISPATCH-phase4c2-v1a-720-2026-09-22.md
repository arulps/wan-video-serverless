# CC-DISPATCH — Phase 4c.2: V1a keeper at 720p (2026-09-22)

**Repo:** `C:\Projects\opencode\video_image` · endpoint `wan-vace-serverless` · no deploy, no code change.
**Cost:** one 720p / 30-step clip with 2 refs, ~25 min H100 (~$1.8). Stop after it.

## 0 · Frame check of 4c (`outputs\vace\_qc\phase4c-*.png`)
- **V2c-minnu-720 = KEEPER.** Turn from window to camera, hands clasped, big open eyes, pigtails + bows, dungarees
  with pocket and buttons; face is as close to `Minnu\front.png` as OpenArt's, arguably closer. 1919 s sampling
  (4 refs add 4 latent frames → more tokens than the 1-ref run; expect ~25 min with 2 refs).
- **V1a-mintu-480-v3 blocks correctly now.** Profile at the glass, both palms on the pane, rises on tiptoe, rain on
  the window, room matches. The OpenArt pose frame as reference #2 did it (and carried the room, which is a bonus for
  cross-shot consistency). Slightly darker grade than OpenArt — acceptable; judge again at 720p.

## 1 · Run
```
cd C:\Projects\opencode\video_image
powershell -ExecutionPolicy Bypass -File scripts\vace_shot.ps1 `
  -Refs "C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Mintu\Gemini_Generated_Image_fxwpvvfxwpvvfxwp.jpeg","outputs\vace\refs\oa-v1a-mintu-at-glass-f50.png" `
  -Label v1a-mintu-720-v3 -Size "1280*720" -Steps 30 -PromptFile prompts\mazhai\V1a-mintu-at-glass-v3.txt -NegativePromptFile prompts\mazhai\NEGATIVE-v1a.txt
```
Same seed (30313) so the blocking should reproduce the 480p result at higher resolution.

## 2 · Report, stop
Meta (`t_sample_s`, `t_total_s`), path, 5-frame strip into `outputs\vace\_qc\v1a-720-v3-strip.png`. Commit nothing
new except this dispatch. Phase 4d (speed: distillation LoRA / flash-attn / TeaCache) is written separately by Fable
before the remaining ten shots are run — at ~$2 a clip we don't shoot the whole song on this configuration.
