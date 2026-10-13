# item-01 report — BLOCKED at step 5 (dry-run: CQa fails to assemble) — $0.00 spent

Run by CC (A12 watcher), 2026-10-13 12:26–12:27 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
**No render was started. No API call was made. Nothing committed.** No generated file or runner was edited.

## Step 0 — prerequisite
`queue\2026-10-13-karadi-1-scale-rule\item-01.done` exists. OK.

## Step 1 — rev 1.2 in place
- `shots.csv`: 18 rows. `duration_s` = 8 for CQa, CQb, CAa, CAb, HKa, HKb (6 of 6); every other row is 6 or 7
  (I1 7; V1Q–V4A 6; O1–O3 7). OK.
- `shots\09_V1A.raw.txt` contains "the basket never leaves his left paw". OK.
- 18 `shots\NN_ID.raw.txt` files; 10 files in `refs\send\`. OK.

## Steps 2–4
- `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`
- Credentials check → `credentials present: True` (no values printed).
- `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 7 failure patterns + the R10 stale age, passes 5 fixed ones + the canon lock lines`
- `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 18 shots, 0 fail, 0 warn`

## Step 5 — dry-run: FAILED
`py comfy\batch_runner.py --song songs\a12-karadi-w3 --only CAa,CQa --hosts api --dry-run`

**CQa — ERROR, verbatim:**
```
shot_id: CQa  cast: Mintu+Minnu+the-rabbit+the-squirrel+Amma+Appa
  ERROR assembling prompt: unknown cast name 'the-rabbit' (known: Amma, Appa, Karadi-Mama, Minmini, Minnu, Mintu). Add it to the song's characters.txt or to PROMPT-PLAYBOOK.md section 8.
```

**CAa — as expected:**
```
shot_id: CAa  cast: Karadi-Mama
engine=wan3 mode=standard steps=6 cfg=1 seed=30313 size=1280x720 frames=129 ref=…refs/send/03-karadi-mama.jpg|…refs/send/10-forest-picnic-set.jpg
  wan3: wan3.0-video 720P 16:9 8s audio=off, est $0.80 (list price); refs=2 labels=['Karadi Mama', 'the forest picnic set'] first=- last=-
```

**Total line:** `engine=wan3 rows: estimated $0.80 at list price` — the item expects 2 rows and "estimated $1.60". Only 1 row assembled.

**CQa's 8 ref files:** 1,455,181 bytes in total (≈ 1.5 MB, as expected):
01-mintu-front 190,928 · 02-minnu-front 153,131 · 04-rabbit 102,869 · 05-squirrel 226,745 · 06-amma-front 119,809 ·
07-appa-face 235,956 · 08-appa-body 125,734 · 10-forest-picnic-set 300,009.

## Read-only diagnosis (nothing changed)
- `songs\a12-karadi-w3\characters.txt` (written 13 Oct 00:39) **does** have the lines `the-rabbit: small grey bunny; …` and
  `the-squirrel: small chestnut squirrel; …`, but the runner's "known" list is only
  `Amma, Appa, Karadi-Mama, Minmini, Minnu, Mintu` — the two lower-case names are not picked up. The likely cause is that the
  runner's lock-line parser only accepts names that start with a capital letter; CC did not open the runner to confirm.
- `prompt_lint.py` passes the same folder (18/0/0), so lint and the runner read cast names differently.
- The same cast names are in 11 of the 18 rows (I1, CQa, CQb, HKb, V3Q, V3A, V4Q, V4A, O1, O2, O3), so this would block the batch too,
  not just this gate.

## Steps 6–8
Not run. No clips, no sheets, no commit hash.

## For Fable
Fix the cast names (or the parser) and re-issue. CC did not retry, edit `characters.txt`/`shots.csv`, or touch the runner.
