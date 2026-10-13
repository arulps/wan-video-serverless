# item-01 report — BLOCKED at step 5 (table is not current)

Run by CC (A12 watcher), 2026-10-13 10:22. Repo `C:\Projects\opencode\video_image`, branch `main`. Nothing committed, nothing pushed,
nothing staged. `docs/CHARACTER-SCALE.md` was not overwritten.

## Steps
1. `py tests\test_prompt_lint.py` — last line:
   `PASS: prompt_lint catches 7 failure patterns + the R10 stale age, passes 5 fixed ones + the canon lock lines`
2. `py tests\test_wan3_mock.py` — last line:
   `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
   `py tests\test_song_cuts_reuse.py` — last line:
   `PASS: ffmpeg filter option by version; rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit, both stand-in cuts frame-exact`
3. SIZES line, `--song songs\l05-urulai-w3 --shot I1` (meets all three required phrases):

   > SIZES, the same in every frame: Mintu and Minnu are the same height — the tops of their heads are level; Minmini is a small flying firefly, about the size of a child's hand; Baby Potato is about as tall as a child's hand; Amma Potato is about one and a half times the size of a child's hand. (Mintu 1.00 m, boy, 4-5, round chubby face, chubby hands, six and a half heads tall; Minnu 1.02 m, girl, 5-6, round bright face with deep dimples, six and a half heads tall; Minmini 0.10 m, TV-firefly mascot, flying; Baby Potato 0.11 m, tiny round baby potato, stubby arms and legs; Amma Potato 0.17 m, bigger oval mother potato.)

   Same with `--mode Minmini=perched` (contains the required "resting or hovering still" phrase):

   > SIZES, the same in every frame: Mintu and Minnu are the same height — the tops of their heads are level; Minmini is resting or hovering still close by, up to about half a child's height; Baby Potato is about as tall as a child's hand; Amma Potato is about one and a half times the size of a child's hand. (Mintu 1.00 m, boy, 4-5, round chubby face, chubby hands, six and a half heads tall; Minnu 1.02 m, girl, 5-6, round bright face with deep dimples, six and a half heads tall; Minmini 0.50 m, TV-firefly mascot, perched; Baby Potato 0.11 m, tiny round baby potato, stubby arms and legs; Amma Potato 0.17 m, bigger oval mother potato.)
4. SIZES line, `--song songs\a07-butterfly --shot I2` (has "Mintu, Minnu and Priya are the same height" and "Red Butterfly is
   about the size of a child's head"):

   > SIZES, the same in every frame: Mintu, Minnu and Priya are the same height — the tops of their heads are level; Leo is a little shorter than Mintu; Red Butterfly is about the size of a child's head; Yellow Butterfly is about the size of a child's head; Blue Butterfly is about the size of a child's head; Green Butterfly is about the size of a child's head. (Mintu 1.00 m, boy, 4-5, round chubby face, chubby hands, six and a half heads tall; Minnu 1.02 m, girl, 5-6, round bright face with deep dimples, six and a half heads tall; Leo 0.95 m, boy, 3-4, round chubby face, big rosy cheeks, wild golden curls; Priya 1.02 m, girl, 6-7, round bright face, rosy warm cheeks, long side braid; Red Butterfly 0.25 m, butterfly; Yellow Butterfly 0.25 m, butterfly; Blue Butterfly 0.25 m, butterfly; Green Butterfly 0.25 m, butterfly.)
5. **FAILED.** `py comfy\scale_line.py --table --out %TEMP%\scale-check.md` wrote the file (exit 0), but
   `fc /W docs\CHARACTER-SCALE.md %TEMP%\scale-check.md` reports differences (exit 1). Output:

```
Comparing files DOCS\CHARACTER-SCALE.md and C:\USERS\ARULP\APPDATA\LOCAL\TEMP\SCALE-CHECK.MD
***** DOCS\CHARACTER-SCALE.md
| Character | Height | Build | Source |
|---|---|---|---|
***** C:\USERS\ARULP\APPDATA\LOCAL\TEMP\SCALE-CHECK.MD
| Character | Height | Build | Source |
|---|---|---|---|
*****

***** DOCS\CHARACTER-SCALE.md
| Green Butterfly | 0.25 m | butterfly | same as Vanna (non-human bible v26 size_m) |
**l05-urulai-w3**
| Character | Height | Build | Source |
***** C:\USERS\ARULP\APPDATA\LOCAL\TEMP\SCALE-CHECK.MD
| Green Butterfly | 0.25 m | butterfly | same as Vanna (non-human bible v26 size_m) |
**a12-karadi-w3**
| Character | Height | Build | Source |
*****

***** DOCS\CHARACTER-SCALE.md
|---|---|---|---|
| Baby Potato | 0.11 m | tiny round baby potato, stubby arms and legs | L05 runsheet rev 2.7 (KIDS_SCALE) |
***** C:\USERS\ARULP\APPDATA\LOCAL\TEMP\SCALE-CHECK.MD
|---|---|---|---|
| Karadi Mama | 1.90 m | big round body with a soft cream tummy, stands and walks upright on two legs | A12 concept (Arul 10 Oc
t): a big grown-up bear, taller than Appa standing |
| the rabbit | 0.28 m | bunny | same as Kutti Muyal (animalHeights.ts 'bunny' staging height (bible card 0.80 m)) |
| the squirrel | 0.30 m | squirrel | same as Anil (non-human bible v26 size_m) |
**l05-urulai-w3**
| Character | Height | Build | Source |
|---|---|---|---|
| Baby Potato | 0.11 m | tiny round baby potato, stubby arms and legs | L05 runsheet rev 2.7 (KIDS_SCALE) |
*****
```

   The only content difference is a new **a12-karadi-w3** section in the generated table (Karadi Mama 1.90 m, the rabbit 0.28 m,
   the squirrel 0.30 m). `songs/a12-karadi-w3/` is untracked and newer than this queue (written 10 Oct), so the generator now
   picks up its song-only characters and the committed-to-be doc does not have them. (The first `fc` block shows identical
   header lines; it is a resync artefact, not a content difference.)
6. R10 count (run before the block was written, for information): `0 R10 issues`.
7. Commit: **not done** — blocked at step 5. No commit hash.

## For Fable
Regenerate `docs/CHARACTER-SCALE.md` (or decide whether the a12 section belongs in this commit, and whether
`songs/a12-karadi-w3/scale.json` should be in the path list), then re-issue. CC did not re-run or fix anything.
