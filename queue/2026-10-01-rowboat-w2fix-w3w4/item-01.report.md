# item-01 report — checks and render 17 shots (≤ $8.00 list)

- **Mock:** `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Lint:** `tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`. `prompt_lint.py` → last line
  `LINT PASS: 17 shots, 0 fail, 1 warn`. The WARN is R8 (no reference images: T1).
- **Dry-run:** 17 rows, all `720P 16:9 audio=off`, **`estimated $7.40`**, exit 0, 0 MISSING/ERROR hits.
- **Pack check:** V3a family + Singa, V4c family, X3a `Modhu|Singa|Pani Karadi`. OK.
- **Protected files:** 161 (the 12 done shots' files, `*-v1-*`, the V2d splices), unchanged after the run by md5.
- **Render window:** **21:03:13 → 21:20:56 UTC, 2026-10-01** (17:03:13 → 17:20:56 Toronto EDT). 3 in parallel, `--max-usd 8.00`;
  the runner exited 0.

| shot | status | task id | wall s | length | frames | refs | est (list) | streams | verbatim |
|---|---|---|---|---|---|---|---|---|---|
| V3a | done | `3e2922c0-82e6-4a01-9c86-486aea59c96e` | 164.1 | 6 s | 180 | 7 (family + Singa) | $0.60 | video | yes |
| V3b | done | `3b1371d1-a07c-43db-9ef8-7810b5aacbc1` | 132.0 | 3 s | 90 | 1 (Singa) | $0.30 | video | yes |
| X2a | done | `44f9ddd1-49d8-43e2-a7b7-54b5602a1109` | 164.7 | 6 s | 180 | 6 (family) | $0.60 | video | yes |
| X2b | done | `a5faf570-1e39-48a6-a373-6a8645a37fff` | 147.7 | 6 s | 180 | 6 (family) | $0.60 | video | yes |
| V4a | done | `5484ae42-850d-42d8-9567-74d441c1a112` | 194.8 | 6 s | 180 | 6 (family) | $0.60 | video | yes |
| V4b | done | `ca6cd6ac-d9ed-4671-a2c6-587a5d6730cb` | 83.5 | 3 s | 90 | 1 (Pani Karadi) | $0.30 | video | yes |
| V4c | done | `b3b9a7a9-df9e-42f0-8d7d-34ae91e8d0b5` | 132.0 | 4 s | 120 | 6 (family) | $0.40 | video | yes |
| X3a | done | `74fab326-be67-4553-a9da-abe24caa6dd6` | 131.5 | 6 s | 180 | 3 (Modhu, Singa, Pani Karadi) | $0.60 | video | yes |
| X3b | done | `c0e9a951-b335-469b-bba3-0d4ed2e0742a` | 147.9 | 6 s | 180 | 6 (family) | $0.60 | video | yes |
| V5a | done | `ee57ad80-82b9-4214-a3b7-8464d54f68ac` | 146.6 | 6 s | 180 | 6 (family) | $0.60 | video | yes |
| V5b | done | `8d88bf30-3e35-4a67-9508-8fe407a64e32` | 99.4 | 3 s | 90 | 1 (Chiku) | $0.30 | video | yes |
| V5c | done | `0a17120e-ad96-4b20-bad4-7babae8ca52a` | 132.2 | 4 s | 120 | 6 (family) | $0.40 | video | yes |
| V6a | done | `03973ace-33b2-4ae9-8c5f-e60b30d2c1d6` | 115.0 | 3 s | 90 | 1 (Chiku) | $0.30 | video | yes |
| V6b | done | `b59b5393-554a-4a3c-b0f5-72f40373b995` | 114.8 | 3 s | 90 | 6 (family) | $0.30 | video | yes |
| V6c | done | `7c2bd6a5-b7e4-4f80-a1eb-73d1630a30e4` | 432.6 | 3 s | 90 | 6 (family) | $0.30 | video | yes |
| V6d | done | `82b8a26d-6541-4795-9862-fe871e801441` | 115.5 | 3 s | 90 | 6 (family) | $0.30 | video | yes |
| T1 | done | `a60aa8e8-62ba-486b-b9d9-5e9c66c03a23` | 65.8 | 3 s | 90 | 0 (-) | $0.30 | video | yes |

- **Total: 74 s, estimated $7.40 at list price** (~$5.18 with the 30% discount); cap $8.00.
- **Failures:** none. No URL or key appears in the sidecars or the log. All 17 status cells are `done`; all 29 song shots are now `done`.
- Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_w2fix_w3w4.log`
