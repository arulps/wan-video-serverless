# item-01 report — check and render 5 rows (≤ $3.00 list)

- **Credentials:** `credentials present: True`. No values were printed.
- **Dry-run** (`--only SN1_w3c,SN2_w3c,SN3_w3c,SN6_w3c,A6_w3c`): 5 rows, all `audio=on`. The SN rows have refs=1;
  A6_w3c has refs=0 with `first=` and `last=` both `keyframes/A6-gate-empty.png`. Total **`estimated $2.50`**, exit 0,
  0 MISSING/ERROR hits.
- **Render window:** **17:31:44 → 17:35:39 UTC, 2026-09-29** (13:31:44 → 13:35:39 Toronto EDT). 3 tasks ran in parallel,
  `--max-usd 3.00`, and the runner exited 0.

| row | refs | frames | status | task id | wall s | length | est (list) | streams |
|---|---|---|---|---|---|---|---|---|
| SN1_w3c | 1 | - | done | `8558ea2f-d049-4954-9ca2-635318a3a03d` | 115.1 | 5.0 s | $0.50 | video+audio |
| SN2_w3c | 1 | - | done | `ba6e7059-8b70-43f0-83cb-7fa5ed351106` | 115.0 | 5.0 s | $0.50 | video+audio |
| SN3_w3c | 1 | - | done | `556e6ef1-c5fc-4ad9-aa36-74e8ee0e04f1` | 130.7 | 5.0 s | $0.50 | video+audio |
| SN6_w3c | 1 | - | done | `35ed75a9-976f-4d2c-acb1-a36c2fa5ee67` | 114.9 | 5.0 s | $0.50 | video+audio |
| A6_w3c | 0 | first=last=keyframe | done | `ef91d918-1ed8-42d0-9a18-c3501edc0984` | 100.9 | 5.0 s | $0.50 | video+audio |

- **Total estimate: $2.50 at list price** (~$1.75 with the 30% discount); cap $3.00.
- **Failures:** none.
- All 5 have video + audio. No URL or key appears in any sidecar or the log. All 5 status cells are `done`.
- Log: `C:\Projects\opencode\video_image\songs\shorts-learning\batch_learning4.log`
