# item-01 report — keep old RA, checks, render RA + V2b + V5a, sheets, commit (≤ $2.00 list)

## 1. Renames (old RA, made with the old T-pose refs)
- In `songs\a07-butterfly\out\`: `RA-seed30313-w3.mp4/.json` → `RA-seed30313-w3-v2-oldrefs.mp4/.json`.
- In `out\_qc\`: `RA-contact.png`, `RA-f000.png`, `RA-f119.png`, `RA-f239.png`, `RA-strip.png` → the same names with `-v2-oldrefs`
  before `.png`.
- 7 files in total, md5 the same after the rename. No target existed beforehand.
- **Not renamed: `_qc\RA-flap-40-100.png`.** It matches "RA-*.png without -v1-/-v2-", but it is not in the item's list (contact,
  f000/f119/f239, strip). It is Fable's 13:13 analysis image of the **v1 tall-Priya** RA, so a `-v2-oldrefs` label would be wrong,
  and nothing in this run writes that name. It is left as is.
- V2b and V5a had no earlier files.
- After the render and the sheets: the 7 `-v2-oldrefs` files and the 55 other files in `out\` (v1 RA, RB, V1a, both V2a takes, the
  V2a splice + note, all their `_qc` images) are md5 unchanged.

## 2–5. Checks
- **Mock:** `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Gates:**
  - `test_prompt_lint` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`;
  - `prompt_lint --song songs\a07-butterfly` → **`LINT PASS: 33 shots, 0 fail, 0 warn`**;
  - `test_song_cuts_reuse --plan-only` → `PASS (plan only): rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit`.
- **Dry-run** (`--only RA,V2b,V5a`): 3 rows, all `720P 16:9 audio=off`, **`estimated $1.80`**, 0 MISSING/ERROR hits.
  - RA 8 s refs=6 (Mintu, Minnu, Leo, Priya, Amma, Mrs Meena)
  - V2b 5 s refs=3 (Minnu, Priya, the yellow butterfly)
  - V5a 5 s refs=8 (Mintu, Minnu, Leo, Priya and the red, yellow, blue and green butterflies)

## 6. Render
**Window: 19:45:58 → 19:53:43 UTC, 2026-10-02** (15:45:58 → 15:53:43 Toronto EDT). One at a time, `--max-usd 2.00`; the runner exited 0.

| clip | status | task id | wall s | length | frames | refs | est (list) |
|---|---|---|---|---|---|---|---|
| RA | done | `8a01123c-c2bc-4945-9393-ddf14d25e392` | 179.7 | 8 s | 240 | 6 | $0.80 |
| V2b | done | `dae9254c-80ea-48cb-8120-9400706340e6` | 132.2 | 5 s | 150 | 3 | $0.50 |
| V5a | done | `de99df36-3a13-438d-bde3-bac05f1e29a0` | 149.1 | 5 s | 150 | 8 | $0.50 |

- **Total: 18 s, estimated $1.80 at list price** (~$1.26 with the 30% discount); cap $2.00.
- **Failures:** none. All three are 1280×720 @ 30 fps (frames counted by ffprobe), video only. Each sidecar prompt equals its
  `*.raw.txt`. No URL or key appears in the sidecars or in the log. All 3 status cells are `done`.

## 7. Sheets and stills
In `C:\Projects\opencode\video_image\songs\a07-butterfly\out\_qc\`:
- `RA-contact.png`, `V2b-contact.png`, `V5a-contact.png`: 5×2, 10 frames evenly spaced, 384 wide → 1920×432.
- `RA-every10.png`: frames 0, 10 … 230 (24), 256 wide, 6×4 → 1536×576.
- `V2b-every10.png`, `V5a-every10.png`: frames 0 … 140 (15), 5×3 → 1280×432.
- 100% stills (1280×720): `RA-f000.png`, `RA-f119.png`, `RA-f239.png`; `V2b-f000.png`, `V2b-f074.png`, `V2b-f149.png`; `V5a-f000.png`,
  `V5a-f074.png`, `V5a-f149.png`.
- Strips (written by the runner): `RA-strip.png`, `V2b-strip.png`, `V5a-strip.png`.
- Old RA for comparison: `..\RA-seed30313-w3-v2-oldrefs.mp4` (+ `.json`) and `RA-contact-v2-oldrefs.png`, `RA-f000/f119/f239-v2-oldrefs.png`,
  `RA-strip-v2-oldrefs.png`.

Clips: `C:\Projects\opencode\video_image\songs\a07-butterfly\out\RA-seed30313-w3.mp4`, `V2b-seed30313-w3.mp4`, `V5a-seed30313-w3.mp4` (+ `.json`).
Log: `C:\Projects\opencode\video_image\songs\a07-butterfly\batch_gate3.log`.
Nothing was written to `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`. `songs\rowboat\` was not touched.

## 8. Commit
The `[skip ci]` commit containing this file. It holds `songs/a07-butterfly/` except `out/`: the new `refs/01-mintu-front.jpg` and
`refs/02-minnu-front.jpg`, the rev 3.4 `shots/*.raw.txt`, `shots.csv`, `cutplan.json` and `batch_gate3.log`. It also holds the queue
folder. The hash is in CC's chat reply.
