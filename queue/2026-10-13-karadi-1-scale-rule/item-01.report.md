# item-01 report — DONE (all checks pass; committed and pushed)

Run by CC (A12 watcher), 2026-10-13 12:21. Repo `C:\Projects\opencode\video_image`, branch `main`. $0, no renders, no API calls.

## Steps
1. `py tests\test_prompt_lint.py` — last line:
   `PASS: prompt_lint catches 7 failure patterns + the R10 stale age, passes 5 fixed ones + the canon lock lines`
2. `py tests\test_wan3_mock.py` — last line:
   `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
   `py tests\test_song_cuts_reuse.py` — last line:
   `PASS: ffmpeg filter option by version; rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit, both stand-in cuts frame-exact`
3. SIZES line, `--song songs\l05-urulai-w3 --shot I1` (starts as required; has both required phrases):

   > SIZES, the same in every frame: Mintu and Minnu are the same height — the tops of their heads are level; Minmini is a small flying firefly, about the size of a child's hand; Baby Potato is about as tall as a child's hand; Amma Potato is about one and a half times the size of a child's hand. (Mintu 1.00 m, boy, 4-5, round chubby face, chubby hands, six and a half heads tall; Minnu 1.02 m, girl, 5-6, round bright face with deep dimples, six and a half heads tall; Minmini 0.10 m, TV-firefly mascot, flying; Baby Potato 0.11 m, tiny round baby potato, stubby arms and legs; Amma Potato 0.17 m, bigger oval mother potato.)

   Same with `--mode Minmini=perched` (has the required "resting or hovering still close by…" phrase):

   > SIZES, the same in every frame: Mintu and Minnu are the same height — the tops of their heads are level; Minmini is resting or hovering still close by, up to about half a child's height; Baby Potato is about as tall as a child's hand; Amma Potato is about one and a half times the size of a child's hand. (Mintu 1.00 m, boy, 4-5, round chubby face, chubby hands, six and a half heads tall; Minnu 1.02 m, girl, 5-6, round bright face with deep dimples, six and a half heads tall; Minmini 0.50 m, TV-firefly mascot, perched; Baby Potato 0.11 m, tiny round baby potato, stubby arms and legs; Amma Potato 0.17 m, bigger oval mother potato.)
4. SIZES line, `--song songs\a07-butterfly --shot I2` (has "Mintu, Minnu and Priya are the same height" and "Red Butterfly is
   about the size of a child's head"):

   > SIZES, the same in every frame: Mintu, Minnu and Priya are the same height — the tops of their heads are level; Leo is a little shorter than Mintu; Red Butterfly is about the size of a child's head; Yellow Butterfly is about the size of a child's head; Blue Butterfly is about the size of a child's head; Green Butterfly is about the size of a child's head. (Mintu 1.00 m, boy, 4-5, round chubby face, chubby hands, six and a half heads tall; Minnu 1.02 m, girl, 5-6, round bright face with deep dimples, six and a half heads tall; Leo 0.95 m, boy, 3-4, round chubby face, big rosy cheeks, wild golden curls; Priya 1.02 m, girl, 6-7, round bright face, rosy warm cheeks, long side braid; Red Butterfly 0.25 m, butterfly; Yellow Butterfly 0.25 m, butterfly; Blue Butterfly 0.25 m, butterfly; Green Butterfly 0.25 m, butterfly.)
5. Table check (Python compare; this replaces the `fc` result the report list asks for): **`TABLE CURRENT`**.
   The doc's `a12-karadi-w3` section lists Karadi Mama 1.90 m, the rabbit 0.28 m, the squirrel 0.30 m. Doc not touched.
6. R10 count: `0 R10 issues`.
7. Commit: message `scale rule: character sizes + builds in every video prompt (R9/R10), Priya = Minnu height [skip ci]`, paths
   added explicitly as listed; nothing else was staged. The hash is in this folder's `LOG.md` done line and in `item-01.done`
   (this report is part of that commit, so it cannot carry its own hash; the markers follow in a small `[skip ci]` commit).

## Left uncommitted on purpose (not in the item's path list)
`queue/2026-10-13-karadi-gate1/`, `queue/A12-WATCH.md`, `queue/A12-WATCH-LOG.md`, `queue/L05-DONE`, `queue/L05-WATCH-LOG.md`,
`songs/a12-karadi-w3/` other than `scale.json` — gate1's own item commits those.
