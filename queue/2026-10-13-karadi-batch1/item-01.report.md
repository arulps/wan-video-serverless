# item-01 report — DONE: all 13 clips rendered, no failures — est $8.90 list

Run by CC (A12 watcher), 2026-10-13. Repo `C:\Projects\opencode\video_image`, branch `main`. One render run, no retries.
The clips were not judged.

## Step 0 — prerequisite
`queue\2026-10-13-karadi-gate2\item-01.done` and `queue\2026-10-13-karadi-gate2\FABLE-VERDICT.md` both exist. OK.

## Step 1 — rev 1.4 in place
- `shots\11_V2A.raw.txt` starts with "Image 1 is Mintu, Image 2 is Karadi Mama". OK.
- V2A's `shots.csv` row: cast `Mintu+Karadi-Mama`, status `todo`, 3 refs (6 s). OK.
- CAa, CQa, V3Q, V4A, O3: status `done`. OK. (The other 12 rows were `todo`.)

## Steps 2–4
- `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
- Credentials check → `credentials present: True` (no values printed).
- `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 7 failure patterns + the R10 stale age, passes 5 fixed ones + the canon lock lines`
- `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 18 shots, 0 fail, 0 warn`

## Step 5 — dry-run
13 rows, all `wan3.0-video 720P 16:9 audio=off`; no ERROR / unknown cast / MISSING / OVER BUDGET / refused / Traceback.
| Row | Length | Refs | Est | | Row | Length | Refs | Est |
|---|---|---|---|---|---|---|---|---|
| I1 | 7 s | 8 | $0.70 | | V2Q | 6 s | 3 | $0.60 |
| CQb | 8 s | 8 | $0.80 | | V2A | 6 s | 3 | $0.60 |
| CAb | 8 s | 2 | $0.80 | | V3A | 6 s | 6 | $0.60 |
| HKa | 8 s | 2 | $0.80 | | V4Q | 6 s | 4 | $0.60 |
| HKb | 8 s | 8 | $0.80 | | O1 | 7 s | 9 | $0.70 |
| V1Q | 6 s | 3 | $0.60 | | O2 | 7 s | 9 | $0.70 |
| V1A | 6 s | 2 | $0.60 | | | | | |

Durations as required: I1, O1, O2 7 s; HKa, HKb, CQb, CAb 8 s; the six verse rows 6 s.
Total: `engine=wan3 rows: estimated $8.90 at list price`.

## Step 6 — render
Command as given (13 IDs, `--hosts api --max-usd 9.00 --timeout-min 50`), log `songs\a12-karadi-w3\batch_batch1.log`
(checked: no URL in the log or in the sidecars).

**Run window:** 2026-10-13 18:42:12 – 19:19:53 UTC = 14:42:12 – 15:19:53 Toronto (EDT). Rows are in the runner's order.

| Clip | Status | Task id | Wall s | Length | Frames (`ffprobe -count_frames`) | Size (B) | Est (list) |
|---|---|---|---|---|---|---|---|
| I1 | done | `9f8984da-7b08-4a0d-95f2-c9fd553a9fb5` | 195.6 | 7.000 s | 210 | 9,126,994 | $0.70 |
| CQb | done | `aadaf461-ace0-4c0c-9bf4-f365a3e70d77` | 210.6 | 8.000 s | 240 | 10,066,402 | $0.80 |
| CAb | done | `1f1906af-ca36-47aa-82b0-2439b8d4c275` | 163.0 | 8.000 s | 240 | 8,549,520 | $0.80 |
| HKa | done | `48d73ce5-f25e-424c-be25-2b175f0f37cc` | 179.1 | 8.000 s | 240 | 11,528,753 | $0.80 |
| HKb | done | `eba663a3-c04b-486c-aa69-d3904dba812e` | 210.3 | 8.000 s | 240 | 9,712,256 | $0.80 |
| V1Q | done | `ff9ad13a-1e33-471a-bd5e-53c1286a03ba` | 147.1 | 6.000 s | 180 | 7,127,647 | $0.60 |
| V1A | done | `cb6b3c6d-74df-4e97-8b87-ebbbea0045cc` | 135.5 | 6.000 s | 180 | 5,377,988 | $0.60 |
| V2Q | done | `e34985d1-fc00-470e-86b7-daaf86f6d4f0` | 131.1 | 6.000 s | 180 | 5,681,506 | $0.60 |
| V2A | done | `7f5562d5-ab38-45a7-acbb-f2414df13ba9` | 148.7 | 6.000 s | 180 | 6,599,906 | $0.60 |
| V3A | done | `c8e3156c-13c3-45fc-a27a-6938fc5c69b7` | 179.3 | 6.000 s | 180 | 8,440,281 | $0.60 |
| V4Q | done | `5ea074cf-d58e-4cbe-8177-bbadfa8dedf2` | 162.9 | 6.000 s | 180 | 6,800,755 | $0.60 |
| O1 | done | `81569ad5-60de-4596-ab57-a51b091b0215` | 195.3 | 7.000 s | 210 | 9,535,535 | $0.70 |
| O2 | done | `26d3888c-d87e-4a7a-a210-3b53ef3784ca` | 195.4 | 7.000 s | 210 | 9,869,027 | $0.70 |

All clips are 1280×720 at 30 fps, files `out\<ID>-seed30313-w3.mp4`. **Failure lines: none** — the re-staged V2A (rev 1.4) came
back this time. Runner total: `total GPU-minutes (done shots): 37.6`.

**Runner's final estimate: $8.90 list** (cap $9.00). All 18 `shots.csv` rows now have status `done`.

## Spend
A12 so far: $1.60 (gate 1b) + $2.50 (gate 2, conservative — includes the refused V2A task) + $8.90 = **$13.00 list** of the
$15.00 song cap (or $12.40 if the refused gate-2 task was not billed). **About $2.00 is left for retakes.**

## Step 7 — sheets and stills, in `songs\a12-karadi-w3\out\_qc\`
For each of the 13 clips (same ffmpeg method as gate 2):
- `<ID>-contact.png` — 5×2, 10 frames evenly spaced, 384 px wide each;
- `<ID>-every4-all.png` — every 4th frame of the whole clip, frame number burned in, 192 px wide, 10 per row
  (8 s: 60 frames, 6 rows; 7 s: 53 frames, 6 rows; 6 s: 45 frames, 5 rows);
- stills at 100 % (1280×720): `-f000`, `-f030`, `-f060`, `-f090`, `-f120`, `-f150` and the last frame
  (`-f239` for 8 s, `-f209` for 7 s, `-f179` for 6 s);
- `<ID>-strip.png` — the runner's own strip.

The five kept clips (CAa, CQa, O3, V3Q, V4A) and their 53 sheet files are untouched. `out\` is not committed, so the 18 clips and
all sheets are on Beast only.

## Step 8 — commit
`[skip ci]`, explicit paths: `songs/a12-karadi-w3/batch_batch1.log`, `songs/a12-karadi-w3/shots.csv`,
`songs/a12-karadi-w3/shots/11_V2A.raw.txt` (Fable's rev 1.4 re-stage), `queue/2026-10-13-karadi-gate2/FABLE-VERDICT.md`,
`queue/2026-10-13-karadi-batch1`, `queue/A12-WATCH-LOG.md`. The hash is in this folder's `LOG.md` done line and `item-01.done`
(this report is inside that commit; the markers follow in a small `[skip ci]` commit).
