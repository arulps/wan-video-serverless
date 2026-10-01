# CC-REPORT — Rowboat W2 retakes + W3–W6 (all remaining shots): L04 Row Row Row Your Boat on Wan 3.0 (2026-10-01)

Queue `queue\2026-10-01-rowboat-w2fix-w3w4`. **Result: 17/17 rendered, 0 failed. 74 s total. Estimate $7.40 at list price**
(~$5.18 with the 30% discount; hard cap $8.00). 1280×720 16:9, 30 fps, audio off, seed 30313. No pod, no upscale.
Nothing was written to `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\`.
**After this run all 29 shots in `songs\rowboat\shots.csv` are `done`.**

## item-01 — checks and render
1. `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
2. Credentials: `credentials present: True`.
3. **Prompt lint gate:**
   - `tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`.
   - `prompt_lint.py --only <17 shots>` → last line **`LINT PASS: 17 shots, 0 fail, 1 warn`**. No FAIL lines.
   - The one WARN: `R8 no reference images -- check the style holds (object-only shots drift photoreal)`. This is T1, the only shot with refs=0.
4. **Dry-run:** 17 rows, all `720P 16:9 audio=off`, **`estimated $7.40`**, 0 MISSING/ERROR/OVER BUDGET hits.
5. **Pack check:** V3a = `Appa|Appa|Mintu|Mintu|Minnu|Minnu|Singa`, V4c = `Appa|Appa|Mintu|Mintu|Minnu|Minnu`,
   X3a = `Modhu|Singa|Pani Karadi`. All OK.
- **Protected files:** **161** files were fingerprinted (md5, in Python) before the run:
  - every file of the 12 `done` shots I1, I2, V1a, V1b, V1c, V2a, V2b, V2c, V2d, X1a, X1b, V3c (clips, sidecars, `_qc`);
  - every `*-v1-*` file;
  - the V2d splice clips and the `_qc\v2d-splice\` folder.

  After the render and again after item-02: **161 unchanged, 0 changed/missing**. None of the 17 output names existed beforehand.
  My first hashing attempt failed on a quoting error (and then on the `v2d-splice` folder) *before* any render started; the
  render was held until the fingerprints existed.
6. **Render window:** **21:03:13 → 21:20:56 UTC, 2026-10-01** (17:03:13 → 17:20:56 Toronto EDT). 3 tasks in parallel,
   `--max-usd 8.00 --timeout-min 60`, and the runner exited 0. V6c's 433 s wall time was API queue time, not an error.

| shot | status | task id | wall s | length | frames | refs | est (list) | streams | verbatim | stills |
|---|---|---|---|---|---|---|---|---|---|---|
| V3a | done | `3e2922c0-82e6-4a01-9c86-486aea59c96e` | 164.1 | 6 s | 180 | 7 (family + Singa) | $0.60 | video | yes | f018/f090/f171 |
| V3b | done | `3b1371d1-a07c-43db-9ef8-7810b5aacbc1` | 132.0 | 3 s | 90 | 1 (Singa) | $0.30 | video | yes | f009/f045/f086 |
| X2a | done | `44f9ddd1-49d8-43e2-a7b7-54b5602a1109` | 164.7 | 6 s | 180 | 6 (family) | $0.60 | video | yes | f018/f090/f171 |
| X2b | done | `a5faf570-1e39-48a6-a373-6a8645a37fff` | 147.7 | 6 s | 180 | 6 (family) | $0.60 | video | yes | f018/f090/f171 |
| V4a | done | `5484ae42-850d-42d8-9567-74d441c1a112` | 194.8 | 6 s | 180 | 6 (family) | $0.60 | video | yes | f018/f090/f171 |
| V4b | done | `ca6cd6ac-d9ed-4671-a2c6-587a5d6730cb` | 83.5 | 3 s | 90 | 1 (Pani Karadi) | $0.30 | video | yes | f009/f045/f086 |
| V4c | done | `b3b9a7a9-df9e-42f0-8d7d-34ae91e8d0b5` | 132.0 | 4 s | 120 | 6 (family) | $0.40 | video | yes | f012/f060/f114 |
| X3a | done | `74fab326-be67-4553-a9da-abe24caa6dd6` | 131.5 | 6 s | 180 | 3 (Modhu, Singa, Pani Karadi) | $0.60 | video | yes | f018/f090/f171 |
| X3b | done | `c0e9a951-b335-469b-bba3-0d4ed2e0742a` | 147.9 | 6 s | 180 | 6 (family) | $0.60 | video | yes | f018/f090/f171 |
| V5a | done | `ee57ad80-82b9-4214-a3b7-8464d54f68ac` | 146.6 | 6 s | 180 | 6 (family) | $0.60 | video | yes | f018/f090/f171 |
| V5b | done | `8d88bf30-3e35-4a67-9508-8fe407a64e32` | 99.4 | 3 s | 90 | 1 (Chiku) | $0.30 | video | yes | f009/f045/f086 |
| V5c | done | `0a17120e-ad96-4b20-bad4-7babae8ca52a` | 132.2 | 4 s | 120 | 6 (family) | $0.40 | video | yes | f012/f060/f114 |
| V6a | done | `03973ace-33b2-4ae9-8c5f-e60b30d2c1d6` | 115.0 | 3 s | 90 | 1 (Chiku) | $0.30 | video | yes | f009/f045/f086 |
| V6b | done | `b59b5393-554a-4a3c-b0f5-72f40373b995` | 114.8 | 3 s | 90 | 6 (family) | $0.30 | video | yes | f009/f045/f086 |
| V6c | done | `7c2bd6a5-b7e4-4f80-a1eb-73d1630a30e4` | 432.6 | 3 s | 90 | 6 (family) | $0.30 | video | yes | f009/f045/f086 |
| V6d | done | `82b8a26d-6541-4795-9862-fe871e801441` | 115.5 | 3 s | 90 | 6 (family) | $0.30 | video | yes | f009/f045/f086 |
| T1 | done | `a60aa8e8-62ba-486b-b9d9-5e9c66c03a23` | 65.8 | 3 s | 90 | 0 (-) | $0.30 | video | yes | f009/f045/f086 |

"family" = `Appa|Appa|Mintu|Mintu|Minnu|Minnu` (face + body each). Task ids come from each clip's sidecar. "Verbatim" means the sidecar
prompt equals the shot's `*.raw.txt` (stripped).

- **Failures:** none. No URL or key appears in any sidecar or in the log. All 17 status cells are `done`.

## item-02 — sheets and stills
- **Contact sheets:** 5×2, 10 frames evenly spaced from the first frame to the last, 384 wide → 1920×432.
- **100% stills** at 10/50/95 % of the frame count (1280×720). The frame numbers are in the "stills" column above.
- Nothing was copied to the song folder.

## Paths
Clips and sidecars, for ID = V3a, V3b, X2a, X2b, V4a, V4b, V4c, X3a, X3b, V5a, V5b, V5c, V6a, V6b, V6c, V6d, T1:
- `C:\Projects\opencode\video_image\songs\rowboat\out\<ID>-seed30313-w3.mp4` (+ `.json`)

For example:
- `C:\Projects\opencode\video_image\songs\rowboat\out\V3a-seed30313-w3.mp4`
- `C:\Projects\opencode\video_image\songs\rowboat\out\X3a-seed30313-w3.mp4`
- `C:\Projects\opencode\video_image\songs\rowboat\out\T1-seed30313-w3.mp4`

QC in `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\`: per shot `<ID>-strip.png`, `<ID>-contact.png` and the three stills,
e.g. `...\_qc\X3a-contact.png`, `...\_qc\X3a-f018.png`, `...\_qc\X3a-f090.png`, `...\_qc\X3a-f171.png`.

Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_w2fix_w3w4.log`

## Commit
The `[skip ci]` commit containing this report. It holds `comfy/prompt_lint.py` (animal aliases, off-screen-object warning),
`songs/rowboat/lint.json`, `songs/rowboat/_make_rowboat.py`, the changed `shots/*.raw.txt` (V3a, V3b, V4b, V5b, V6a), `shots.csv`
(all 29 `done`), `cutplan.json` (Fable's change: the V2d take = splice2), the queue folder and this report. `out/` is not included.
The hash is in CC's chat reply. Not committed: Fable's uncommitted edit to `REVIEW-learning-batch1-2026-09-29.md`.

## Not judged
Fable reviews.
