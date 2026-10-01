# item-01 report — checks and render V1a (≤ $0.70 list)

- **Mock:** `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Dry-run, all 29 rows:** 29 rows, all `720P 16:9 audio=off`, total **`estimated $12.90`**, exit 0, 0 MISSING/ERROR hits.
  V1a: 6 s, refs=6 (Appa ×2, Mintu ×2, Minnu ×2), est $0.60.
- **Render window:** **14:34:44 → 14:37:14 UTC, 2026-10-01** (10:34:44 → 10:37:14 Toronto EDT). `--max-usd 0.70`; the runner exited 0.

| row | status | task id | wall s | length | est (list) |
|---|---|---|---|---|---|
| V1a | done | `46c02932-f924-430b-80fb-1c164849d89f` | 148.9 | 6 s | $0.60 |

- **Failures:** none. Video only (audio off), 1280×720 @ 30 fps, 180 frames.
- The sidecar prompt equals `shots\03_V1a.raw.txt` verbatim, apart from the trailing newline.
- No URL or key appears in the sidecar or the log.
- Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_gate.log`
