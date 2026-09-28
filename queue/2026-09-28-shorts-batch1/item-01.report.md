# item-01 report — check and render the 19 Shorts

- **Credentials:** `credentials present: True`. No values were printed.
- **Dry-run** (`--only L02_w3 … L20_w3`): **19 rows, all `audio=on`**, total **`estimated $9.70`** at list price, exit 0.
  A case-sensitive grep for `MISSING|ERROR|OVER BUDGET|refused|Traceback` found 0 hits. A case-insensitive grep had matched
  ordinary prompt words ("falling over", "dungarees over"); those were false positives, not problems.
  - All rows: `wan3.0-video` 720P 9:16. L03 and L14 are 6 s ($0.60); the other 17 are 5 s ($0.50).
  - Refs: 12 rows have 1 ref (6× Minnu, 6× Mintu), 6 rows have 2 (Amma/Mintu ×2, Paati/Mintu, Thatha/Minnu, Thatha/Mintu),
    and 1 row has 3 (Thatha/Mintu/Minnu).
- **Render window:** **20:41:46 → 20:59:01 UTC** (16:41:46 → 16:59:01 Toronto EDT). Three tasks ran in parallel,
  `--max-usd 10.50`, and the runner exited 0.
- **Failures:** none. No `FAILED`, `code:` or error line in `batch_shorts1.log`.
- No URL or key appears in any of the 19 sidecars or in the log (grepped).

| row | status | task id | wall s | length | est (list) |
|---|---|---|---|---|---|
| L02_w3 | done | `537b1f28-efbe-4d35-96ab-4da11953862b` | 147.4 | 5.0 s | $0.50 |
| L03_w3 | done | `461aa2e8-c193-4c3f-a3ac-6e283e8fb619` | 163.1 | 6.0 s | $0.60 |
| L04_w3 | done | `a2276e9e-71fd-4070-9cd9-accf306d3681` | 147.3 | 5.0 s | $0.50 |
| L05_w3 | done | `ae6c0535-5876-4a9b-b27d-bd3d55943161` | 145.7 | 5.0 s | $0.50 |
| L06_w3 | done | `7955a43b-9706-48b1-84d6-5eaf33daf07c` | 145.7 | 5.0 s | $0.50 |
| L07_w3 | done | `02da67ab-e49b-4dfe-9daf-70d04b316a30` | 146.6 | 5.0 s | $0.50 |
| L08_w3 | done | `f6884085-aa8c-4cad-bfed-43da157e452a` | 145.7 | 5.0 s | $0.50 |
| L09_w3 | done | `0229085a-4897-4cc6-8f54-a2aaadb37fbe` | 146.1 | 5.0 s | $0.50 |
| L10_w3 | done | `ab229355-70a9-481b-9929-3f37814ea16d` | 146.8 | 5.0 s | $0.50 |
| L11_w3 | done | `4d54c30b-04f5-4838-a3b1-e948f30b5535` | 146.3 | 5.0 s | $0.50 |
| L12_w3 | done | `b58fee31-5e2b-4d52-b947-3aadd5f3bc7f` | 146.2 | 5.0 s | $0.50 |
| L13_w3 | done | `59e04dc0-feb5-4819-ba45-01c7fcfa64f1` | 146.2 | 5.0 s | $0.50 |
| L14_w3 | done | `62e8e914-dbf2-48e3-9ef1-6548287fba61` | 146.1 | 6.0 s | $0.60 |
| L15_w3 | done | `85b4a427-a946-4a03-9ddd-812972f26f08` | 146.0 | 5.0 s | $0.50 |
| L16_w3 | done | `54c19a18-8738-4faa-b48d-b142e112a7e7` | 147.4 | 5.0 s | $0.50 |
| L17_w3 | done | `93168b40-919a-4c38-9aa3-588b3a09794c` | 146.4 | 5.0 s | $0.50 |
| L18_w3 | done | `835d6098-4bee-4ed2-86be-cba5175e01d0` | 146.0 | 5.0 s | $0.50 |
| L19_w3 | done | `6cb7d080-d350-4070-b413-ef8a91c2a2bd` | 146.4 | 5.0 s | $0.50 |
| L20_w3 | done | `c3db8cb9-c9eb-42bc-8ea7-1c66b3635c9c` | 146.5 | 5.0 s | $0.50 |

**Total estimate: $9.70 at list price** (17 × $0.50 + 2 × $0.60), about $6.80 with the 30% discount; cap $10.50.
The runner reported 46.6 task-minutes. `shots.csv`: all 19 `Lxx_w3` status cells were set to `done` by the runner.

- Log: `C:\Projects\opencode\video_image\songs\shorts-loops\batch_shorts1.log`
- Clips: `C:\Projects\opencode\video_image\songs\shorts-loops\out\Lxx_w3-seed30313-w3.mp4` (+ `.json`, `_qc\Lxx_w3-strip.png`), xx = 02..20
