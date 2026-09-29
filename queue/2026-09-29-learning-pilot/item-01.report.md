# item-01 report — check and render (≤ $3.20 list)

- **Credentials:** `credentials present: True`. No values were printed.
- **Dry-run 1** (`songs\shorts-learning --only C1_w3,F3_w3,FD1_w3,AC2_w3,V2_w3`): 5 rows, all `audio=on`, 720P 9:16 5 s.
  C1, F3 and V2 have refs=0; FD1 (Mintu) and AC2 (Minnu) have refs=1. Total **`estimated $2.50`**, exit 0, 0 MISSING/ERROR hits.
- **Dry-run 2** (`songs\shorts-loops --only L04_w3d`): 1 row, `audio=on`, 5 s, refs=1 (Minnu), **`estimated $0.50`**, 0 hits.
- **Run windows**, all on 2026-09-29:

| batch | UTC | Toronto (EDT) |
|---|---|---|
| learning pilot (5 rows, 3 in parallel, `--max-usd 2.60`) | 12:46:54 → 12:51:22 | 08:46:54 → 08:51:22 |
| L04_w3d (`--max-usd 0.60`) | 12:51:22 → 12:53:51 | 08:51:22 → 08:53:51 |

| row | status | task id | wall s | length | est (list) |
|---|---|---|---|---|---|
| C1_w3 | done | `fba5d899-2e1d-4c13-b00a-d5c154598ed2` | 111.5 | 5 s | $0.50 |
| F3_w3 | done | `b94698b1-e502-49c8-a183-1f00c0694459` | 124.4 | 5 s | $0.50 |
| FD1_w3 | done | `3443ab40-1aa1-4c5b-be21-752372188934` | 152.3 | 5 s | $0.50 |
| AC2_w3 | done | `22d5c490-f1f3-48fc-955f-ee5eec4cc3ed` | 150.8 | 5 s | $0.50 |
| V2_w3 | done | `bbd82b69-4d3e-44a2-866e-4872765fede5` | 112.3 | 5 s | $0.50 |
| L04_w3d | done | `acc52b4b-139f-4111-95e6-bb15ef73b97b` | 147.2 | 5 s | $0.50 |

- **Total estimate: $3.00 at list price** (~$2.10 with the 30% discount); cap $3.20.
- **Failures:** none. Both runners exited 0.
- All six clips have a video and an audio stream: 720P 9:16 in `usage`.
- No URL or key appears in any sidecar or in the two logs.
- Logs:
  - `C:\Projects\opencode\video_image\songs\shorts-learning\batch_pilot.log`
  - `C:\Projects\opencode\video_image\songs\shorts-loops\batch_retakes3.log`
