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
