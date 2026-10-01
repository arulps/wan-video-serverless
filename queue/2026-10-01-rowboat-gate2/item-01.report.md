# item-01 report — checks and render V1a + V1b (≤ $1.00 list)

- **Mock:** `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Dry-run** (`--only V1a,V1b`): 2 rows, both `720P 16:9 audio=off`, **`estimated $0.90`**, exit 0, 0 MISSING/ERROR hits.
- **Seating check:** both `03_V1a.raw.txt` and `04_V1b.raw.txt` contain "two low wooden benches face each other"; "side by side" is in no `*.raw.txt`.
- **Render window:** **15:09:27 → 15:12:43 UTC, 2026-10-01** (11:09:27 → 11:12:43 Toronto EDT). `--max-usd 1.00`; the runner exited 0.

| shot | status | task id | wall s | length | est (list) |
|---|---|---|---|---|---|
| V1a | done | `5d302529-dcc3-4667-b5fd-39c4d19ed2de` | 195.2 | 6 s | $0.60 |
| V1b | done | `468a6fb5-4b3f-4698-9d17-8ff9923e22f5` | 147.9 | 3 s | $0.30 |

- **Failures:** none. Prompts were sent verbatim. No URL or key appears in the sidecars or the log. The rim-seat files are untouched.
- Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_gate2.log`
