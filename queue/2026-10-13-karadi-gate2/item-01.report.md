# item-01 report — 3 of 4 rendered; **V2A FAILED at the API (content check), not re-run** — est $2.50 list

Run by CC (A12 watcher), 2026-10-13. Repo `C:\Projects\opencode\video_image`, branch `main`. One render run, no retries.
The clips were not judged.

## Step 0 — prerequisite
`queue\2026-10-13-karadi-gate1b\item-01.done` and `queue\2026-10-13-karadi-gate1b\FABLE-VERDICT.md` both exist. OK.

## Steps 1–3
- `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
- Credentials check → `credentials present: True` (no values printed).
- `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 7 failure patterns + the R10 stale age, passes 5 fixed ones + the canon lock lines`
- `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 18 shots, 0 fail, 0 warn`

## Step 4 — dry-run
4 rows, all `wan3.0-video 720P 16:9 audio=off`; no ERROR / unknown cast / MISSING / OVER BUDGET / refused / Traceback.
| Row | Length | Refs | Labels | Est |
|---|---|---|---|---|
| V2A | 6 s | 2 | Karadi Mama, the forest picnic set | $0.60 |
| V3Q | 6 s | 6 | Mintu, Minnu, Karadi Mama, the rabbit, the squirrel, the forest picnic set | $0.60 |
| V4A | 6 s | 6 | Mintu, Minnu, Karadi Mama, the rabbit, the squirrel, the forest picnic set | $0.60 |
| O3 | 7 s | 10 | Mintu, Minnu, Karadi Mama, the rabbit, the squirrel, Amma, Appa, Appa, Minmini, the forest picnic set | $0.70 |

Total: `engine=wan3 rows: estimated $2.50 at list price`. O3's 10 ref files (`refs/send/01` … `10`): **1,608,482 bytes**.

## Step 5 — render
Command as given (`--only O3,V3Q,V2A,V4A --hosts api --max-usd 2.60 --timeout-min 50`), log `songs\a12-karadi-w3\batch_gate2.log`
(checked: no URL in the log or in the sidecars).

**Run window:** 2026-10-13 18:02:09 – 18:13:21 UTC = 14:02:09 – 14:13:21 Toronto (EDT). The runner's order was V2A, V3Q, V4A, O3.

| Clip | Status | Task id | Wall s | Length | Frames (`ffprobe -count_frames`) | Size | Refs | Est (list) | File |
|---|---|---|---|---|---|---|---|---|---|
| V2A | **FAILED** | `7a1d6dc7-b3d4-4344-acf3-37bdbc231543` | 130.2 | — | — | — | 2 | $0.60 (see Spend) | none |
| V3Q | done | `89855eaf-d17d-426d-9da8-2e87b6d90350` | 163.4 | 6.000 s | 180 (30 fps, 1280×720) | 7,491,864 B | 6 | $0.60 | `out\V3Q-seed30313-w3.mp4` |
| V4A | done | `ffab0fd8-35af-45a0-84f5-1b7b4e3a93ff` | 164.7 | 6.000 s | 180 (30 fps, 1280×720) | 8,053,046 B | 6 | $0.60 | `out\V4A-seed30313-w3.mp4` |
| O3 | done | `d36f3849-6881-407e-bd09-ff01289fab9e` | 211.8 | 7.000 s | 210 (30 fps, 1280×720) | 8,254,817 B | 10 | $0.70 | `out\O3-seed30313-w3.mp4` |

Runner total: `total GPU-minutes (done shots): 9.0`.

### Failure lines, verbatim
```
  wan3 task 7a1d6dc7-b3d4-4344-acf3-37bdbc231543: FAILED
[V2A] FAILED (wan3): Wan3 task 7a1d6dc7-b3d4-4344-acf3-37bdbc231543 FAILED: IPInfringementSuspect Output data is suspected of being involved in IP infringement
V2A        failed        130.2  Wan3 task 7a1d6dc7-b3d4-4344-acf3-37bdbc231543 FAILED: IPInfringementSuspect Output data is suspected of being involved in IP infringement
```
The task ran for 130 s and was then refused by the service's check on the **output** ("IPInfringementSuspect"). No file was
downloaded. V2A is Karadi Mama alone with the honeycomb and three bees; CAa (same two refs) passed in gate 1b. CC did not re-run it
and did not look into the cause. `shots.csv` status for V2A is now `failed` (the runner's own update).

## Spend
- The runner's running list-price estimate ended at **$2.50** (cap $2.60): it counts V2A's $0.60 even though the task failed.
- Whether the service bills a task that fails its output check is **not known from here** — the three delivered clips are $1.90.
  CC logs the conservative figure: **QUEUE END est $2.50**.
- A12 so far: $1.60 (gate 1b) + $2.50 = **$4.10 list** of the $15.00 song cap (or $3.50 if the failed task is free).

## Step 6 — sheets and stills, in `songs\a12-karadi-w3\out\_qc\`
For each of `O3`, `V3Q`, `V4A` (none for V2A — there is no clip):
- `<ID>-contact.png` — 5×2, 10 frames evenly spaced (every 21st frame for O3, every 18th for V3Q/V4A), 384 px wide each.
- `<ID>-every4-first2s.png` — frames 0, 4, … 60, frame number burned in, 256 px wide, 4×4.
- `<ID>-every4-all.png` — every 4th frame of the whole clip, frame number burned in, 192 px wide, 10 per row
  (O3: 53 frames, 6 rows; V3Q and V4A: 45 frames, 5 rows).
- Stills at 100 % (1280×720): `-f000`, `-f030`, `-f060`, `-f090`, `-f120`, `-f150` and the last frame
  (`O3-f209`, `V3Q-f179`, `V4A-f179`).
- `<ID>-strip.png` — the runner's own strip.

CAa and CQa and their sheets are untouched (20 files still in `_qc`). `out\` is not committed, so clips and sheets are on Beast only.

## Step 7 — commit
`[skip ci]`, explicit paths: `songs/a12-karadi-w3/batch_gate2.log`, `songs/a12-karadi-w3/shots.csv` (status cells),
`queue/2026-10-13-karadi-gate1b/FABLE-VERDICT.md`, `queue/2026-10-13-karadi-gate2`, `queue/A12-WATCH-LOG.md`.
The hash is in this folder's `LOG.md` done line and `item-01.done` (this report is inside that commit; the markers follow in a small
`[skip ci]` commit).

## Marker choice
All steps ran and three of four clips exist, so CC wrote `item-01.done` and `QUEUE END`, with the V2A failure stated in both.
If Fable would rather a partial failure be a `.blocked`, say so in the next queue's protocol.
