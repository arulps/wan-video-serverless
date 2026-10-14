# item-01 report — BLOCKED at step 5: both renders FAILED on a network (SSL) error — no clips, not re-run

Run by CC (A12 watcher), 2026-10-13 23:06–23:12 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
One render run, no retries. **No clip came back, so steps 6–8 (sheets, slot cuts, commit) were not done.** Nothing committed.

## Step 0 — prerequisite
`queue\2026-10-13-karadi-rev21-refs\item-01.done` exists. OK.

## Step 1 — rev 2.1+ in place
- `shots\05_HKa.raw.txt` contains "the children do their own quick full turn beside him" and "Image 7 is the lower forest path set". OK.
- `shots\19_O1.raw.txt` contains "Karadi Mama's home set" and "a tall olive-green hiking daypack". OK.
- `shots.csv`: HKa `todo`, O1 `todo`; V1A, V2A, V3A, V4A `done`. OK.
- `refs\send\` has `11-set-path-low.jpg`, `13-set-home.jpg`, `08b-appa-body-backpack.jpg`. OK.
- `out\` had no `HKa-seed30313-w3.mp4` or `O1-seed30313-w3.mp4` at the top level. OK.

**Extra, not in the item (said here as the item asks for moves to be reported):** the rev 1.x `HKa`/`O1` **sidecars and QC sheets**
were still under the plain names and would have been overwritten by this gate. Before rendering, CC moved them (`mv -n`, nothing
deleted): `out\HKa-seed30313-w3.json` and `out\O1-seed30313-w3.json` → `out\_rev1x-2026-10-13\`; the 20 files `out\_qc\HKa-*.png`
and `out\_qc\O1-*.png` → new folder `out\_qc\_rev1x-2026-10-13\`. 22 files in all.

## Steps 2–3
- `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
- Credentials check → `credentials present: True` (no values printed).
- `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 7 failure patterns + the R10 stale age, passes 5 fixed ones + the canon lock lines`
- `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 21 shots, 0 fail, 0 warn`

## Step 4 — dry-run
2 rows, both `wan3.0-video 720P 16:9 audio=off`; no ERROR / unknown cast / MISSING / OVER BUDGET / refused / Traceback.
- **HKa** — 8 s, est $0.80, refs=7: `01-mintu-front`, `02-minnu-front`, `03-karadi-mama`, `06-amma-front`, `07-appa-face`,
  `08b-appa-body-backpack`, `11-set-path-low`; labels `['Mintu', 'Minnu', 'Karadi Mama', 'Amma', 'Appa', 'Appa', 'the lower forest path set']`.
- **O1** — 7 s, est $0.70, refs=9: `01`, `02`, `03`, `04-rabbit`, `05-squirrel`, `06-amma-front`, `07-appa-face`,
  `08b-appa-body-backpack`, `13-set-home`; labels end `"Karadi Mama's home set"`.
- Total: `engine=wan3 rows: estimated $1.50 at list price`.

## Step 5 — render: BOTH FAILED
Command as given (`--only HKa,O1 --hosts api --max-usd 1.60 --timeout-min 40`), log `songs\a12-karadi-w3\batch_gateA.log`
(checked: no URL in it).

**Run window:** 2026-10-14 03:07:19 – 03:11:33 UTC = 13 Oct 23:07:19 – 23:11:33 Toronto (EDT).

| Clip | Status | Task id | Wall s | Length | Frames | Refs | Est |
|---|---|---|---|---|---|---|---|
| HKa | **FAILED** | none — failed before a task was submitted | 76.4 | — | — | 7 | $0.00 |
| O1 | **FAILED** | `6d24e073-4519-4515-801e-31a553879f70` (submitted, was RUNNING) | 177.1 | — | — | 9 | $0.70 at risk |

### The whole log, verbatim
```
[HKa] -> wan3 wan3.0-video 720P 16:9 8s refs=7 first=False last=False est $0.80
[HKa] FAILED (wan3): <urlopen error EOF occurred in violation of protocol (_ssl.c:2427)>
[O1] -> wan3 wan3.0-video 720P 16:9 7s refs=9 first=False last=False est $0.70
  wan3 submitted task 6d24e073-4519-4515-801e-31a553879f70
  wan3 task 6d24e073-4519-4515-801e-31a553879f70: RUNNING
[O1] FAILED (wan3): <urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)>

SHOT       STATUS       WALL_S  FILE
HKa        failed         76.4  <urlopen error EOF occurred in violation of protocol (_ssl.c:2427)>
O1         failed        177.1  <urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)>

total GPU-minutes (done shots): 0.0
```

### What this looks like (CC did not investigate further or retry)
- Both are **connection errors on Beast's side of the link** (the TLS connection was cut), not a refusal by the service and not a
  prompt problem. No `IPInfringementSuspect`.
- **HKa** died while sending the request (76 s in, most likely during the upload of its 7 reference images — about 9 MB with the new
  2.5 MB set plate). No task id was returned, so nothing should be billed.
- **O1** was accepted — the service returned a task id and reported RUNNING — and the connection dropped while the runner was
  polling. **That task may well have finished on the service and may be billed ($0.70) even though no file was downloaded.** If the
  runner or API can fetch a finished task by id, the clip could be recovered without paying for a second render; CC did not try,
  because the queue allows only the one render command.
- The runner printed no running estimate (no clip completed). `shots.csv` now has HKa and O1 as `failed` (the runner's own update).
- The earlier A12 batches today (33 clips) ran over the same route without a network error; the set plates are new in this gate and
  make the uploads several times larger than before — worth checking whether size is the trigger.

## Steps 6–8
Not run: there are no clips to sheet or cut, and `_cuts\_gateA\` was not created. **No commit.** Uncommitted in the repo:
`songs/a12-karadi-w3/batch_gateA.log` (new), `songs/a12-karadi-w3/shots.csv` (HKa, O1 → `failed`), this queue folder,
`queue/A12-WATCH.md` (the 23:00 edit) and `queue/A12-WATCH-LOG.md`.

## Spend
Conservative: **$0.70** (the O1 task that was accepted). A12: $15.40 + $0.70 = **$16.10 list** of the $29.50 cap in `A12-WATCH.md`
($15.40 if the O1 task is not billed).
