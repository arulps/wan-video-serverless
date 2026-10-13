# item-01 report — DONE: old takes kept, V1A + V2A + V3A + V4A re-rendered, no failures — est $2.40 list

Run by CC (A12 watcher), 2026-10-13. Repo `C:\Projects\opencode\video_image`, branch `main`. One render run, no retries.
The clips were not judged.

## Step 1 — old takes kept (renamed with `mv -n`; nothing copied over or deleted)
In `songs\a12-karadi-w3\out\` (8 files):
- `V1A-seed30313-w3.mp4` / `.json` → `V1A-seed30313-w3-v1-picnic.mp4` / `.json`
- `V2A-seed30313-w3.mp4` / `.json` → `V2A-seed30313-w3-v1-picnic.mp4` / `.json`
- `V3A-seed30313-w3.mp4` / `.json` → `V3A-seed30313-w3-v1-picnic.mp4` / `.json`
- `V4A-seed30313-w3.mp4` / `.json` → `V4A-seed30313-w3-v1-picnic.mp4` / `.json`

In `out\_qc\` (41 files), each `<name>.png` → `<name>-v1-picnic.png`:
- V1A, V2A, V3A — 10 each: `-contact`, `-every4-all`, `-f000`, `-f030`, `-f060`, `-f090`, `-f120`, `-f150`, `-f179`, `-strip`.
- V4A — 11: the same ten plus `-every4-first2s` (from gate 2).

49 renames in all. Afterwards no un-suffixed `V1A-*` … `V4A-*` file was left in `out\` or `out\_qc\`.

## Step 2 — rev 1.5 in place
- `shots.csv`: V1A, V2A, V3A, V4A are `todo`; the other 14 rows are `done`. OK.
- `shots\09_V1A.raw.txt` contains "tall wildflowers". OK.
- `shots\11_V2A.raw.txt` contains "bees' nest". OK.
- `shots\13_V3A.raw.txt` contains "ankle-deep water". OK.
- `shots\15_V4A.raw.txt` contains "among the blueberry bushes". OK.

## Steps 3–4
- `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
- Credentials check → `credentials present: True` (no values printed).
- `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 7 failure patterns + the R10 stale age, passes 5 fixed ones + the canon lock lines`
- `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 18 shots, 0 fail, 0 warn`

## Step 5 — dry-run
4 rows, all `wan3.0-video 720P 16:9 6s audio=off`; no ERROR / unknown cast / MISSING / OVER BUDGET / refused / Traceback.
| Row | Cast | Refs | Ref files (`refs/send/`) | Est |
|---|---|---|---|---|
| V1A | Minnu+Karadi-Mama | 2 | `02-minnu-front`, `03-karadi-mama` | $0.60 |
| V2A | Mintu+Karadi-Mama | 2 | `01-mintu-front`, `03-karadi-mama` | $0.60 |
| V3A | Mintu+Minnu+Karadi-Mama+Rabbit+Squirrel | 5 | `01`, `02`, `03`, `04-rabbit`, `05-squirrel` | $0.60 |
| V4A | Mintu+Minnu+Karadi-Mama+Rabbit+Squirrel | 5 | `01`, `02`, `03`, `04-rabbit`, `05-squirrel` | $0.60 |

`10-forest-picnic-set` is in none of the four. Total: `engine=wan3 rows: estimated $2.40 at list price`.

## Step 6 — render
Command as given (`--only V1A,V2A,V3A,V4A --hosts api --max-usd 2.50 --timeout-min 50`), log
`songs\a12-karadi-w3\batch_restage1.log` (checked: no URL in the log or in the sidecars).

**Run window:** 2026-10-13 19:52:32 – 20:02:06 UTC = 15:52:32 – 16:02:06 Toronto (EDT).

| Clip | Status | Task id | Wall s | Frames (`ffprobe -count_frames`) | Length | Size (B) | Est (list) |
|---|---|---|---|---|---|---|---|
| V1A | done | `044141e9-dbb3-42a8-8406-8d225274fb11` | 131.3 | 180 | 6.000 s | 8,019,321 | $0.60 |
| V2A | done | `f8402c4c-f4d7-4909-97c2-d3b4990cf405` | 131.1 | 180 | 6.000 s | 8,327,415 | $0.60 |
| V3A | done | `8f738dd8-c113-466e-b26d-54d58c55b839` | 146.9 | 180 | 6.000 s | 10,187,556 | $0.60 |
| V4A | done | `a7e6e7c5-07de-434a-84a0-ab787b0ce44f` | 162.7 | 180 | 6.000 s | 9,370,700 | $0.60 |

All 1280×720 at 30 fps, files `out\<ID>-seed30313-w3.mp4`. **Failure lines: none** (no `IPInfringementSuspect`).
Runner total: `total GPU-minutes (done shots): 9.5`. **Runner's final estimate: $2.40 list** (cap $2.50).

## Step 7 — sheets and stills, in `out\_qc\`
For each of V1A, V2A, V3A, V4A (written with ffmpeg `-n`, so nothing could be overwritten):
- `<ID>-contact.png` — 5×2, every 18th frame, 384 px wide each;
- `<ID>-every4-all.png` — every 4th frame (45 frames, 5 rows of 10), frame number burned in, 192 px wide;
- stills at 100 %: `-f000`, `-f030`, `-f060`, `-f090`, `-f120`, `-f150`, `-f179`;
- `<ID>-strip.png` — the runner's own strip.

## Spend
A12: $13.00 (conservative) + $2.40 = **$15.40 list** of the $17.00 cap (or $14.80 if gate 2's refused task was not billed).
The $17 cap is the figure in `queue\A12-WATCH.md` as edited on 13 Oct 15:47 ("raised from $15 by Arul"); CC took it from that file
and has asked Arul in chat to confirm it.
