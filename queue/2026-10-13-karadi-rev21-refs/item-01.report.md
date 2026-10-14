# item-01 report — DONE: rev 2.1 rebuilt with the set plates and Appa's daypack ref; rev 1.x files moved aside — $0.00

Run by CC (A12 watcher), 2026-10-13, started 23:02 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
No API call, no render. Neither the prompts nor the images were judged.

Song folder below = `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama`.

## Step 1 — the five reference files (in `<song folder>\refs\`)
| File | Bytes | Modified (13 Oct, Toronto) |
|---|---|---|
| `11-set-path-low.jpg` | 2,550,055 | 22:34 |
| `12-set-path-high.jpg` | 2,537,905 | 22:35 |
| `13-set-home.jpg` | 2,640,862 | 22:51 |
| `08b-appa-body-backpack.jpg` | 1,967,162 | 22:51 |
| `06-amma-front.jpg` | 1,889,841 | 17:02 |

All five exist.

## Step 2 — rev 1.x leftovers moved aside (`mv -n`; nothing deleted or overwritten)
**Prompts** → new folder `songs\a12-karadi-w3\shots\_rev1x-2026-10-13\` — all 16 listed names were present and moved:
`02_CQa`, `03_CQb`, `04_CAa`, `05_CAb`, `06_HKa`, `08_V1Q`, `09_V1A`, `10_V2Q`, `11_V2A`, `12_V3Q`, `13_V3A`, `14_V4Q`, `15_V4A`,
`16_O1`, `17_O2`, `18_O3` (`.raw.txt`). `shots\` now holds exactly the 21 rev 2.x files plus that folder.

**Takes** → new folder `songs\a12-karadi-w3\out\_rev1x-2026-10-13\` — all 14 listed IDs were present and moved. There were no
`-v1-picnic` fallbacks for these 14 IDs (only V1A–V4A have them), so none were moved.

Final listing of `out\_rev1x-2026-10-13\` (14 files):
```
CAa-seed30313-w3.mp4
CAb-seed30313-w3.mp4
CQa-seed30313-w3.mp4
CQb-seed30313-w3.mp4
HKa-seed30313-w3.mp4
HKb-seed30313-w3.mp4
I1-seed30313-w3.mp4
O1-seed30313-w3.mp4
O2-seed30313-w3.mp4
O3-seed30313-w3.mp4
V1Q-seed30313-w3.mp4
V2Q-seed30313-w3.mp4
V3Q-seed30313-w3.mp4
V4Q-seed30313-w3.mp4
```

Final listing of `out\` (top level):
```
CAa-seed30313-w3.json
CAb-seed30313-w3.json
CQa-seed30313-w3.json
CQb-seed30313-w3.json
HKa-seed30313-w3.json
HKb-seed30313-w3.json
I1-seed30313-w3.json
O1-seed30313-w3.json
O2-seed30313-w3.json
O3-seed30313-w3.json
V1A-seed30313-w3-v1-picnic.json
V1A-seed30313-w3-v1-picnic.mp4
V1A-seed30313-w3.json
V1A-seed30313-w3.mp4
V1Q-seed30313-w3.json
V2A-seed30313-w3-v1-picnic.json
V2A-seed30313-w3-v1-picnic.mp4
V2A-seed30313-w3.json
V2A-seed30313-w3.mp4
V2Q-seed30313-w3.json
V3A-seed30313-w3-v1-picnic.json
V3A-seed30313-w3-v1-picnic.mp4
V3A-seed30313-w3.json
V3A-seed30313-w3.mp4
V3Q-seed30313-w3.json
V4A-seed30313-w3-v1-picnic.json
V4A-seed30313-w3-v1-picnic.mp4
V4A-seed30313-w3.json
V4A-seed30313-w3.mp4
V4Q-seed30313-w3.json
_qc/
_rev1x-2026-10-13/
```
The four kept takes `V1A|V2A|V3A|V4A-seed30313-w3.mp4` are still in `out\`.

**For Fable — two things the item did not cover, left as they are:**
- The 14 moved takes' **`.json` sidecars are still in `out\`** (the item listed `.mp4` only). A new render of the same ID and seed
  writes `<ID>-seed30313-w3.json` again, which would overwrite the rev 1.x sidecar unless it is moved first.
- The rev 1.x **QC sheets in `out\_qc\`** for those 14 IDs (`<ID>-contact.png`, `-every4-all.png`, stills, `-strip.png`) are also
  still there under the plain names; new sheets for the same IDs would collide with them.

## Step 3 — build
`py "<song folder>\_gen\build_karadi_runsheet.py" "<song folder>" --repo songs\a12-karadi-w3 --selftest` → exit 0, no Traceback,
no AssertionError. Last two lines, verbatim:
```
ok 21 clips 146 s $14.60 list $17.50 w/ reserve slots TA 29 EN 24 set image
SELFTEST OK: place, facing, word-action, pacing, camera rules all refuse a bad clip
```
("set image", as required.) `refs\send\` now has 14 files: the previous ten plus `08b-appa-body-backpack.jpg`,
`11-set-path-low.jpg`, `12-set-path-high.jpg`, `13-set-home.jpg`.

## Step 4 — lint
`py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`

## Step 5 — dry-run
`py comfy\batch_runner.py --song songs\a12-karadi-w3 --hosts http://x --dry-run` → exit 0, 17 rows. Final line, verbatim:
```
engine=wan3 rows: estimated $12.20 at list price (a launch discount may lower it); run with --max-usd >= that
```
`REF MISSING`: 0. `OVER BUDGET`: 0. No `ERROR` or `Traceback`.

`ref=` line of the **HKa** row (7 files):
```
ref=songs/a12-karadi-w3\refs/send/01-mintu-front.jpg|songs/a12-karadi-w3\refs/send/02-minnu-front.jpg|songs/a12-karadi-w3\refs/send/03-karadi-mama.jpg|songs/a12-karadi-w3\refs/send/06-amma-front.jpg|songs/a12-karadi-w3\refs/send/07-appa-face.jpg|songs/a12-karadi-w3\refs/send/08b-appa-body-backpack.jpg|songs/a12-karadi-w3\refs/send/11-set-path-low.jpg
```
`ref=` line of the **O3** row (exactly 10 files, ending in `13-set-home.jpg`):
```
ref=songs/a12-karadi-w3\refs/send/01-mintu-front.jpg|songs/a12-karadi-w3\refs/send/02-minnu-front.jpg|songs/a12-karadi-w3\refs/send/03-karadi-mama.jpg|songs/a12-karadi-w3\refs/send/04-rabbit.jpg|songs/a12-karadi-w3\refs/send/05-squirrel.jpg|songs/a12-karadi-w3\refs/send/06-amma-front.jpg|songs/a12-karadi-w3\refs/send/07-appa-face.jpg|songs/a12-karadi-w3\refs/send/08b-appa-body-backpack.jpg|songs/a12-karadi-w3\refs/send/09-minmini-front.jpg|songs/a12-karadi-w3\refs/send/13-set-home.jpg
```

## Step 6 — status list
```
[('I1', 'todo'), ('CQ0', 'todo'), ('CQa', 'todo'), ('CQb', 'todo'), ('HKa', 'todo'), ('HKc', 'todo'), ('HKb', 'todo'), ('JOIN', 'todo'), ('CAa', 'todo'), ('CAb', 'todo'), ('V1Q', 'todo'), ('V1A', 'done'), ('V2Q', 'todo'), ('V2A', 'done'), ('V3Q', 'todo'), ('V3A', 'done'), ('V4Q', 'todo'), ('V4A', 'done'), ('O1', 'todo'), ('O2', 'todo'), ('O3', 'todo')]
```
V1A–V4A `done`; the 17 others `todo`. As expected.

## Step 7 — cut plan
```
wrote songs/a12-karadi-w3\cutplan.json: TA 29 slots 154.800 s, EN 24 slots 128.000 s, 21 clips — all slots fit their clips, no gaps
```
(The console showed the dash as a replacement character — display only.)

## Step 8 — commit
Message as given. Explicit paths: `songs/a12-karadi-w3/shots.csv`, `shots/` (including `_rev1x-2026-10-13/`), `lint.json`,
`scale.json`, `world.txt`, `characters.txt`, `cutplan.json`, `refs/send/` (`-f`),
`queue/2026-10-13-karadi-restage1/FABLE-VERDICT.md`, `queue/2026-10-13-karadi-rev21-refs`, `queue/A12-WATCH-LOG.md`.
The hash is in this folder's `LOG.md` done line and `item-01.done` (this report is inside that commit; the markers follow in a
small `[skip ci]` commit). `out\` is not committed.

Note: `queue/A12-WATCH.md` was edited at 23:00 (order of the rev 2.x queues; song cap $17 → $29.50). It is not in this item's
commit list, so that edit is still uncommitted.

## Spend
$0.00. A12 total unchanged: $15.40 list (conservative).
