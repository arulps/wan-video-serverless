# item-01 report — DONE: CAa + CQa rendered, sheets made, committed — est $1.60 list

Run by CC (A12 watcher), 2026-10-13. Repo `C:\Projects\opencode\video_image`, branch `main`. One render run, no retries.
The clips were not judged.

## Step 0 — prerequisite
`queue\2026-10-13-karadi-1-scale-rule\item-01.done` exists. OK.

## Step 1 — rev 1.3 in place
- `shots.csv` `cast` column uses `Rabbit` and `Squirrel` (11 rows each). `the-rabbit` / `the-squirrel`: 0 occurrences in `shots.csv`,
  0 in `characters.txt`. `characters.txt` has `Rabbit:` and `Squirrel:` lines. OK.
- `duration_s` = 8 for CQa, CQb, CAa, CAb, HKa, HKb (6 of 6); every other row 6 or 7 (I1 7; V1Q–V4A 6; O1–O3 7). OK.
- `shots\09_V1A.raw.txt` contains "the basket never leaves his left paw". OK.
- 18 rows, 18 `shots\NN_ID.raw.txt`, 10 files in `refs\send\`. OK.

## Steps 2–4
- `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
- Credentials check → `credentials present: True` (no values printed).
- `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 7 failure patterns + the R10 stale age, passes 5 fixed ones + the canon lock lines`
- `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 18 shots, 0 fail, 0 warn`

## Step 5 — dry-run
2 rows, no MISSING / ERROR / OVER BUDGET / refused / Traceback.
- **CQa** — `wan3: wan3.0-video 720P 16:9 8s audio=off, est $0.80 (list price); refs=8 labels=['Mintu', 'Minnu', 'the rabbit', 'the squirrel', 'Amma', 'Appa', 'Appa', 'the forest picnic set']`
  refs: `01-mintu-front`, `02-minnu-front`, `04-rabbit`, `05-squirrel`, `06-amma-front`, `07-appa-face`, `08-appa-body`,
  `10-forest-picnic-set` (all `refs/send/*.jpg`).
- **CAa** — `wan3: wan3.0-video 720P 16:9 8s audio=off, est $0.80 (list price); refs=2 labels=['Karadi Mama', 'the forest picnic set']`
  refs: `refs/send/03-karadi-mama.jpg`, `refs/send/10-forest-picnic-set.jpg`.
- Total: `engine=wan3 rows: estimated $1.60 at list price`.
- CQa's 8 ref files: **1,455,181 bytes** (≈ 1.5 MB).

## Step 6 — render
Command as given (`--only CAa,CQa --hosts api --max-usd 1.70 --timeout-min 40`), log `songs\a12-karadi-w3\batch_gate1.log`
(checked: no URL in the log or in the two sidecars).

**Run window:** 2026-10-13 17:22:14 – 17:28:46 UTC = 13:22:14 – 13:28:46 Toronto (EDT).

| Clip | Status | Task id | Wall s | Length | Frames (`ffprobe -count_frames`) | Size | Refs | Est (list) | File |
|---|---|---|---|---|---|---|---|---|---|
| CQa | done | `ed9e6b93-21fd-4f27-b50e-e5ff8736858d` | 227.2 | 8.000 s | 240 (30 fps, 1280×720) | 9,555,857 B | 8 | $0.80 | `out\CQa-seed30313-w3.mp4` |
| CAa | done | `1352e7b4-19a0-4078-8ec8-745a77be33bb` | 163.9 | 8.000 s | 240 (30 fps, 1280×720) | 8,464,577 B | 2 | $0.80 | `out\CAa-seed30313-w3.mp4` |

Runner total: `total GPU-minutes (done shots): 6.5`; running list-price estimate **$1.60** (cap $1.70). The runner rendered CQa first,
then CAa. **Failure lines: none.**

## Step 7 — sheets and stills, in `songs\a12-karadi-w3\out\_qc\`
For each of `CAa` and `CQa`:
- `<ID>-contact.png` — 5×2, frames 0, 24, 48, … 216, 384 px wide each (1920×432).
- `<ID>-every4-first2s.png` — frames 0, 4, … 60, frame number burned in, 256 px wide, 4×4 (1024×576).
- `<ID>-every4-all.png` — frames 0, 4, … 236 (60 frames), frame number burned in, 192 px wide, 10×6 (1920×648).
- `<ID>-f000.png`, `-f030`, `-f060`, `-f120`, `-f180`, `-f239` — 1280×720 stills at 100 %.
- `<ID>-strip.png` — the runner's own strip (6400×720), made automatically.

Made with ffmpeg 9.0.2 (`select` + `drawtext` + `tile`). One sheet was opened only to confirm the frame numbers are burned in.
`out\` is not committed (queue rule), so the clips and sheets are on Beast only.

## Step 8 — commit
`[skip ci]`, paths added explicitly: `songs/a12-karadi-w3/` except `out/` (`refs` with `-f`), `queue/2026-10-13-karadi-gate1`,
`queue/2026-10-13-karadi-gate1b`, `queue/A12-WATCH.md`, `queue/L05-DONE`, `queue/L05-WATCH-LOG.md`. The hash is in this folder's
`LOG.md` done line and `item-01.done` (this report is inside that commit; the markers follow in a small `[skip ci]` commit).

## Spend
A12 so far: **$1.60 list** of the $15.00 song cap (this gate only; the scale-rule queues were $0).
