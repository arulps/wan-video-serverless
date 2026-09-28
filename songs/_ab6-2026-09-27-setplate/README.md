# A/B round 6 (2026-09-27): can a SET PLATE hold the world constant across Phantom shots? 832x480, seed 30313.

Problem (phase 6a + _ab4): Phantom holds characters but invents a different house in every shot (mint shed + city in
T04_ph720, a domed mint house in T08_ph720, a third house in _ab4) -- a song cannot cut together like that. Phantom only
takes reference images (up to 4), so the test is whether the Twinkle terrace set plate, given as ONE MORE reference image,
becomes the setting in every shot.

Set plate: `set/terrace-set-16x9.png`, built by Fable from `C:\Channel Contents\MinMiniKids\songs\Twinkle Twinkle\v2-mintu-terrace-set.png`
(1344x768, daytime diorama on a flat grey studio background): background keyed to white by an edge flood-fill, fitted to
1280x720 with a 24 px margin like the character sheets. It is DAYTIME; night comes from the prompt (`world-set.txt` = the
song's world.txt + "House, deck and balustrade exactly as in the set reference, at night.").

| row | refs | sampler | question |
|---|---|---|---|
| T04_noset | Minnu | distilled | control: the house Phantom invents with no set ref |
| T04_set | Minnu + set | distilled | does the plate's house/deck/balustrade appear, at night? |
| T08_set | Minmini front + side + set | distilled | SAME house as T04_set? (the consistency test) |
| T07_set | Minnu + Mintu + set | full | two distinct children still hold with a 3rd ref; same house again |

Failure modes to look for: the diorama pasted in as a floating object (grey/white void around it), daylight kept, the
characters shrunk to diorama scale, or identity weakened by the extra reference.
