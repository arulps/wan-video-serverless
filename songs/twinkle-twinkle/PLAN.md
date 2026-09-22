# மின்னும் மின்னும் நட்சத்திரமே / Twinkle Twinkle — VACE run sheet

Terrace at night. Four characters: **Mintu, Minnu, Thangam** (the star) and **Minmini**
(the channel mascot). Written to `docs/SHOT-LIST-SPEC.md`; language follows
`MAZHAI-OPENART-RUNSHEET.md`; every rule in `docs/PROMPT-PLAYBOOK.md` applied.

    python comfy\batch_runner.py --song songs\twinkle-twinkle --hosts http://unused --dry-run

## 1 · Audio — Tamil is the master

| | |
|---|---|
| Master | `மின்னும் நட்சத்திரம்_4.mp3` — **151.201 s**, first audio 0.567 s |
| English | `மின்னும் நட்சத்திரம் english.wav` — **171.160 s** |
| Tempo | ~100.35 BPM for the first 100 s, easing to ~99.4 BPM by 140 s |
| Bar | 2.392 s · 2-bar 4.784 s · 4-bar 9.567 s |
| Lyrics | 9 couplets: R · A · R · B1 · B2 · R · C1 · C2 · R, plus a loopable intro and outro |

**⚠ The two masters are 20 s apart**, so unlike Mazhai one set of visuals will not carry
both cuts unchanged. Cut Tamil first; the English cut takes its extra ~20 s from the
ping-pong pool below, never from stretching.

**⚠ There is no frame-accurate music map for this track.** Autocorrelation peaks at only
r=0.23 (Row Row Row hit a single sharp maximum) and the tempo drifts ~1%, so a fixed phrase
grid accumulates ~0.7 s by the end. Cut by ear on the refrain entries. Shot lengths are nominal.

## 2 · The two decisions that remove the OpenArt failure mode

**Nobody sings on camera, in any shot.** Not "closed in the instrumentals and singing in the
verses" — closed everywhere, in all 21 shots. A lullaby does not need a moving mouth, and once
no shot depicts singing, the lyric-timing uncertainty above costs nothing: no shot is wrong if
it lands two seconds early. `negative.txt` bans `open mouth, talking, singing, lip-sync` for
the whole song, and the drowsy beat (T17) is written as **eyelids drooping, not yawning** — an
open mouth in this model reads as singing.

**Nothing ever leaves the deck but Minmini and Thangam.** The place clause is the terrace
equivalent of the Mazhai INTERIOR CLAUSE that fixed V1a: every child stays on the planks, the
sky is far above and beyond the railing, and no child is ever in the sky, on the railing or
on the roof. With a flying mascot and a floating star in the same song, that guard is load-bearing.

## 3 · The spine — மின் is both their names

மின்னும் (*that which flashes*), மின்மினி (firefly) and மின்னு share the root **மின்**. The
song's title word and the mascot's name are the same Tamil root, so the tail lantern blinking
is not a workaround for a hard shot — it is the title made visible. It runs the whole song:

| act | what the light does |
|---|---|
| 1 | Minmini dozing on the rail, lantern dim |
| 2 | the wink — lantern double-pulses, then the face winks, then he goes |
| 2→3 | in flight the lantern pulses in rhythm as he climbs |
| 3 | up at the star they pulse at each other, then together |
| 4 | both fading slower and slower, down to one ember on the rail |

**The wink is two shots, not one**, because the face and the tail are at opposite ends of the
character and cannot be read in one frame. T09a is the close-up face wink; T09b is the wide
tail double-pulse and launch. The tail reads at any distance and in silhouette so it carries
the wides and the whole flight; the face reads only in close, so it gets exactly one shot.

## 4 · Two pinned places

`world.txt` — the terrace deck, the mint cartoon house, the cream balustrade, the mat, and the
sleeping pastel village far below. `world-sky.txt` — open night sky only, with an explicit
"no ground, no horizon, no building and no person" guard. Selected per row by the `world` column.

## 5 · The staging rule — never more than three in a sheet

VACE takes ONE reference image and centre-crops it (playbook §3). Four tiles in 1280×720 makes
every face too small to hold. So no shot casts more than three. T15 is children + Thangam;
T18 and T20 are children + Minmini; the two of them are only ever in frame together in the sky
shots, where there are no children.

## 6 · Shots — 21

| block | shots | note |
|---|---|---|
| Act 1 · wondering | T01 T02 T03 T04 T05 | empty terrace, star field, both at the rail, close on Minnu, the sleeping village |
| Act 2 · the answer | T06 T07 T08 T09a T09b T10 | Thangam reveal, they wave back, Minmini wakes, **the wink**, the launch, the climb |
| Act 3 · two lights | T11 T12 T13 | the meeting, the diamond scatter, the widest shot |
| Act 4 · sleep | T14 T15 T16 T17 T18 T19 T20 | they descend, she settles on the rail, she touches his palm, the mat, asleep, the ember, the final hold |

**Ten of the 21 are low-risk**: 4 have no cast at all and 6 are a single non-human against open
sky. Thangam and Minmini are rigid, symmetrical, glowing and have no fingers — none of the
failure surfaces the negative list spends most of its length guarding against.

## 7 · Cut plan — Tamil, 151.201 s

```
0.000-0.567   black, fading up (no clip)
21 shots x 4.8 s trimmed from 5.0 s generated          = 100.8 s
+ ping-pong on the cheap shots (T02 T05 T13 and the
  two outro holds), ~4.0 s each, plus slow 5% push-ins =  ~50 s
                                                          --------
                                                          ~151 s
```
0.4 s cross-fades. **Ping-pong only shots with no child in them** — T02, T05, T13, and T19/T20
if their holds reverse cleanly. Children never reverse. For the English cut (+19.96 s), take a
second ping-pong on T02, T13 and the outro holds rather than stretching any picture.

## 8 · Before the first generation

```bat
pip install rembg onnxruntime
python scripts\build_song_refs.py --song twinkle-twinkle
```
Ten sheets, all from images already on disk. Thangam and Minmini are cut out first — the star's
pastel dawn-sky background and the mascot's grey studio background would carry straight into
the night, exactly as the OpenArt frame carried the Mazhai living room into V1a (playbook §5).

**`minmini-wink-16x9.png` is the important one**: neutral front *and* wink front in the same
sheet, identical framing, differing only in the eye. That is the playbook §2 pose-reference fix
— the thing that got V1a right in one try — applied to a facial expression. Without it, a
per-eye change on a drawn face is the most fragile shot in the song.

**Look at the sheets before spending anything.** Three tiles in 1280×720 is tight; if a face is
too small to read, crop that tile to head-and-shoulders and rebuild.

## 9 · Order of work

1. Build the sheets. `--dry-run` and read all 21 prompts; it now fails loudly on a missing sheet.
2. **Generate T09a alone** at 832×480 / 4 steps. It is the brand shot and the one fragile
   expression — if the wink comes back clean with the two-frame sheet, nothing else in this
   song is harder. Same seed reproduces it at 720p.
3. Then T03 at 480p — the first shot with both children on the deck, and the night-world test.
   If the indigo collapses to grey at cfg 1.0 that is the Mazhai rain problem again: run 6 steps
   at cfg 1.5–2.0 before touching the shot text, since ATMOSPHERE is already doubled.
4. Then T15 at 480p — the first three-up sheet.
5. Full run at 1280×720 / 6 steps, same seed.

## 10 · Known risks

- **No night or terrace reference exists in the bible.** Both worlds are text-only. So was the
  Mazhai living room, and it rendered well — but it means shot 1 is also the world test.
- **Deep night at cfg 1.0** is the same class of problem as the rain that vanished. Mitigated
  (ATMOSPHERE first and repeated, `daylight, sunlight, daytime` in the negative, and both
  non-humans are practical light sources) — but check it on the first clip.
- **Minmini is the logo.** Drift on him is worse than drift on any other character. T08, T09a
  and T09b all blocking-test before the batch. Your own mascot spec wants his motion procedural
  and composited in Remotion; if the screen-face comes back mangled at 480p, that is the fallback
  and these shots become plates with a mascot-shaped hole.
