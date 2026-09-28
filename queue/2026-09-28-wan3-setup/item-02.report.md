# item-02 report — render through the Wan 3.0 API

**Result: 3/3 SUCCEEDED, 0 failed. L01_w3 was not run (no keyframe, per item-01).**

## Run window, for the console bill
| | UTC | Toronto (EDT, UTC−4) |
|---|---|---|
| start | 2026-09-28 15:18:03 | 2026-09-28 11:18:03 |
| end | 2026-09-28 15:20:44 | 2026-09-28 11:20:44 |

- Command: `batch_runner.py --song songs\_ab7-2026-09-28-wan3 --hosts api,api,api --max-usd 1.60 --timeout-min 30`.
  It ran with `PYTHONUTF8=1` so the Windows console/tee handles the UTF-8 in the runner's output.
- The log is `batch_6e.log`. It has no `code: message` line: there were no auth, region, model or quota errors.

## Per row
All three: model `wan3.0-video` at 720P 16:9, 5 s, seed 30313, list-price estimate $0.50.
Output 1280×720 @ 30 fps, 150 frames.

| row | task id | status | wall s | refs |
|---|---|---|---|---|
| T04_w3 | `cea3ca0c-2174-44c1-ae5f-b8103302129f` | SUCCEEDED | 151.5 | 2 |
| T07_w3 | `38371c07-f182-4f21-bfb4-4c196b3953ab` | SUCCEEDED | 152.6 | 3 |
| T08_w3 | `8195eb38-99c7-4e19-9698-fb1a324fdbd3` | SUCCEEDED | 153.0 | 3 |

Sidecar `usage` block, identical for all three:
`{'duration': 5.0, 'input_video_duration': 0.0, 'output_video_duration': 5.0, 'fps': 30, 'video_count': 1, 'SR': 720, 'ratio': '16:9'}`

**Total estimate: $1.50 at list price** (~$1.05 if the console's 30% launch discount applies). The actual charge is in the
Model Studio console under Usage & Billing, for the window above.

- The sidecars were checked for `http(s)://` and `sk-`: none present.
- `shots.csv` status cells were set to `done` by the runner.

## Paths
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\T04_w3-seed30313-w3.mp4` · `...\out\T04_w3-seed30313-w3.json` · `...\out\_qc\T04_w3-strip.png`
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\T07_w3-seed30313-w3.mp4` · `...\out\T07_w3-seed30313-w3.json` · `...\out\_qc\T07_w3-strip.png`
- `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\out\T08_w3-seed30313-w3.mp4` · `...\out\T08_w3-seed30313-w3.json` · `...\out\_qc\T08_w3-strip.png`
- Log: `C:\Projects\opencode\video_image\songs\_ab7-2026-09-28-wan3\batch_6e.log`
