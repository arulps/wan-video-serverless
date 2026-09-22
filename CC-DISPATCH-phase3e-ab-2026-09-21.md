# CC-DISPATCH — Phase 3e: controlled A/B against OpenArt (2026-09-21)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** Claude Code on the laptop.
**Cost:** two 30-step clips on the existing 5B endpoint (~$0.25). No deploy, no code change, no commit
needed (outputs/ is untracked).

## 0 · Why this run exists

Fable compared the OpenArt rain-song shots (`songs\Mazhai- rain rain go away\03_V1a_mintu-at-glass.mp4`,
`09_V2c_minnu-hands-clasped.mp4`) frame-by-frame against today's two waist-framed masters. See
`outputs\ladder\_qc\openart-vs-ours-2026-09-21.png` (rows: OpenArt Mintu, ours Mintu, OpenArt Minnu, ours Minnu).

Three differences, all at once, so nothing is isolated yet:

| | OpenArt (worked) | ours (drifts / claws) |
|---|---|---|
| start frame | character **inside a full lit room**, ~55 % of frame height, camera at child height | cut-out on a flat cream/grey canvas, 2/3 of the frame empty |
| prompt | ~150 words: INTERIOR clause + STYLE + WORLD + character lock + NEGATIVE (the runsheet blocks) | ~30 words, no world, no colour anchors; Wan's tuned default negative replaced by a short list |
| model | "Wan 3.0" on a hosted 14B-class tier, 1280×720, 5 s | Wan 2.2 **TI2V-5B**, 1280×704, 3.4 s |

Note the OpenArt frame 0 shows the **same T-pose turnaround** placed in the room — and there the arms
lower and the child turns cleanly. So the T-pose was never the problem.

This run removes differences 1 and 2 and keeps only 3: feed our 5B the **OpenArt first frame itself**
(character already in the room) with the **runsheet prompt blocks**. If the 5B then lowers Mintu's arms
and keeps five fingers, the model is fine and our start-frame/prompt pipeline was the fault. If hands
still claw and colours still drift, the 5B is the limit and Phase 4 (14B I2V) is justified.

## 1 · Inputs (already on disk, written by Fable)

- `outputs\ladder\ab\oa-mintu-f0-1280x704.png` — OpenArt V1a frame 0, centre-cropped 720→704
- `outputs\ladder\ab\oa-minnu-f0-1280x704.png` — OpenArt V2c frame 0, same crop

Both are exactly 1280×704, so pass `-NoFitToFrame` (no canvas, no bbox, no compositing).

## 2 · Run

```
cd C:\Projects\opencode\video_image

powershell -ExecutionPolicy Bypass -File scripts\step_ladder.ps1 `
  -Image "outputs\ladder\ab\oa-mintu-f0-1280x704.png" -Label ab-mintu -NoFitToFrame -SkipSelftest `
  -Prompt "INTERIOR SHOT. The camera is inside the living room. Mintu is inside the room, standing on the wooden floor in front of the window; the rain, the garden and the grey sky are outside, on the far side of the glass. Medium shot, camera locked off at child height. Mintu slowly lowers both arms to his sides, turns to face the window, rises on tiptoe and presses both palms against the inside of the glass, looking out at the rain with a hopeful pleading face. Mintu: boy, 3-4, black hair with a cowlick above the right brow, warm brown skin, green t-shirt with a dinosaur print, blue shorts, blue shoes; keep him exactly as shown, do not restyle, recolour or resize. Modern children's 3D animation, Pixar-soft, soft rounded shapes, smooth matte surfaces, vibrant saturated colours, soft even indoor daylight with a gentle warm rim light from a lamp, shallow cinematic depth of field. Slow natural motion, camera steady." `
  -NegativePrompt "on-screen text, letters, subtitles, captions, watermark, logo, additional people, photorealism, live action, lightning, storm, fast camera shake, whip pan, strobing, character outside the window, zooming out, shrinking, colour shift, deformed hands, extra fingers, missing fingers, blurry, 色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走"

powershell -ExecutionPolicy Bypass -File scripts\step_ladder.ps1 `
  -Image "outputs\ladder\ab\oa-minnu-f0-1280x704.png" -Label ab-minnu -NoFitToFrame -SkipSelftest `
  -Prompt "INTERIOR SHOT. The camera is inside the living room. Minnu is inside the room, standing on the wooden floor in front of the window; the rain, the garden and the grey sky are outside, on the far side of the glass. Medium shot, camera locked off at child height. Minnu slowly lowers both arms, turns away from the window toward camera with a hopeful pleading expression, clasps her hands, and gives one small impatient bounce on her toes, pigtails bouncing. Minnu: girl, 3-4, jet-black hair in two pigtails with red ribbon bows, warm brown skin, violet dungarees over a cream t-shirt, white canvas shoes; keep her exactly as shown, do not restyle, recolour or resize. Modern children's 3D animation, Pixar-soft, soft rounded shapes, smooth matte surfaces, vibrant saturated colours, soft even indoor daylight with a gentle warm rim light from a lamp, shallow cinematic depth of field. Slow natural motion, camera steady." `
  -NegativePrompt "on-screen text, letters, subtitles, captions, watermark, logo, additional people, photorealism, live action, lightning, storm, fast camera shake, whip pan, strobing, character outside the window, zooming out, shrinking, colour shift, deformed hands, extra fingers, missing fingers, blurry, 色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走"
```

The Chinese tail is Wan's own default negative prompt (`wan/configs/shared_config.py`), which our
short English negative had been *replacing*; appending it restores the tuned default. If PowerShell
mangles the Chinese, put both prompts in UTF-8 files and pass `-Prompt (Get-Content -Raw -Encoding UTF8 <file>)`.

Two jobs = two workers in parallel (endpoint max 3); ~8 min wall clock.

## 3 · Report

For each clip: the meta JSON (`gpu`, `t_sample_s`, `vae_decode_*`, `delivery`) and the file path.
Then produce the same 5-frame strip Fable made (frames 0, 20, 40, 60, 80) so the comparison is like-for-like:

```
ffmpeg -y -i outputs\ladder\<clip>.mp4 -vf "select='eq(n,0)+eq(n,20)+eq(n,40)+eq(n,60)+eq(n,80)',tile=5x1" -vsync 0 outputs\ladder\_qc\<label>-strip.png
```
(if ffmpeg isn't on PATH, say so — Fable will strip them from the masters instead.)

Do **not** interpret the result; Arul and Fable judge. What decides Phase 4: five fingers held through the
arm-lowering, hair/skin colour unchanged at frame 80, no dolly-out.

## 4 · Not in this dispatch

- Any change to `step_ladder.ps1`, the worker, or the endpoint.
- Phase 4 (i2v-A14B on an 80 GB endpoint) — only after this A/B says the 5B is the limit.
