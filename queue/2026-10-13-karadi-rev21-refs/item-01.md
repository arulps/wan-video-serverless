# item-01 — rebuild with the refs, move rev 1.x files aside, lint, dry-run, cut plan, commit ($0.00)

1. Check the five files exist (report sizes): in `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\refs\`:
   `11-set-path-low.jpg`, `12-set-path-high.jpg`, `13-set-home.jpg`, `08b-appa-body-backpack.jpg`, `06-amma-front.jpg`. Any missing → **blocked**.
2. Move the rev 1.x leftovers aside (`move`, never `del`), from the repo root:
   ```
   mkdir songs\a12-karadi-w3\shots\_rev1x-2026-10-13
   move songs\a12-karadi-w3\shots\02_CQa.raw.txt songs\a12-karadi-w3\shots\_rev1x-2026-10-13\
   ```
   …and the same for `03_CQb 04_CAa 05_CAb 06_HKa 08_V1Q 09_V1A 10_V2Q 11_V2A 12_V3Q 13_V3A 14_V4Q 15_V4A 16_O1 17_O2 18_O3`
   (16 files; these are the OLD numbers — the rev 2.x files have different numbers for the same IDs; if a listed name is missing,
   say so and carry on). Then the old takes whose IDs will be re-rendered:
   ```
   mkdir songs\a12-karadi-w3\out\_rev1x-2026-10-13
   for %i in (I1 CQa CQb CAa CAb HKa HKb V1Q V2Q V3Q V4Q O1 O2 O3) do move songs\a12-karadi-w3\out\%i-seed30313-w3.mp4 songs\a12-karadi-w3\out\_rev1x-2026-10-13\
   ```
   plus any `%i-*-v1-picnic*.mp4` fallbacks for those IDs, the same way. **Do not move** `V1A|V2A|V3A|V4A-seed30313-w3.mp4`.
   Report the final listing of `out\` (top level) and of `out\_rev1x-2026-10-13\`.
3. Build:
   ```
   py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\build_karadi_runsheet.py" "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama" --repo songs\a12-karadi-w3 --selftest
   ```
   Expect the last two lines `ok 21 clips 146 s $14.60 list $17.50 w/ reserve slots TA 29 EN 24 set image` (note: **set image**, not
   "no set image") and `SELFTEST OK: ...`. Anything else → **blocked**, verbatim.
4. `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`.
5. `py comfy\batch_runner.py --song songs\a12-karadi-w3 --hosts http://x --dry-run` → final line `... estimated $12.20 ...`, no
   `REF MISSING`. Also report the `ref=` line of the HKa row and of the O3 row (O3 must list exactly 10 files ending in `13-set-home.jpg`).
6. Status check as in the previous queue: V1A–V4A `done`, the 17 others `todo`.
7. `py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\make_cutplan.py" songs\a12-karadi-w3` → `... 21 clips — all slots fit their clips, no gaps`.
8. Commit with `[skip ci]` and push: `songs/a12-karadi-w3/` (shots.csv, shots/ incl. the moved folder, lint.json, scale.json, world.txt,
   characters.txt, cutplan.json, refs/send/ with `-f`), `queue/2026-10-13-karadi-restage1/FABLE-VERDICT.md`,
   `queue/2026-10-13-karadi-rev21-refs`, `queue/A12-WATCH-LOG.md`.
   Message: `a12 rev 2.1: set plates (lower path, upper path, home) + Appa's daypack ref in every trek clip; rev 1.x prompts and takes moved aside; lint 21/0/0, dry-run $12.20 [skip ci]`

   **Do not judge the prompts or the images.**

**item-01.report.md** must cover: the five file sizes, the two `out\` listings, each step's output verbatim, the two `ref=` lines, the commit hash.
