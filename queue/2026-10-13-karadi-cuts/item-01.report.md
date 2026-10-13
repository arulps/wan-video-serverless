# item-01 report — DONE: cutplan written, 18 clips staged, TA + EN 1080p rough cuts made — $0.00

Run by CC (A12 watcher), 2026-10-13 15:41–15:45 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
Local ffmpeg only; no API call. The cuts were not judged.

Song folder below = `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama`.

## Step 1 — cut plan
`py "<song folder>\_gen\make_cutplan.py" songs\a12-karadi-w3` printed:
```
wrote songs/a12-karadi-w3\cutplan.json: TA 29 slots 154.800 s, EN 24 slots 128.000 s, 18 clips — all slots fit their clips, no gaps
```
(As expected. The console showed the dash as a replacement character — a code-page display issue only.)
No `CUTPLAN CHECK FAILED`. `cutplan.json` → `song_folder` = `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama`. OK.

## Step 2 — stage
`py comfy\song_cuts.py songs\a12-karadi-w3 stage` → exit 0, 18 files copied into the song folder:
```
staged  01_I1_intro-the-picnic-nuts-for-new-friends.mp4 <- I1-seed30313-w3.mp4
staged  02_CQa_chorus-question-karadi-mama-where-are-you-going-.mp4 <- CQa-seed30313-w3.mp4
staged  06_HKa_hook-karadi-mama-strolls-along-the-trail.mp4 <- HKa-seed30313-w3.mp4
staged  04_CAa_chorus-answer-my-home-is-near-the-forest-spin-an.mp4 <- CAa-seed30313-w3.mp4
staged  07_HKb_hook-clap-along-on-the-picnic-blanket.mp4 <- HKb-seed30313-w3.mp4
staged  08_V1Q_verse-1-question-minnu-your-woolly-coat-looks-ni.mp4 <- V1Q-seed30313-w3.mp4
staged  09_V1A_verse-1-answer-a-gift-from-god.mp4 <- V1A-seed30313-w3.mp4
staged  03_CQb_chorus-question-karadi-mama-where-are-you-going-.mp4 <- CQb-seed30313-w3.mp4
staged  05_CAb_chorus-answer-my-home-is-near-the-forest-spin-an.mp4 <- CAb-seed30313-w3.mp4
staged  10_V2Q_verse-2-question-mintu-a-honeycomb-in-your-hand.mp4 <- V2Q-seed30313-w3.mp4
staged  11_V2A_verse-2-answer-the-busy-little-bees-made-it.mp4 <- V2A-seed30313-w3.mp4
staged  12_V3Q_verse-3-question-everyone-little-fish-in-your-ba.mp4 <- V3Q-seed30313-w3.mp4
staged  13_V3A_verse-3-answer-i-caught-them-in-the-river-splash.mp4 <- V3A-seed30313-w3.mp4
staged  14_V4Q_verse-4-question-the-rabbit-and-the-squirrel-blu.mp4 <- V4Q-seed30313-w3.mp4
staged  15_V4A_verse-4-answer-i-picked-them-in-the-forest-every.mp4 <- V4A-seed30313-w3.mp4
staged  16_O1_outro-1-karadi-mama-shares-his-blueberries.mp4 <- O1-seed30313-w3.mp4
staged  17_O2_outro-2-everyone-s-bear-walk-with-karadi-mama.mp4 <- O2-seed30313-w3.mp4
staged  18_O3_outro-3-spin-skip-wave-and-home-to-the-forest.mp4 <- O3-seed30313-w3.mp4
```

## Step 3 — cuts
`py comfy\song_cuts.py songs\a12-karadi-w3 cut --lang both` → exit 0. Final lines per language, verbatim:
```
plan: 4644 frames (154.800 s)
wrote C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\A12-KARADI-MAMA-ROUGH-TA.mp4 4644 video frames = plan 4644; container 154.800 s (audio 154.800 s)
plan: 3840 frames (128.000 s)
wrote C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\A12-KARADI-MAMA-ROUGH-EN.mp4 3840 video frames = plan 3840; container 128.000 s (audio 128.000 s)
```

| Cut | Path (in `<song folder>\_cuts\`) | Frames (`ffprobe -count_frames`) | Size | Duration | Bytes |
|---|---|---|---|---|---|
| Tamil | `A12-KARADI-MAMA-ROUGH-TA.mp4` | **4644** = plan | 1920×1080, 30 fps | 154.800 s | 167,394,254 |
| English | `A12-KARADI-MAMA-ROUGH-EN.mp4` | **3840** = plan | 1920×1080, 30 fps | 128.000 s | 136,622,182 |

**"holds last frame" lines: none** (searched the full output of the cut step).
The opening trims are in the plan as Fable specified: the EN log shows `EN-INTRO-01=I1 … slip 1.200` and `HKb … slip 1.000` /
`slip 1.800`.

`song_cuts.py` also wrote, in `_cuts\`: `A12-KARADI-MAMA-ROUGH-TA.cutlog.txt`, `A12-KARADI-MAMA-ROUGH-EN.cutlog.txt`,
`_graph-ta.txt`, `_graph-en.txt`.

## Step 4 — contact sheets (in `<song folder>\_cuts\`)
- `A12-ROUGH-TA-sheet.jpg` — 2400×1080: 10 columns × 8 rows, 71 frames.
- `A12-ROUGH-EN-sheet.jpg` — 2400×810: 10 columns × 6 rows, 58 frames.

One frame every 2.2 s, 240 px wide, timestamp (h:mm:ss.ms of the cut) burned into each frame. ffmpeg's `fps=1/2.2` takes the
frame at the middle of each 2.2 s window, so the stamps read 1.067 s, 3.267 s, 5.467 s, … rather than 0.0, 2.2, 4.4.
The EN sheet was opened once to confirm the stamps are burned in; nothing was judged.

## What was written where
- Song folder: only the 18 staged `NN_ID_slug.mp4` copies and `_cuts\`. WAVs/MP3s, `refs\`, `_gen\` and the runsheet files untouched
  (the plan script in `_gen\` was run, not edited).
- Repo: `songs\a12-karadi-w3\cutplan.json` (new). `shots.csv`, the shot files and `out\` untouched.

## Step 5 — commit
`[skip ci]`, explicit paths: `songs/a12-karadi-w3/cutplan.json`, `queue/2026-10-13-karadi-batch1/FABLE-VERDICT.md`,
`queue/2026-10-13-karadi-cuts`, `queue/A12-WATCH-LOG.md`. The hash is in this folder's `LOG.md` done line and `item-01.done`
(this report is inside that commit; the markers follow in a small `[skip ci]` commit).

## Spend
$0.00. A12 total unchanged: $13.00 list (conservative) of $15.00.
