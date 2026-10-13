# item-02 report — DONE: ROUGH2 cuts made with the four new clips — $0.00

Run by CC (A12 watcher), 2026-10-13 16:02–16:06 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
Local ffmpeg only; no API call. Neither the clips nor the cuts were judged.

Song folder below = `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama`.

## Step 1 — fallbacks
**None used.** All four new clips exist (`out\V1A…`, `V2A…`, `V3A…`, `V4A-seed30313-w3.mp4`, 180 frames each).
The `-v1-picnic` takes are still in `out\`, untouched.

## Step 2 — old staged copies retired (moved with `mv -n`, not deleted)
Into `<song folder>\_superseded-2026-10-13\` (new folder):
- `09_V1A_verse-1-answer-a-gift-from-god.mp4`
- `11_V2A_verse-2-answer-the-busy-little-bees-made-it.mp4`
- `13_V3A_verse-3-answer-i-caught-them-in-the-river-splash.mp4`
- `15_V4A_verse-4-answer-i-picked-them-in-the-forest-every.mp4`

## Step 3 — stage
`py comfy\song_cuts.py songs\a12-karadi-w3 stage` → `staged` for the four, `keep` for the other 14:
```
keep    01_I1_intro-the-picnic-nuts-for-new-friends.mp4
keep    02_CQa_chorus-question-karadi-mama-where-are-you-going-.mp4
keep    06_HKa_hook-karadi-mama-strolls-along-the-trail.mp4
keep    04_CAa_chorus-answer-my-home-is-near-the-forest-spin-an.mp4
keep    07_HKb_hook-clap-along-on-the-picnic-blanket.mp4
keep    08_V1Q_verse-1-question-minnu-your-woolly-coat-looks-ni.mp4
staged  09_V1A_verse-1-answer-a-gift-from-god.mp4 <- V1A-seed30313-w3.mp4
keep    03_CQb_chorus-question-karadi-mama-where-are-you-going-.mp4
keep    05_CAb_chorus-answer-my-home-is-near-the-forest-spin-an.mp4
keep    10_V2Q_verse-2-question-mintu-a-honeycomb-in-your-hand.mp4
staged  11_V2A_verse-2-answer-the-busy-little-bees-made-it.mp4 <- V2A-seed30313-w3.mp4
keep    12_V3Q_verse-3-question-everyone-little-fish-in-your-ba.mp4
staged  13_V3A_verse-3-answer-i-caught-them-in-the-river-splash.mp4 <- V3A-seed30313-w3.mp4
keep    14_V4Q_verse-4-question-the-rabbit-and-the-squirrel-blu.mp4
staged  15_V4A_verse-4-answer-i-picked-them-in-the-forest-every.mp4 <- V4A-seed30313-w3.mp4
keep    16_O1_outro-1-karadi-mama-shares-his-blueberries.mp4
keep    17_O2_outro-2-everyone-s-bear-walk-with-karadi-mama.mp4
keep    18_O3_outro-3-spin-skip-wave-and-home-to-the-forest.mp4
```

## Step 4 — ROUGH2 cuts
`py comfy\song_cuts.py songs\a12-karadi-w3 cut --lang both --tag ROUGH2` → exit 0, no error. Final lines, verbatim:
```
plan: 4644 frames (154.800 s)
wrote C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\A12-KARADI-MAMA-ROUGH2-TA.mp4 4644 video frames = plan 4644; container 154.800 s (audio 154.800 s)
plan: 3840 frames (128.000 s)
wrote C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\A12-KARADI-MAMA-ROUGH2-EN.mp4 3840 video frames = plan 3840; container 128.000 s (audio 128.000 s)
```

| Cut | Path (in `<song folder>\_cuts\`) | Frames (`ffprobe -count_frames`) | Size | Duration | Bytes |
|---|---|---|---|---|---|
| Tamil | `A12-KARADI-MAMA-ROUGH2-TA.mp4` | **4644** = plan | 1920×1080, 30 fps | 154.800 s | 173,671,697 |
| English | `A12-KARADI-MAMA-ROUGH2-EN.mp4` | **3840** = plan | 1920×1080, 30 fps | 128.000 s | 142,299,564 |

**"holds last frame" lines: none.**

**The first ROUGH cuts are unchanged:** the MD5 of `A12-KARADI-MAMA-ROUGH-TA.mp4` and `…-ROUGH-EN.mp4` was taken before the cut step
and again after — identical. Their sheets and cutlogs are untouched.

Note on `_graph-ta.txt` / `_graph-en.txt`: `song_cuts.py` rewrites these two scratch files on every cut (same names, whatever the
tag). So that nothing from the first cut was lost, CC copied them to `_graph-ta-ROUGH.txt` / `_graph-en-ROUGH.txt` before running
the ROUGH2 cut. `song_cuts.py` also wrote `A12-KARADI-MAMA-ROUGH2-TA.cutlog.txt` and `…-ROUGH2-EN.cutlog.txt`.

## Step 5 — contact sheets (in `<song folder>\_cuts\`, same format as the ROUGH sheets)
- `A12-ROUGH2-TA-sheet.jpg` — 2400×1080: 10 columns × 8 rows.
- `A12-ROUGH2-EN-sheet.jpg` — 2400×810: 10 columns × 6 rows.

One frame every 2.2 s, 240 px wide, timestamp burned in. Written with ffmpeg `-n` (cannot overwrite).

## What was written where
- Song folder: four new staged clips, `_superseded-2026-10-13\` (the four old staged clips), and in `_cuts\` the two ROUGH2 cuts,
  their cutlogs, the two ROUGH2 sheets and the two `_graph-*-ROUGH.txt` copies. WAVs/MP3s, `refs\`, `_gen\` and the runsheet files
  untouched.
- Repo: nothing edited by hand; `shots.csv` status cells are the runner's own updates (all 18 `done`).

## Step 6 — commit
`[skip ci]`, explicit paths: `songs/a12-karadi-w3/batch_restage1.log`, `songs/a12-karadi-w3/shots.csv`, the four rev 1.5 prompt
files (`shots/09_V1A`, `11_V2A`, `13_V3A`, `15_V4A` `.raw.txt`), `queue/2026-10-13-karadi-restage1`, `queue/A12-WATCH.md`,
`queue/A12-WATCH-LOG.md`. The hash is in this folder's `LOG.md` done line and `item-02.done` (this report is inside that commit;
the markers follow in a small `[skip ci]` commit).

## Spend
This item $0.00. Queue total **$2.40 list**. A12: **$15.40 list** (conservative) of the $17.00 cap written in `A12-WATCH.md`.
