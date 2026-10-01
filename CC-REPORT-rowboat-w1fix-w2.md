# CC-REPORT — Rowboat W1 retakes + W2 (golden grass + Singa), on Wan 3.0 (2026-10-01)

Queue `queue\2026-10-01-rowboat-w1fix-w2`. **Result: 9/9 rendered, 0 failed. 35 s total. Estimate $3.50 at list price** (~$2.45
with the 30% discount; hard cap $4.00). 1280×720 16:9, 30 fps, audio off, seed 30313. No pod, no upscale. Nothing was written to
`C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\`.

## item-01 — checks and render
1. `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
2. Credentials: `credentials present: True`.

2b. **Prompt lint gate:**
- `tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`.
- `comfy\prompt_lint.py --song songs\rowboat --only V1b,V2a,V2b,V2c,V2d,X1b,V3a,V3b,V3c` → last line
  **`LINT PASS: 9 shots, 0 fail, 0 warn`**. No FAIL or WARN lines.

3. **Dry-run:** 9 rows, all `720P 16:9 audio=off`, **`estimated $3.50`**, 0 MISSING/ERROR/OVER BUDGET hits.

4. **Pack check** (`shots.csv` `ref_labels`):
- V1b, V2a, V2b, V2d, V3a and V3c are `Appa|Appa|Mintu|Mintu|Minnu|Minnu`.
- V2c is `Appa|Appa|Mintu|Mintu|Minnu|Minnu|Modhu`.
- All OK.

5. **Render window:** **19:39:06 → 19:51:03 UTC, 2026-10-01** (15:39:06 → 15:51:03 Toronto EDT). 3 tasks in parallel,
   `--max-usd 4.00 --timeout-min 40`, as in the item. The runner exited 0.

- **Protected files:** before the run, the md5 of all 67 protected files was recorded. They are every file of the 5 `done` shots
  (I1, I2, V1a, V1c, X1a) and every `*-v1-*` clip, sidecar and `_qc` PNG.
  - After the run all 67 were **unchanged**.
  - My first post-run check printed "FAILED open or read" for all 67. That was a manifest bug of mine: CRLF line endings and
    backslash paths. It also made the background task exit 1. Re-checked in Python: 67 unchanged, 0 changed, 0 missing.
  - None of the 9 output names existed beforehand.

| shot | status | task id | wall s | length | frames | refs (labels) | est (list) | streams | verbatim prompt |
|---|---|---|---|---|---|---|---|---|---|
| V1b | done | `b1dcb113-5e0b-4226-938a-c871c42a993e` | 116.1 | 3 s | 90 | 6 (Appa ×2, Mintu ×2, Minnu ×2) | $0.30 | video | yes |
| V2a | done | `d8c50ccf-fd69-46b4-9590-d014ecfabd4c` | 102.0 | 3 s | 90 | 6 (family) | $0.30 | video | yes |
| V2b | done | `16dda29b-4d4e-429d-99bc-759b6ec19be3` | 116.5 | 3 s | 90 | 6 (family) | $0.30 | video | yes |
| V2c | done | `96e4af20-6bb8-44d1-a2cc-945a5d9f7a73` | 117.1 | 3 s | 90 | 7 (family + Modhu) | $0.30 | video | yes |
| V2d | done | `bc04df5f-14e0-4c6e-a146-733a2c3a4712` | 116.0 | 4 s | 120 | 6 (family) | $0.40 | video | yes |
| X1b | done | `9e94ff81-08db-4202-955b-2d09c5cec64e` | 595.8 | 6 s | 180 | 6 (family) | $0.60 | video | yes |
| V3a | done | `4bd907e9-a256-46ee-9f25-4ccd689f827a` | 155.6 | 6 s | 180 | 6 (family) | $0.60 | video | yes |
| V3b | done | `0c24c5fd-e0b8-4db8-aa75-df03b3bd8f4a` | 109.4 | 3 s | 90 | 1 (Singa) | $0.30 | video | yes |
| V3c | done | `908a19ff-e568-4f36-947a-a50733f08232` | 210.8 | 4 s | 120 | 6 (family) | $0.40 | video | yes |

"Family" = `Appa|Appa|Mintu|Mintu|Minnu|Minnu` (face + body each). Task ids come from each clip's sidecar.

- **Failures:** none. No URL or key appears in any sidecar or in the log. All 9 `shots.csv` status cells are `done`.
- X1b's 596 s wall time was API queue time, not an error.
- **Prompt content, numbers only:**
  - The "Only Appa, the grown-up father … rows and holds the oars" line is in 8 of 9 prompts. The exceptions are V3b (Singa only)
    and V2c (Modhu's water-level shot; its only "rows" is "rows of small rounded bumps", which the lint rule excludes).
  - "One continuous take, no cuts between the timed moments" is present in the beat shots (e.g. X1b, V3a).

## item-02 — sheets and stills
- **Contact sheets:** 5×2, 10 frames evenly spaced from the first frame to the last, 384 wide → 1920×432.
- **100% stills** at 10/50/95 % of the frame count (1280×720):

| shot(s) | frames | stills |
|---|---|---|
| X1b, V3a | 180 | f018, f090, f171 |
| V2d, V3c | 120 | f012, f060, f114 |
| V1b, V2a, V2b, V2c, V3b | 90 | f009, f045, f086 |

- Nothing was copied to the song folder.

## Paths
Clips and sidecars:
- `C:\Projects\opencode\video_image\songs\rowboat\out\V1b-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V2a-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V2b-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V2c-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V2d-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\X1b-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V3a-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V3b-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V3c-seed30313-w3.mp4` (+ `.json`)

QC in `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\`: per shot `<ID>-strip.png`, `<ID>-contact.png` and the three stills
above, e.g. `...\_qc\V3a-contact.png`, `...\_qc\V3a-f018.png`, `...\_qc\V3a-f090.png`, `...\_qc\V3a-f171.png`.

Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_w1fix_w2.log`

## Commit
The `[skip ci]` commit containing this report. It holds:
- `comfy/prompt_lint.py`, `tests/test_prompt_lint.py`, `songs/rowboat/lint.json`;
- `songs/rowboat/_make_rowboat.py` (PACK_SWAP / PACK_SHOT / SHOT_FIX), the regenerated `shots/`, `shots.csv` (9 new `done` cells)
  and `cutplan.json` (unchanged, so a no-op);
- the queue folder and this report.

`out/` is not included. The hash is in CC's chat reply. Not committed: Fable's uncommitted edit to
`REVIEW-learning-batch1-2026-09-29.md`.

## Not judged
Fable reviews.
