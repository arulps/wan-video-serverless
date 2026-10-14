# item-01 report — DONE: rev 2.0 built on Beast, lint + dry-run + cut plan match Fable's mirror — $0.00

Run by CC (A12 watcher), 2026-10-13 22:41–22:47 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
No API call, no render. The prompts were not judged.

Song folder below = `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama`.

## Step 0 — tidy
```
renamed 'queue/2026-10-13-karadi-pacing' -> 'queue/2026-10-13-karadi-pacing-SUPERSEDED'
```
Rename only; its `QUEUE.md` and `item-01.md` are unchanged inside. It never had a READY file and was never run.

## `git status --short` before the build (and so before the add)
Leaving out other songs' untracked logs/reviews and the L05 `urulai` folders, which this queue does not touch:
```
 M queue/A12-WATCH-LOG.md
 M songs/a12-karadi-w3/refs/send/06-amma-front.jpg
?? queue/2026-10-13-karadi-pacing-SUPERSEDED/
?? queue/2026-10-13-karadi-restage1/FABLE-VERDICT.md
?? queue/2026-10-13-karadi-rev20-build/
```
Note: `refs/send/06-amma-front.jpg` was **already modified before the build** (file time 13 Oct 17:02) — not by CC.

## Step 1 — build
`py "<song folder>\_gen\build_karadi_runsheet.py" "<song folder>" --repo songs\a12-karadi-w3 --selftest` → exit 0, no Traceback,
no AssertionError. Last two lines, verbatim:
```
ok 21 clips 146 s $14.60 list $17.50 w/ reserve slots TA 29 EN 24 no set image
SELFTEST OK: place, facing, word-action, pacing, camera rules all refuse a bad clip
```
("no set image" variant, as the item allows.)

## Step 2 — lint
`py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`

## Step 3 — dry-run
`py comfy\batch_runner.py --song songs\a12-karadi-w3 --hosts http://x --dry-run` → exit 0, 17 rows assembled. Final line, verbatim:
```
engine=wan3 rows: estimated $12.20 at list price (a launch discount may lower it); run with --max-usd >= that
```
`REF MISSING`: 0. `OVER BUDGET`: 0. No `ERROR` or `Traceback`.

## Step 4 — status list
```
[('I1', 'todo'), ('CQ0', 'todo'), ('CQa', 'todo'), ('CQb', 'todo'), ('HKa', 'todo'), ('HKc', 'todo'), ('HKb', 'todo'), ('JOIN', 'todo'), ('CAa', 'todo'), ('CAb', 'todo'), ('V1Q', 'todo'), ('V1A', 'done'), ('V2Q', 'todo'), ('V2A', 'done'), ('V3Q', 'todo'), ('V3A', 'done'), ('V4Q', 'todo'), ('V4A', 'done'), ('O1', 'todo'), ('O2', 'todo'), ('O3', 'todo')]
```
V1A, V2A, V3A, V4A = `done`; the 17 others = `todo`. As expected.

## Step 5 — cut plan
`py "<song folder>\_gen\make_cutplan.py" songs\a12-karadi-w3` →
```
wrote songs/a12-karadi-w3\cutplan.json: TA 29 slots 154.800 s, EN 24 slots 128.000 s, 21 clips — all slots fit their clips, no gaps
```
(The console showed the dash as a replacement character — display only.)

## Things Fable should know (nothing was changed because of them)
1. **16 old-numbered prompt files are still in `shots\`.** The builder wrote the 21 rev 2.0 files with new numbers and did not remove
   the rev 1.x ones, so the folder holds 37 files. Left over (rev 1.x numbering): `02_CQa`, `03_CQb`, `04_CAa`, `05_CAb`, `06_HKa`,
   `08_V1Q`, `09_V1A`, `10_V2Q`, `11_V2A`, `12_V3Q`, `13_V3A`, `14_V4Q`, `15_V4A`, `16_O1`, `17_O2`, `18_O3` (`.raw.txt`).
   Lint and the runner read `shots.csv`, so both ignore them (21 / 17 rows). CC did not move or delete them; they are unchanged in
   git. Several IDs now exist under two numbers (e.g. `02_CQa` old and `03_CQa` new).
2. **The four kept verse answers are identical**, as Fable said: new `12_V1A`, `14_V2A`, `16_V3A`, `18_V4A` match the committed
   rev 1.5 `09_V1A`, `11_V2A`, `13_V3A`, `15_V4A` (compared ignoring line endings).
3. **Nine reference images changed** in `refs\send\` (`01`–`09`; `10-forest-picnic-set.jpg` did not). `06-amma-front.jpg` had
   already changed before this run (see above).
4. **`out\` untouched:** 45 files in `out\` and 223 in `out\_qc\` before and after. The `out\` clip names still follow rev 1.x IDs.
5. **Budget, for the next queue:** A12 stands at $15.40 list (conservative) of the $17.00 cap in `A12-WATCH.md`. The 17 todo rows
   are $12.20, so any render queue with a cap above $1.60 will be stopped by the watcher's step-4 budget check unless the cap in
   `A12-WATCH.md` changes first. (The builder's own line says "$17.50 w/ reserve".)
6. `queue\2026-10-13-karadi-restage1\FABLE-VERDICT.md` is untracked and not in this item's commit list, so it is still uncommitted.

## Step 6 — commit
Message as given. Explicit paths: `songs/a12-karadi-w3/shots.csv`, `shots/`, `lint.json`, `scale.json`, `world.txt`,
`characters.txt`, `cutplan.json`, `refs/send/` (`-f`), `queue/2026-10-13-karadi-rev20-build`,
`queue/2026-10-13-karadi-pacing-SUPERSEDED`, `queue/A12-WATCH-LOG.md`. The hash is in this folder's `LOG.md` done line and
`item-01.done` (this report is inside that commit; the markers follow in a small `[skip ci]` commit).

In the song folder the builder wrote only what the queue lists (`KARADI-MAMA-WAN3-RUNSHEET.md`, `karadi-shots.json`,
`_gen\scale.json`, `_gen\lint.json`); CC wrote nothing there.
