# item-01 report — checks and render 9 shots (≤ $4.00 list)

- **Mock:** `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Lint gate (2b):** `tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`.
  `prompt_lint.py --only …` → last line `LINT PASS: 9 shots, 0 fail, 0 warn`, with no FAIL lines.
- **Dry-run:** 9 rows, all `720P 16:9 audio=off`, **`estimated $3.50`**, exit 0, 0 MISSING/ERROR hits.
- **Pack check:** V1b, V2a, V2b, V2d, V3a and V3c are `Appa|Appa|Mintu|Mintu|Minnu|Minnu`; V2c is the same `|Modhu`. OK.
- **Protected files** (67: all files of the done shots I1/I2/V1a/V1c/X1a, plus every `*-v1-*` clip, sidecar and `_qc` PNG):
  unchanged after the run, by md5. My first `md5sum -c` failed on my own CRLF/backslash manifest, which made the background task
  exit 1; re-verified in Python: 67/67 unchanged.
- **Render window:** **19:39:06 → 19:51:03 UTC, 2026-10-01** (15:39:06 → 15:51:03 Toronto EDT). 3 in parallel,
  `--max-usd 4.00 --timeout-min 40`; the runner exited 0.

| shot | status | task id | wall s | length | frames | refs (labels) | est (list) | streams | verbatim prompt |
|---|---|---|---|---|---|---|---|---|---|
| V1b | done | `b1dcb113-5e0b-4226-938a-c871c42a993e` | 116.1 | 3 s | 90 | 6 (family) | $0.30 | video | yes |
| V2a | done | `d8c50ccf-fd69-46b4-9590-d014ecfabd4c` | 102.0 | 3 s | 90 | 6 (family) | $0.30 | video | yes |
| V2b | done | `16dda29b-4d4e-429d-99bc-759b6ec19be3` | 116.5 | 3 s | 90 | 6 (family) | $0.30 | video | yes |
| V2c | done | `96e4af20-6bb8-44d1-a2cc-945a5d9f7a73` | 117.1 | 3 s | 90 | 7 (family + Modhu) | $0.30 | video | yes |
| V2d | done | `bc04df5f-14e0-4c6e-a146-733a2c3a4712` | 116.0 | 4 s | 120 | 6 (family) | $0.40 | video | yes |
| X1b | done | `9e94ff81-08db-4202-955b-2d09c5cec64e` | 595.8 | 6 s | 180 | 6 (family) | $0.60 | video | yes |
| V3a | done | `4bd907e9-a256-46ee-9f25-4ccd689f827a` | 155.6 | 6 s | 180 | 6 (family) | $0.60 | video | yes |
| V3b | done | `0c24c5fd-e0b8-4db8-aa75-df03b3bd8f4a` | 109.4 | 3 s | 90 | 1 (Singa) | $0.30 | video | yes |
| V3c | done | `908a19ff-e568-4f36-947a-a50733f08232` | 210.8 | 4 s | 120 | 6 (family) | $0.40 | video | yes |

- **Total: 35 s, estimated $3.50 at list price** (~$2.45 with the 30% discount); cap $4.00.
- **Failures:** none. X1b's 596 s was API queue time. No URL or key appears in the sidecars or the log. All 9 status cells are `done`.
- Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_w1fix_w2.log`
