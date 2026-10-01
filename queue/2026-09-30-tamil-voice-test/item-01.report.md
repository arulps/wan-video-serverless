# item-01 report — check and render 2 rows (≤ $1.20 list)

- **Credentials:** `credentials present: True`. No values were printed.
- **Dry-run** (`--only C1_w3ta,C1_w3tr`): 2 rows, `audio=on`, refs=1 (Minnu), **`estimated $1.00`**, exit 0, 0 MISSING/ERROR hits.
- **Render window:** **03:27:10 → 03:30:14 UTC, 2026-10-01** (23:27:10 → 23:30:14 Toronto EDT, 2026-09-30). 2 tasks ran in parallel,
  `--max-usd 1.20`, and the runner exited 0.

| row | status | task id | wall s | length | est (list) |
|---|---|---|---|---|---|
| C1_w3ta | done | `cd84ea2d-1d91-4843-9a9c-a39db49233d9` | 178.8 | 5 s | $0.50 |
| C1_w3tr | done | `b242bb4c-67eb-44aa-8fd4-8fa4f468de27` | 178.8 | 5 s | $0.50 |

- **Failures:** none. Both have video + audio. No URL or key appears in the sidecars or the log.
- The sidecar prompt of C1_w3ta holds the Tamil script intact (31 Tamil characters); C1_w3tr holds the Latin transliteration.
- Log: `C:\Projects\opencode\video_image\songs\shorts-learning\batch_tamil_test.log`
