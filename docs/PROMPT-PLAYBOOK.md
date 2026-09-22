# Prompt playbook for VACE-14B (distilled, ComfyUI) — what worked, what didn't, 2026-09-21/22

Read this before writing any shot paragraph. Every rule below cost a paid clip to learn.

## 1 · The model is literal about the camera
"Back three-quarters to camera, camera at child height" produced an over-the-shoulder shot with the head cropped.
State three things explicitly in every shot paragraph, in this order:
1. **Camera placement** — "the camera stands across the room, facing the window, at a child's eye height, locked
   off, no camera movement."
2. **Framing** — "medium-wide: whole body from the top of the head to the shoes, with room above the head; never crop
   the head" (or "medium: head to knees"). If hands matter, say "hands clearly visible".
3. **Contact and pose** — "both palms already pressed flat on the inside of the glass at shoulder height".
   Say what is NOT wanted when the reference pose is strong: "NOT facing the camera, arms NOT spread out".

## 2 · The reference pose leaks
A single T-pose reference makes the character stand facing camera with arms spread. Fixes, in order of strength:
- add a **pose reference** to the sheet: a frame of the character (from an approved clip) already in the target pose
  — `mintu-2ref-16x9.png` (lawn front view + OpenArt V1a frame) fixed V1a in one try;
- the explicit NOT-lines above; a per-shot negative (`T-pose, arms spread wide, arms outstretched, facing the camera`)
  — note negatives are weak at cfg 1.0;
- plan shots so the first beat is a natural pose (standing at a window, sitting, back view) rather than a pose change.

## 3 · Multi-view references
Native ComfyUI takes ONE reference image and centre-crops it to the output aspect — sheets must be exactly 1280×720
with white padding (`comfy/make_ref_sheet.py`). Four views (front/back/left/right) held Minnu's identity; one lawn
front view held Mintu's. Two characters in one shot: both sheets side by side in one 1280×720 image.

## 3b · Big casts (5+ characters in a song)
The song can have any number of characters (`songs/<slug>/characters.txt` + the `cast` column take any list), but
**a shot should not**. Two hard limits sit behind the runner's warnings:
- **One 1280×720 sheet per shot.** `make_ref_sheet.py` wraps 5–8 images onto two rows, but every extra tile makes
  every tile smaller; it warns under ~300 px. Put on the sheet only the characters that are in *that* shot — 1–3
  is the sweet spot, 4 the ceiling. Sheets are per shot, not per song: `refs/appa-minnu-16x9.png`,
  `refs/family-wide-16x9.png`.
- **512 text-encoder tokens — a hard budget, not a guideline.** Wan was trained with a 512-token umt5 context.
  The official Wan code truncates there; ComfyUI sends the whole prompt, so an over-long one is not cut — it is
  outside the trained range and every detail gets a thinner slice of attention (the "rain disappeared" mechanism).
  The runner estimates tokens at **1.7 per word** (measured on the pod with the real umt5 tokenizer, 2026-09-22:
  283 words → 472 tokens, 322 → 558; ±2 %), prints `~tokens=` in `--dry-run`, and **refuses to submit an
  over-budget shot** (`--allow-long` overrides). Aim for ≤ 490 estimated. The first two planned songs came in at
  530–1090 tokens per shot before trimming, so plan to these budgets from the start (words):

  | block | max words | notes |
  |---|---|---|
  | `world.txt` line 1 (place clause) | 20 | where the camera is and where the characters may be — one sentence |
  | assembled shot paragraph (ATMOSPHERE ×2 + ANGLE + SHOT + POSE + MOTION) | 100 | ATMOSPHERE ≤ 12 words since it is said twice; NOT-lines count |
  | `style.txt` | 25 | the look in one breath |
  | `world.txt` lines 2+ (WORLD block) | 55 | only the set elements a shot can see or touch |
  | each character lock line | 25 | the reference sheet carries the identity; the lock line names the 4–5 non-negotiables + "keep exactly as in the reference image" — the song's `characters.txt` overrides §8's longer lines |
  | cast per shot | 3 | three locks ≈ 130 tokens; a 4th does not fit |

  That totals ≈ 470 tokens with three characters. Fixes when a shot is still over: cut décor from WORLD first, then
  adjectives from POSE/MOTION, then a character from the shot — never the camera/framing lines.

## 3c · Two children in one shot — bind by outfit and position, not by name
S03 (Appa + Minnu + Mintu, blocking test 2026-09-22) rendered **two** people: Appa, and one child with Minnu's
pigtails and Mintu's dinosaur shirt. "Minnu" and "Mintu" are near-identical tokens and the lock lines are the last
thing in the prompt; two similar child tiles side by side on the sheet were read as one child. Rules:
- In POSE/MOTION refer to each child as **"the girl in violet dungarees" / "the boy in the green dinosaur t-shirt"**
  with a **position** ("in the bow", "left"); names belong in the lock lines only.
- Per-shot NEGATIVE for two-child shots: `two children merged, only two people, pigtails on the boy, dinosaur shirt
  on the girl`, and say "all three people" / "three separate people" in SHOT.
- On the sheet keep the two children apart — an adult or the animal between them (`minnu-appa-mintu-16x9.png`)
  is the A/B being tested; if it wins it becomes the rule for every kids+someone sheet.
- Negatives only bite at cfg > 1: two-child shots run at cfg 1.5 if the cfg-1 pass merges them.

## 3d · Expressions the model does not do on its own (the wink)
T09a at 4 steps / cfg 1.0 blinked both eyes and opened the mouth — a symmetric blink is the model's default, and
at cfg 1.0 every negative ("both eyes closed", "open mouth") is ignored. Identity, world and framing were perfect.
Order of fixes: (1) 6 steps / cfg 2.0 with the wink negatives active and the asymmetry spelled out ("only his left
eye closes … right eye stays wide open and round"); (2) a second seed; (3) if still a blink: VACE first/last-frame
keyframes — frame 0 = the neutral frame from the passed clip, frame 80 = a wink keyframe painted from that frame
(Gemini image edit), fed as `control_video` + `control_masks` so the model only in-betweens. Two reference tiles of
the same character (neutral + wink) also produced a stray second pair of wings by the door — one identity tile plus
the expression tile is the most a sheet should carry, and "extra wings, sleeves" go in that shot's NEGATIVE.

## 3e · What the distilled sampler will not do (4g A/B, 2026-09-22)
Measured on T09a and S03 at 832×480, six rows:
- **cfg 2.0 removed the expression entirely** — no wink and no blink; cfg 1.0 gives a symmetric blink. The negative
  prompt does not create asymmetry at any cfg the distilled LoRA tolerates.
- **Two tiles of the same character** (neutral + wink) rendered a ghost second TV set at seed 4242 (both cfg 1 and 2).
  One identity tile per character on a sheet; an expression is not a pose reference for this model.
- **Appa between the children** fixed the head count (3 people, correct seats) at cfg 1.0 and 1.5 — that rule stands.
  But the boy still got the girl's pigtails and bow, and both children held oars against POSE and the negative:
  identity of two look-alike children and "hands on the gunwales" did not survive cfg 1.5 either.
- The `mode` column therefore exists: `full` = no LoRA, 30 steps, cfg 5, uni_pc — the 4d control config, ~8× slower
  (~4 min at 480p, ~10–12 min at 720p on an A100). It is the next lever for exactly these three failure types; if
  full sampling also fails, the lever after it is VACE keyframes (§3d step 3) — a composed first frame with the right
  two children, or a painted wink frame, and the model only in-betweens.
- Cheap distilled lever still worth one row: cast order — the lock line that comes last loses first, so the
  character whose identity slipped goes first in `cast`.

## 4 · Distilled sampling (lightx2v LoRA): 4–6 steps, cfg 1.0, shift 5, lcm/simple
- 4 steps is clean; 6 is a touch smoother. Never needed 30 again.
- At cfg 1.0 the negative prompt is ignored and adherence to secondary details drops: **the rain disappeared** from
  both pod clips. Put atmosphere/weather in the FIRST sentence of the shot paragraph and repeat it once ("rain running
  down the window glass, grey rainy sky outside"). If it still drops out, run 6 steps at cfg 1.5–2.0 (≈2× time).
- Last 3–4 frames can drift (arms opening) — trim the tail on the timeline; generate 5 s to keep 4.5 s.

## 5 · One room per song
Every shot invents its own room unless the WORLD block is identical and pinned. Keep `world.txt` verbatim across
shots, same seed for the song, and put a room reference frame into the sheet for shots where continuity matters
(the OpenArt frame carried its room into V1a). Cutting between two different living rooms breaks a preschooler's
sense of place — the runsheet's "WORLD rendered well in clip 1 — keep it verbatim" is the rule.

## 6 · Shot design that suits the model
- Small, slow motions: turn, look, blink, clasp hands, press palms, breathe, hair/bows sway. These are clean.
- Avoid: pose changes across the clip (T-pose → arms down), fast waves, walking through frame, props exchanged.
- 5 s per shot, cut on the beat; 12–13 shots per 60 s song (the Mazhai cut plan is the template).
- No-character shots (rain detail, toys on the rug, establishing push-in) are cheap and hide edits — use them.
- Text, captions, logos never in the generation; they go on in the edit.

## 7 · Test cheap, shoot once
Blocking at 832×480 / 4 steps (~1–2 min, cents); keepers at 1280×720 / 6 steps. Same seed reproduces the blocking
at the higher resolution.

## 8 · Character lock lines (append for the cast)
Mintu: little boy, 4–5, black hair with a cowlick above the right brow, warm brown skin, green t-shirt with a dinosaur
print, blue shorts, blue shoes — keep him exactly as in the reference image; do not restyle, recolour or resize.
Minnu: girl, 6–8, jet-black hair in two pigtails with red ribbon bows, warm brown skin, violet dungarees over a cream
t-shirt, white canvas shoes — keep her exactly as in the reference image; do not restyle, recolour or resize.
