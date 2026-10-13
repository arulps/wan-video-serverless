# item-01 report — BLOCKED at step 5 (`fc` does not print "no differences encountered")

Run by CC (A12 watcher), 2026-10-13 11:11–11:13. Repo `C:\Projects\opencode\video_image`, branch `main`. Nothing committed,
nothing pushed, nothing staged. `docs/CHARACTER-SCALE.md` was not overwritten.

**Short version:** the doc's *text* matches the generated table exactly; the two files differ only in line endings
(doc = LF, generated file = CRLF), and `fc /W` prints one spurious block for that instead of "FC: no differences encountered".
The item's pass condition is the literal `fc` message, so CC stopped rather than judge it.

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
5. **FAILED on the letter of the check.** `py comfy\scale_line.py --table --out %TEMP%\scale-check.md` wrote the file (exit 0).
   `fc /W docs\CHARACTER-SCALE.md %TEMP%\scale-check.md` exit code 1, full output:

```
Comparing files DOCS\CHARACTER-SCALE.md and C:\USERS\ARULP\APPDATA\LOCAL\TEMP\SCALE-CHECK.MD
***** DOCS\CHARACTER-SCALE.md
| Character | Height | Build | Source |
|---|---|---|---|
***** C:\USERS\ARULP\APPDATA\LOCAL\TEMP\SCALE-CHECK.MD
| Character | Height | Build | Source |
|---|---|---|---|
*****
```

   Read-only diagnosis (no file changed):
   - doc: 165 lines, 16718 bytes; generated: 165 lines, 16883 bytes — the 165-byte gap is one CR per line.
   - `cmp` first difference: byte 72, line 1 (the end of line 1).
   - `diff` of the two files with CRs stripped: **no differences** (exit 0).
   - The doc has the three song sections (a07-butterfly, a12-karadi-w3, l05-urulai-w3); the a12 section lists
     Karadi Mama 1.90 m, the rabbit 0.28 m, the squirrel 0.30 m, as the item asks.
   - The same spurious first block was in the 10:22 run's `fc` output (`queue\2026-10-10-scale-rule\item-01.report.md`),
     where CC called it a resync artefact; it is this line-ending difference.
6. R10 count (for information): `0 R10 issues`.
7. Commit: **not done** — blocked at step 5. No commit hash.

## For Fable
Content is current; only the comparison tool disagrees. Options: re-issue with an EOL-insensitive compare
(e.g. `git diff --no-index --ignore-cr-at-eol --exit-code docs/CHARACTER-SCALE.md <generated>`), have `scale_line.py --table`
write LF, or state that this exact `fc` output counts as a pass. CC did not re-run or fix anything.
