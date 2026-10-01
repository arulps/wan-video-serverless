# item-01 report — checks and render world 1 (≤ $5.00 list)

- **Mock:** `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Dry-run** (10 shots): 10 rows, all `720P 16:9 audio=off`, **`estimated $4.50`**, exit 0, 0 MISSING/ERROR hits.
- **Seating check:** "on the low wooden bench at the other end of the boat" is in `04_V1b.raw.txt`; "face to face" is in no `*.raw.txt`.
- **Protected files:** V1a and all `*-v1-*` files (14, by md5) are unchanged after the run. V1a was not re-rendered.
- **Render window:** **17:57:50 → 18:08:41 UTC, 2026-10-01** (13:57:50 → 14:08:41 Toronto EDT). 3 tasks in parallel,
  `--max-usd 5.00`; the runner exited 0.

| shot | status | task id | wall s | length | frames | refs | est (list) | streams | verbatim prompt |
|---|---|---|---|---|---|---|---|---|---|
| I1 | done | `d5e86f59-d723-4ed3-b9a8-ad62a15d42e4` | 131.3 | 8.0 s | 240 | 0 | $0.80 | video | yes |
| I2 | done | `adc657df-3bb6-47e8-9fbb-e1c9328cd154` | 194.6 | 6.0 s | 180 | 6 | $0.60 | video | yes |
| V1b | done | `8c946de9-4034-403b-a8d8-b84387c85069` | 147.0 | 3.0 s | 90 | 4 | $0.30 | video | yes |
| V1c | done | `add135e2-f928-4510-843c-5e303e863ce3` | 162.5 | 3.0 s | 90 | 6 | $0.30 | video | yes |
| V2a | done | `7cfcd830-44cb-4853-9006-0054bf4e7ffe` | 147.6 | 3.0 s | 90 | 2 | $0.30 | video | yes |
| V2b | done | `90f16e98-dc06-4a29-8005-34f317d09334` | 163.4 | 3.0 s | 90 | 4 | $0.30 | video | yes |
| V2c | done | `ec3207f3-5af2-4877-b24d-ad3a3f032f08` | 156.9 | 3.0 s | 90 | 1 | $0.30 | video | yes |
| V2d | done | `61ef984a-4780-43e3-bec4-d18534447b7c` | 194.5 | 4.0 s | 120 | 4 | $0.40 | video | yes |
| X1a | done | `679acac1-d78b-4c7b-a8ca-06c5419fdf24` | 195.8 | 6.0 s | 180 | 7 | $0.60 | video | yes |
| X1b | done | `960137fc-c8ef-41a5-9b06-ad1db60fe00b` | 195.5 | 6.0 s | 180 | 6 | $0.60 | video | yes |

- **Total: 45 s, estimated $4.50 at list price** (~$3.15 with the 30% discount); cap $5.00.
- **Failures:** none. No URL or key appears in the sidecars or the log. All 10 status cells are `done`.
- Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_w1.log`
