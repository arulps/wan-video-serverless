# CC-REPORT — Rowboat final: T1 + V5c retakes and Tamil/English rough cuts, L04 Row Row Row Your Boat (2026-10-01)

Queue `queue\2026-10-01-rowboat-final`.

## item-01 — T1 + V5c ($0.70 list; cap $1.00)
- Mock PASS, credentials True, lint test PASS, `LINT PASS: 2 shots, 0 fail, 0 warn`.
- Dry-run 2 rows `720P 16:9 audio=off`, **estimated $0.70**. Packs: both `Appa|Appa|Mintu|Mintu|Minnu|Minnu`.
- **Render window:** **21:44:57 → 21:47:42 UTC, 2026-10-01** (17:44:57 → 17:47:42 Toronto EDT).

| shot | status | task id | wall s | length | frames | refs | est (list) | stills |
|---|---|---|---|---|---|---|---|---|
| T1 | done | `f83967fd-aa3d-45aa-8a4e-bb3c8cc4cb58` | 163.3 | 3 s | 90 | 6 (family) | $0.30 | f009/f045/f086 |
| V5c | done | `d2bff217-abee-40ab-bd8c-6f30b055313f` | 115.9 | 4 s | 120 | 6 (family) | $0.40 | f012/f060/f114 |

- Both are 1280×720 @ 30 fps, video only. The prompts were sent verbatim (they equal the `*.raw.txt`). No URL or key appears in the
  sidecars or the log.
- **Protected:** 280 files (the 27 done shots' files, every `*-v1-*`, every `*splice*`), md5 unchanged.
- **All 29 song shots are `done`.**

Paths:
- `C:\Projects\opencode\video_image\songs\rowboat\out\T1-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\V5c-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\T1-contact.png`, `T1-f009.png`, `T1-f045.png`, `T1-f086.png`, `T1-strip.png`
- `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\V5c-contact.png`, `V5c-f012.png`, `V5c-f060.png`, `V5c-f114.png`, `V5c-strip.png`
- Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_final.log`

## item-03 — Tamil + English rough cuts ($0)

- Command: `python comfy\song_cuts.py songs\rowboat cut --lang both --src out --force` → exit 0, run **21:49:08 → 21:59:47 UTC**.
  The log is `C:\Projects\opencode\video_image\songs\rowboat\cuts_rough1.log`.

| cut | path | duration | size | video | audio |
|---|---|---|---|---|---|
| Tamil | `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-TA.mp4` | **123.767 s** (plan 123.76; audio 123.760 s) | 170,269,807 B | h264 1920×1080 30 fps | 1× AAC 48 kHz stereo |
| English | `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-EN.mp4` | **96.920 s** (plan 96.92; audio 96.920 s) | 132,972,693 B | h264 1920×1080 30 fps | 1× AAC 48 kHz stereo |

- **Cutlogs:**
  - `...\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-TA.cutlog.txt` lists 29 shots (01 I1 … 29 T1).
  - `...\_cuts\L04-ROW-ROW-ROW-YOUR-BOAT-ROUGH-EN.cutlog.txt` lists 24 shots. X1a, X1b, X2a, X2b and T1 have no English slot in
    `cutplan.json` (`en_in`/`en_out` = None), so they are omitted by design.
  - The cutlogs give in-point / use / slip / transition per shot but not file names. **The take per shot is from `cutplan.json`:**
    every shot uses `<ID>-seed30313-w3.mp4`, except **V2d = `V2d-seed30313-w3-splice2.mp4`** (Fable's hand-built take, as intended).
- **Bad / missing shots: 0.** The log has 0 lines matching bad|missing|error|warn|not found.
- Also written by the tool in `_cuts\`: `_graph-ta.txt` (updated) and `_graph-en.txt` (new), the ffmpeg filter graphs.
- `_cuts\_partial-interrupted-TA.mp4` was left in place, md5 unchanged. Arul can delete it.
- **Song folder:** the 34 files outside `_cuts\` were fingerprinted before item-03. After it: 34 unchanged, 0 changed, 0 new.
  Only `_cuts\` was written. The 280 protected render files in `songs\rowboat\out\` are also unchanged.

## Total
API: **$0.70 at list price** (~$0.49 with the 30% discount); cap $1.00. Cuts: $0.

## Commits
- Item-02: `0e14b17`, with `_make_rowboat.py`, `lint.json`, `shots/` (T1, V5c), `shots.csv` and the queue folder.
  `cutplan.json` was unchanged, so a no-op.
- Item-03 + queue end: the `[skip ci]` commit containing this updated report. The hash is in CC's chat reply.
- Not committed: `out/`, the `_cuts\` outputs (in the song folder, outside the repo), the batch/cut logs, and Fable's uncommitted
  edit to `REVIEW-learning-batch1-2026-09-29.md`.

## Not judged
Fable reviews the takes and the rough cuts.
