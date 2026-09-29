# item-01 report — check and render the 3 retakes

- **Credentials:** `credentials present: True`. No values were printed.
- **Dry-run** (`--only L03_w3b,L04_w3b,L10_w3b`): 3 rows, all `audio=on`, exit 0, total **`estimated $1.60`**.
  L03_w3b is 6 s at seed 4242 (3 refs: Thatha, Mintu, Minnu). L04_w3b (ref Minnu) and L10_w3b (ref Mintu) are 5 s at seed 30313.
  Grep for `MISSING|ERROR|OVER BUDGET|refused|Traceback`: 0 hits.
- **Render window:** **01:19:05 → 01:22:46 UTC, 2026-09-29** (21:19:05 → 21:22:46 Toronto EDT, 2026-09-28). Three tasks ran
  in parallel, `--max-usd 1.80`, and the runner exited 0.

| row | status | task id | wall s | length | est (list) |
|---|---|---|---|---|---|
| L03_w3b | done | `c3588a8e-655b-4cbc-9de8-115a1db65027` | 211.3 | 6 s | $0.60 |
| L04_w3b | done | `9df92af4-6f70-43b9-b855-24fa357ca2f2` | 163.5 | 5 s | $0.50 |
| L10_w3b | done | `d7a48f51-ac3e-4095-b72e-ae6687a6692a` | 178.9 | 5 s | $0.50 |

- **Total estimate: $1.60 at list price** (~$1.12 with the 30% discount); cap $1.80.
- **Failures:** none.
- All three have a video and an audio stream: 720P 9:16 in `usage`.
- No URL or key appears in the sidecars or in the log.
- Log: `C:\Projects\opencode\video_image\songs\shorts-loops\batch_retakes1.log`
