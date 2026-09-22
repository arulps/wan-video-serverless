# CC-DISPATCH — Twinkle Twinkle + Row Row Row: commit, sheets, first two blocking shots (2026-09-22, rev 2)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC. Rev 1 (Opus planning session) is superseded by this file;
Fable merged both sessions' runner changes, found every planned shot 1.3–2× over the text-encoder budget, re-cut the
shared prompt blocks to fit, and verified all three dry-runs. Nothing is committed yet.
**Order of work:** this dispatch runs **after Part A of `CC-DISPATCH-phase4e-batch-2026-09-22.md`** (models on R2,
fresh pod proven) — Part C of 4e (the `_selftest` batch) is replaced by §5 below, which proves the same plumbing on
real shots. **Budget for §5:** ≤ 20 min pod time (~$0.50).

## 1 · What is on disk now (all written by Fable, verified)
| file | state |
|---|---|
| `comfy/batch_runner.py` | **merged**: Opus's UTF-8 stdout fix, `characters.txt` per-song cast (`_parse_lock_lines` / `song_character_lines`, any `Name+Name` cast, deduped), `--dry-run` ref preflight (`!! REF MISSING`) **+** Fable's token budget: `~tokens=` per shot, `OVER BUDGET` refused before GPU time (`--allow-long` overrides), dry-run summary of over-budget shots |
| `comfy/make_ref_sheet.py` | 5–8 tiles wrap to two rows; warns when a tile < 300 px |
| `docs/PROMPT-PLAYBOOK.md` | §3b big casts + **the word budgets table** (place 25 / shot 120 / style 30 / world 70 / lock 30 / cast ≤ 3) |
| `docs/SHOT-LIST-SPEC.md` | `world` column, `characters.txt`, cast = any names, ref preflight |
| `songs/twinkle-twinkle/` | 21 shots, **re-cut to budget** (max ~494 est. tokens, was 650–1090); originals in `_untrimmed-2026-09-22/` |
| `songs/row-row-row-your-boat/` | 21 shots, **re-cut to budget** (max ~472, was 530–925); Mintu/Minnu 30-word overrides in `characters.txt`; **new `world-jetty.txt` for S01** (the shared guard says "boat never empty" — S01 is the empty boat; `shots.csv` S01 `world` column set); originals in `_untrimmed-2026-09-22/` |
| `scripts/build_song_refs.py` | Opus's sheet builder (16 sheets, rembg on the 4 sources with backgrounds); all 24 source paths verified to exist on this machine |
| `scripts/pod_bootstrap.sh` | from 4e — R2 model origin |

Why the re-cut: Wan was trained with a 512-token umt5 context. ComfyUI does not truncate, it sends the whole prompt,
so an 900-token prompt is out of the trained range and every detail (the lock lines last of all) gets a thinner slice
of attention — the same mechanism that lost the rain in 4d. The runner now refuses such shots. What was removed is
listed per song in §7 so Arul can veto; every ANGLE/SHOT/POSE fact, NOT-line, negative and place-clause guard was kept.

## 2 · Verify (no GPU)
```
python comfy\batch_runner.py --song songs\_selftest             --hosts http://x --dry-run
python comfy\batch_runner.py --song songs\twinkle-twinkle       --hosts http://x --dry-run
python comfy\batch_runner.py --song songs\row-row-row-your-boat --hosts http://x --dry-run
```
Expected: 2 / 21 / 21 shots, exit 0, **no `OVER BUDGET` lines**, max `~tokens=` 461 / 494 / 472, and every character
shot listed under `REF MISSING` (sheets not built yet — that is the point of the preflight).

## 3 · Cleanup + commit
1. `songs/twinkle-twinkle/shots/` still holds 23 orphaned bedroom-draft files not referenced by `shots.csv`
   (`A1 A2 B1a B1b B2a B2b C1a C1b C2a C2b C2c I0 I1 I2 I3 O1 O2 R1a R1b R2a R3a R4a R4b`.txt). Delete them (they are
   untracked; plain delete, nothing to `git rm`).
2. `git status`; confirm no `.env`, `logs.txt`, `nil`, `outputs/cutouts`, `songs/*/out/`, `songs/*/refs/` in the set
   (refs are built artefacts — keep them untracked until a sheet is approved; then commit the approved sheets).
3. Commit:
```
git add comfy/ docs/ scripts/build_song_refs.py scripts/pod_bootstrap.sh songs/_selftest songs/twinkle-twinkle songs/row-row-row-your-boat CC-DISPATCH-songs-twinkle-row-2026-09-22.md CC-DISPATCH-phase4e-batch-2026-09-22.md CC-DISPATCH-phase4d-comfy-pod-2026-09-22.md outputs/vace/pod/_qc
git commit -m "songs: Twinkle Twinkle + Row Row Row re-cut to the 512-token budget; per-song cast; token gate; R2 bootstrap

batch_runner: characters.txt per song layered over PROMPT-PLAYBOOK section 8; cast = any Name+Name;
--dry-run preflights reference sheets; ~tokens estimate per shot and OVER BUDGET shots refused before
GPU time (--allow-long); UTF-8 stdout on Windows.
make_ref_sheet: multi-row sheets for 5-8 tiles with a small-tile warning.
docs: word budgets per prompt block (playbook 3b); world column, characters.txt in the spec.
songs/twinkle-twinkle: 21 shots, terrace at night, cast Mintu/Minnu/Thangam/Minmini.
songs/row-row-row-your-boat: 21 shots; Appa + animals in characters.txt; S01 gets world-jetty.txt.
scripts/build_song_refs.py: 16 sheets with background removal on the 4 sources that carry one.
scripts/pod_bootstrap.sh: Cloudflare R2 as the model origin for pods (phase 4e rev 2)."
git push
```

## 4 · Build and LOOK at the sheets (laptop, no GPU)
```
pip install rembg onnxruntime
python scripts\build_song_refs.py
python comfy\batch_runner.py --song songs\twinkle-twinkle --hosts http://x --dry-run      (REF MISSING list must be empty)
python comfy\batch_runner.py --song songs\row-row-row-your-boat --hosts http://x --dry-run
```
Open every sheet in `songs\*\refs\`. Report (attach) these four before spending anything:
`twinkle-twinkle/refs/minmini-wink-16x9.png`, `twinkle-twinkle/refs/kids-thangam-16x9.png`,
`row-row-row-your-boat/refs/appa-mintu-minnu-16x9.png`, `row-row-row-your-boat/refs/kids-chiku-16x9.png`.
Check: rembg left no halo/holes on Thangam, Modhu, Singa, Minmini (grey studio bg is the risky one); the three-tile
sheets keep faces ≥ ~300 px tall (the script warns otherwise); the T-pose Chiku source is the only T-pose in any sheet.
If a cut-out is bad, fix that one source (crop tighter, or `--no-cut` with a hand-cut PNG dropped into
`outputs\cutouts\<key>.png`) and rebuild — do not proceed with a bad sheet.

## 5 · First two blocking shots on the fresh pod (replaces 4e Part C)
On the pod from 4e Part A (`bash pod_bootstrap.sh pull` done, ComfyUI ready), after `wan-push` from the laptop so the
songs + sheets are on R2:
```
cd /workspace/wan
python comfy/batch_runner.py --song songs/twinkle-twinkle --hosts http://127.0.0.1:8188 --only T09a --dry-run
python comfy/batch_runner.py --song songs/twinkle-twinkle --hosts http://127.0.0.1:8188 --only T09a --seed 30313
python comfy/batch_runner.py --song songs/row-row-row-your-boat --hosts http://127.0.0.1:8188 --only S03 --seed 30313 \
    --max-minutes 20 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/row-row-row-your-boat && bash /workspace/pod_bootstrap.sh out-push songs/twinkle-twinkle && runpodctl stop pod $RUNPOD_POD_ID"
```
**Before running, set both rows to blocking settings in the CSVs** (`size` `832x480`, `steps` `4`) — the CSV rows are
at production 1280×720/6 steps; edit the two cells, run, then put them back and clear `status` so the keepers rerun
later at full size with the same seed. Expect ~1–2 min each warm.
- **T09a** = the mascot wink, the brand shot and the fragile expression (the sheet pairs neutral + wink, the §2
  pose-reference trick). Pass = left eye winks, right eye stays open, screen face readable, no children in frame.
- **S03** = the look-lock and the first 6.3 s clip (101 frames; everything proven so far is 81). Pass = boat centred
  and still while banks slide, three heads uncropped, Appa rowing slowly, children's identities held.
Report both strips (`out/_qc/*-strip.png`) + sidecar JSONs + wall times, and the **real umt5 token count** of one
sidecar prompt (the 4e §6 recipe) so the 1.4/word estimate can be calibrated.
If S03 at 101 frames fails on motion/coherence while T09a passes, the fallback is 81 frames (5.06 s) for the whole
song and cutting the audio grid to 5 s beats — say so in the report, do not retry with other settings.

## 6 · Not in this dispatch
- The other 40 shots. They wait for Fable's frame check of the two above.
- `charecter bible\generation-refs-2026-08-31\Appa\` is a second Appa set in the same style as the kids' refs; the
  plan uses the four-view `Turnarounds\Dad` instead. If Appa's identity drifts in S03, the bible set is the A/B.
- `songs\Twinkle Twinkle\v2-mintu-terrace-set.png` (a terrace set plate) is not in any sheet; adding it as a tile is
  the §5 continuity experiment for later, not now.

## 7 · What the re-cut removed (veto list for Arul)
**twinkle-twinkle** — WORLD: slate-blue tiled roof; lattice panes on the glass door; round window above the door and
arched side window; terracotta topiary pot and low bush (T01 POSE no longer names the topiary); ball finials on the
balustrade; "raised" deck; the village's fruit trees, palms, hills; sky "graduating to violet"; adjectives drifting /
soft / pale. Sky world: pink clouds; stars "of varying sizes". Place clause: the "far above and beyond the railing"
sentence (WORLD still says "far below"). Style: "YouTube widescreen", "no sharp edges", the lamp rim-light phrase,
"stepped or stop-motion" (negative covers it). **Thangam lock** keeps: small cartoon star, butter-yellow, big glossy
black eyes, stubby arms, no legs, always floats, never stands. **Minmini lock** keeps: firefly, cream television-set
head, face on screen, pale teal body, golden antennae, amber wings, yellow-green tail lantern, grey feet. Shots: only
adjectives/restatements; biggest cuts — T09a "dark grey screen surround", T08 "soft pool of light" → "lighting the
rail", T15 Minnu's pigtails swinging, T16 "eyes wide", T17 "heads to waists" framing wording.
**row-row-row-your-boat** — guard wording compressed (water/banks no longer named in the guard; "no child in the
water or on the bank" stays). WORLD: the big shady tree; golden: round bushes, "warm and content"; grass: bushes,
"a few" rocks; snow: bare snowy trees, "small" puffs of breath; channel: "tiny and secret" → "everything oversized".
Style: rim-light phrase (clashed with golden/snow), "no sharp edges", "stepped or stop-motion". **Appa** keeps: South
Indian, mid-30s, short jet-black hair, neat moustache, golden-brown skin, black-and-white checked shirt, navy trousers.
**Modhu/Singa/Karadi/Chiku** lose "walks on four legs", paws/tails/whiskers/nose details (kept where a shot's MOTION
names them). **Mintu/Minnu overrides** drop "cowlick above the right brow" → "cowlick", "dinosaur print" → "green
dinosaur t-shirt", the shoes, "in two" pigtails. Shots: S04 "already under the leafy arch"; S05 Minnu's start turn;
S06/S07/S10/S14/S18 "only the near gunwale shows" (the "Appa out of frame" guard stays); S18 Chiku's ears/whiskers in
the start pose (MOTION keeps them; all T-pose NOT-lines and his NEGATIVE kept).
Anything vetoed goes back by editing that block and re-running the dry-run — the budget line tells you what it cost.
