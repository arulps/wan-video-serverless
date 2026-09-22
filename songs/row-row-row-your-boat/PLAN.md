# ஓட்டு ஓட்டு ஓடத்தை / Row Row Row Your Boat — VACE run sheet

Re-plan of `ROW-ROW-ROW-YOUR-BOAT_Gemini-Director-Pack.md` for VACE-14B distilled.
The Director Pack's **measured song map is kept exactly**; the shot craft is rewritten,
because the Veo pack asks for most of what playbook §6 says this model cannot do.

    python comfy\batch_runner.py --song songs\row-row-row-your-boat --hosts http://unused --dry-run

## 1 · Audio — Tamil is the master

`14.1s Recording (Aug 29 @ 12_25 p.m.) (Remix).mp3` — **123.560 s** · 79.96 BPM ·
bar 1.5006 s · **8-bar verse = 12.0047 s**. Ten 12 s cycles plus a 1.347 s pickup and a
2.17 s tail. Cycles 0/3/5/7 are instrumental, 1/2/4/6/8/9 are sung — verified by ear with
`STRUCTURE-CHECK first4=claimed-instrumental last4=claimed-sung.mp3` in the song folder.
**36 of the 123.6 s have no lyrics at all.** `adventure on river english (2).wav` is the
English cut and is a different length — a second edit, not an audio swap.

21 shots on 6.002 s boundaries (half a verse = a 4-bar phrase), so every cut lands on the
music by construction. Generate 6.3 s (101 frames at 16 fps), **trim to 6.002 s** — playbook
§4: the last 3–4 frames drift.

| shot | sound | window | peak |
|---|---|---|---|
| S06 | crocodile → scream | 35.56–36.25 | 35.71 |
| S10 | lion → roar | 59.47–60.50 | 59.71 |
| S14 | polar bear → shiver | 83.60–84.60 | 83.63 |
| S18 | mouse → squeak | 107.50–109.20 | 107.64 (rings to ≈111.2 — let it bleed into S19) |

## 2 · What changed from the Veo pack, and why

| Veo pack asked for | Playbook says | What this plan does |
|---|---|---|
| boat moving across frame, camera tracking | avoid moving through frame | **camera tracks at exactly the boat's speed** — the boat is static in frame, the bank slides past. A move becomes parallax. Twelve shots depend on this. |
| walk down the bank, board the boat, Appa lifts Mintu in | avoid pose changes, avoid props | S01 is the **empty boat at the jetty**, no people. S02 opens with all three **already seated**; the only motion is one push off the post. |
| arms up ×4, stand up and dance, roar back, shiver, squeak | avoid pose changes across the clip | every reaction shot **starts already in the reaction pose**. The clip is a sustain — hold the peak, shake with it, settle. The editor cuts in on the hit. |
| dance break — children stand up in the boat | small slow motions only | they stay seated and **pull imaginary oars in time with Appa**. Reads as a dance, costs no pose change. |
| in-shot transitions green→snow, green→channel | one place per shot, pinned | both rewritten as **single-place shots**; the biome change happens on a cross-fade in the edit. |
| four biomes in one song | one room per song | **five pinned world files**, each verbatim across its shots, selected by the `world` column. |
| "mouths moving as if singing" in the verses | no lip-sync | **mouths closed in every shot except the four SFX reactions**, which run on `negative-reaction.txt`. The OpenArt failure was mouths singing in instrumental sections; closing them everywhere removes the class of error. |

## 3 · The cast — now a real mechanism

`characters.txt` in this folder carries **Appa, Modhu, Singa, Karadi and Chiku**; Mintu and
Minnu come from `PROMPT-PLAYBOOK.md` §8. `batch_runner.py` layers the song's file over the
playbook and accepts any `Name` or `Name+Name+Name` in the `cast` column, so each lock line
appears **only in the shots that character is actually in** — confirmed by `--dry-run`.
The world files are place-only again: scenery plus the boat as a set piece, no character locks.

**Appa steps out of frame for the four money shots.** S06, S07, S10, S14 and S18 tighten onto
the two children and the animal. That keeps every sheet at three tiles *and* makes the beat
land harder — a wide with dad laughing in it dilutes exactly the moment the shot exists for.
Appa rows the verses and the interludes, which is where he belongs.

## 4 · The animal references, and the one trap in them

All four now exist in the song folder — S15 is no longer the highest-risk shot in the song.
But:

- **Modhu arrives in a jungle and Singa on a savanna.** A reference carries its own background
  into the shot (playbook §5, the same way the OpenArt frame carried the Mazhai living room into
  V1a). The savanna is *nearly* right for the golden-grass bank, which makes it more dangerous,
  not less. Both are cut out to white by `scripts/build_song_refs.py`. Karadi is already on clean grey.
- **Chiku is a T-pose, and Chiku is the only biped.** This is precisely the reference shape §2
  names as the thing that broke V1a. The three quadrupeds cannot really do it; the mouse can and
  will. S18 carries explicit NOT-lines in the POSE and `T-pose, arms spread wide, arms outstretched`
  in its own NEGATIVE, and the shot opens with his paws already under his chin — not a pose change into it.
- **`make_ref_sheet.py` scales every tile to a common height**, so a Chiku tile and a Singa tile
  come out the same size — the sheet actively says a mouse and a lion are the same scale. S18's
  POSE therefore states the scale in words: *"tiny — no bigger than Mintu's hand."*
- The **leaf umbrella is dropped** from S18. It was in the Veo pack, it is a held prop, and §6
  lists props among the things to avoid. The squeaking game is the beat; the umbrella is a re-roll.

## 5 · Before the first generation

```bat
pip install rembg onnxruntime
python scripts\build_song_refs.py --song row-row-row-your-boat
```
Six sheets: `appa-mintu-minnu` for the eleven rowing and interlude shots, one children+animal
sheet for each of the four reactions, and `animals-3up` for S15. **Look at them first** — three
tiles in 1280×720 is tight, and if Appa's face is too small to read, crop his tile to
head-and-shoulders and rebuild that sheet.

## 6 · Order of work

1. Build the sheets. `--dry-run`, read all 21 prompts; it now fails loudly on a missing sheet.
2. **Generate S03 alone at 832×480 / 4 steps.** The look-lock shot — all three in the boat in
   flat daylight, the tracking-alongside framing twelve other shots depend on, and Appa's first
   appearance. Check: does Appa hold from a three-up sheet? Does the boat stay static while the
   bank slides? Does one slow oar stroke read as rowing? **And check drift at 6.3 s** — every
   clip here is 26% longer than the proven 5 s, and if the last second falls apart the fallback
   is 3-bar shots and a re-cut, so find out now.
3. Then S06 at 480p — the first reaction and the first animal. If the scream-from-frame-0
   staging works, the other three will.
4. Then S18 at 480p — the T-pose reference. If Chiku still comes back facing camera with his
   arms out, add a pose frame from the S18 blocking run as a second tile (§2's strongest fix).
5. Full run at 1280×720 / 6 steps, same seed.

## 7 · Cut plan — 123.560 s

```
0.000-1.347   black, fading up with the music (no clip)
S01..S20      20 x 6.002 s                                    = 120.04 s
S21           first 2.17 s of a 6.3 s generation              =   2.17 s
                                                                ---------
                                                                123.56 s
```
Butt-joins land on 4-bar phrases by construction. If a cut feels harsh use a 6–8 frame dissolve
**centred** on the boundary — never move the boundary. Fade to black over the last 1.2 s of S21.
Mute all generated audio; lay the MP3 under; do not stretch or trim it.

Final QC: watch 37–49 s, 61–73 s and 85–97 s with sound on and confirm nobody is singing. With
mouths closed everywhere but the four reactions that should be structurally impossible.

## 8 · Known risks

- **6.3 s clips are untested on this pipeline.** Everything proven so far is 5 s. S03 finds out.
- **S15 puts Karadi on a warm green bank** with no cold cues, because the three animals gather to
  wave goodbye together. It is a deliberate continuity wobble carried over from the Veo pack, not
  an oversight — add a light frost note to its ATMOSPHERE if it reads wrong in the cut.
- **The four animals have no turnarounds**, only the single three-quarter view each. Identity
  across their 2–3 consecutive shots should hold; a fourth appearance would be pushing it.
