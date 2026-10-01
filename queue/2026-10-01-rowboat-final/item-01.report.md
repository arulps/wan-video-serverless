# item-01 report — checks and render T1 + V5c (≤ $1.00 list)

- **Mock:** `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Lint:** `tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`. `prompt_lint.py --only T1,V5c` →
  `LINT PASS: 2 shots, 0 fail, 0 warn`.
- **Dry-run:** 2 rows, `720P 16:9 audio=off` (V5c 4 s $0.40, T1 3 s $0.30), **`estimated $0.70`**, 0 MISSING/ERROR hits.
- **Pack check:** T1 and V5c are both `Appa|Appa|Mintu|Mintu|Minnu|Minnu`. OK.
- **Protected files:** 280 (all files of the 27 done shots, every `*-v1-*`, every `*splice*`), md5 unchanged after the run.
  The old takes are `T1-seed30313-w3-v1-invented-family.*` and `V5c-seed30313-w3-v1-worried-faces.*`; there were no name collisions.
- **Render window:** **21:44:57 → 21:47:42 UTC, 2026-10-01** (17:44:57 → 17:47:42 Toronto EDT). 2 tasks in parallel,
  `--max-usd 1.00`; the runner exited 0.

| shot | status | task id | wall s | length | frames | refs | est (list) |
|---|---|---|---|---|---|---|---|
| T1 | done | `f83967fd-aa3d-45aa-8a4e-bb3c8cc4cb58` | 163.3 | 3 s | 90 | 6 (family) | $0.30 |
| V5c | done | `d2bff217-abee-40ab-bd8c-6f30b055313f` | 115.9 | 4 s | 120 | 6 (family) | $0.40 |

- **Total: 7 s, estimated $0.70 at list price** (~$0.49 with the 30% discount); cap $1.00.
- **Failures:** none. Both are 1280×720 @ 30 fps, video only. Prompts were sent verbatim. No URL or key appears in the sidecars or the log.
- All 29 song shots are `done`.
- Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_final.log`
