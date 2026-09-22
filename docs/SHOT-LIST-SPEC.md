# Shot list spec — what a song's shot list must contain for `comfy/batch_runner.py`

One song = one folder `songs/<song-slug>/` in this repo (or anywhere; paths in the list may be absolute):

```
songs/<song-slug>/
  shots.csv                 # the list (this spec)
  world.txt                 # line 1 = the PLACE clause (e.g. the runsheet's INTERIOR clause); blank line; then the WORLD block — one place, pinned for every shot
  style.txt                 # STYLE block (defaults to prompts/mazhai style if absent)
  negative.txt              # NEGATIVE (defaults to prompts/mazhai/NEGATIVE.txt)
  characters.txt            # optional: song-only cast, "Name: lock line..." per character (adds to / overrides PROMPT-PLAYBOOK §8 for this song)
  shots/<shot_id>.txt       # structured shot file (ATMOSPHERE / ANGLE / SHOT / POSE / MOTION / NEGATIVE) — see below
  refs/<name>.png           # character sheets and pose references, 1280x720, white padding
```

## shots.csv — columns (UTF-8, header row required)

| column | required | meaning |
|---|---|---|
| `shot_id` | yes | e.g. `I0`, `V1a`, `V2c`. Used for file names; unique. |
| `cast` | yes | `none`, or one or more character names joined with `+` (`Minnu`, `Mintu`, `Minnu+Mintu`, `Appa+Minnu`, ...). Each name must have a `Name:` lock line in `docs/PROMPT-PLAYBOOK.md` §8 (standing cast) or in the song's `characters.txt`; lock lines are emitted in the order listed, deduped. An unknown name is a hard error at dry-run. |
| `ref` | yes unless cast=none | reference sheet path (one image, 1280x720), built with `comfy/make_ref_sheet.py` — only the characters in this shot (1–3 ideal, 4 max; see playbook §3b). `--dry-run` reports sheets that do not exist yet. cast=none with no ref = text-to-video (establishing shots, rain detail); a room frame may still be given for continuity. |
| `prompt` | yes | path to the shot paragraph file, e.g. `shots/V1a.txt` |
| `duration_s` | no | target seconds; converted to frames `4n+1` at 16 fps (5.0 → 81). Default 81 frames. |
| `steps` | no | default 6 (distilled). 4 for blocking tests. |
| `cfg` | no | default 1.0 (distilled LoRA). 1.5–2.0 only when adherence needs help (costs 2×). |
| `seed` | no | default: song seed from `batch_runner --seed`; set per shot only for retakes. |
| `size` | no | `1280x720` (default) or `832x480` for blocking tests. |
| `world` | no | per-shot world file (e.g. `world-snow.txt`) when this shot's place differs from `world.txt`. One place per shot, pinned, never described loosely. |
| `negative` | no | per-shot negative file (e.g. the T-pose negative for shots starting from the turnaround). |
| `status` | runner | `pending` / `done` / `failed` — written by the runner; leave blank. |
| `notes` | no | free text for the editor (e.g. "cut at 3.5 s", "ping-pong ok"). |

Example:
```
shot_id,cast,ref,prompt,duration_s,steps,cfg,seed,size,negative,status,notes
I0,none,,shots/I0.txt,5,6,1.0,,1280x720,,,empty room push-in
V1a,Mintu,refs/mintu-2ref-16x9.png,shots/V1a.txt,5,6,1.0,,1280x720,negative-v1a.txt,,
V2c,Minnu,refs/minnu-4view-16x9.png,shots/V2c.txt,5,6,1.0,,1280x720,,,
V3a,Minnu+Mintu,refs/both-16x9.png,shots/V3a.txt,5,6,1.0,,1280x720,,,two-shot
```

## Shot file format — `shots/<shot_id>.txt` (this is what the planning session writes)
KEY: value lines; a value may wrap onto following lines. Every key is optional but a shot without ANGLE and SHOT
will block wrong (learned on V1a). The runner assembles them in the order that produced the keepers:

```
ATMOSPHERE: rain running down the window glass, grey rainy sky outside, cool grey daylight from the window
ANGLE: the camera stands across the living room, facing the window, at a child's eye height, locked off, no camera movement
SHOT: medium-wide shot — whole body from the top of the head to the shoes, room above the head, never crop the head, hands clearly visible
POSE: Mintu stands right against the glass in three-quarter profile so one cheek and eye are visible; both palms pressed flat on the inside of the pane at shoulder height; NOT facing the camera, arms NOT spread
MOTION: he rises slowly onto tiptoe keeping both palms on the glass, looks out at the rain with a hopeful pleading face, one small blink; slow, gentle motion only
NEGATIVE: T-pose, arms spread wide, arms outstretched, facing the camera
```
- `ATMOSPHERE` goes first **and is repeated after MOTION** — the distilled sampler (cfg 1.0) drops weather and mood
  unless it is said twice; the pod runs lost the rain this way.
- `ANGLE` = where the camera is and what it faces; `SHOT` = shot size and what must be in frame (the runsheet's
  "medium shot … locked off at child height" split into its two halves); `POSE` = the start pose and contact, with
  explicit NOT-lines when the reference pose is strong; `MOTION` = the one or two slow actions of the 5 s.
- `NEGATIVE` is prepended to the song's negative file for this shot only (pose guards live with the pose).
- A file that does not start with a `KEY:` line is used verbatim as a paragraph (old-style prompts still work).

## characters.txt — song-only cast
Same format as the playbook's §8: `Name: lock text…` (a wrapped entry continues on the next lines until the next
`Name:`; `#` lines are comments). Put a song's guest characters here (Appa, Thangam, an animal) rather than in
`world.txt`, so `cast` can name them and the lock line is emitted only for the shots they are in. A name that also
exists in §8 is overridden for this song only. Any number of characters; the per-shot limits (one sheet, 512 tokens
— `--dry-run` prints `~tokens=` per shot) are in the playbook §3b. Example:
```
Appa: father, mid-30s, short black hair, thick moustache, cream kurta, brown trousers, brown sandals — keep him
  exactly as in the reference image; do not restyle, recolour or resize.
```

## How the runner builds the prompt
`world.txt` line 1 (place clause) → assembled shot paragraph → `style.txt` → `world.txt` lines 2+ (WORLD block) →
CHARACTERS lock line(s) for `cast` (from `docs/PROMPT-PLAYBOOK.md` §8, plus the song's `characters.txt`) → `No text, no captions, no watermark.`
Negative = shot `NEGATIVE:` + (`negative` column file | `negative.txt` | `prompts/mazhai/NEGATIVE.txt`).
The runner never edits your words. `--dry-run` prints every assembled prompt without touching the GPU — run it before
every batch. A shot needing a different place (an outdoor verse) gets its own `world` column path: one place per shot,
pinned, never described loosely.

## What the runner produces
`songs/<song-slug>/out/<shot_id>-seed<seed>-s<steps>.mp4` (+ `.json` sidecar with timing and the exact prompt),
`out/_qc/<shot_id>-strip.png` (5 frames), and `shots.csv` updated with `status`. Re-running skips `done` shots;
retakes = change seed/prompt and clear the status cell.
