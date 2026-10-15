# item-02 report — DONE: ROUGH3 TA + EN cut from `out\` (frames = plan, no held frames), four sheets — $0

Run by CC (A12 watcher), 2026-10-14 22:52–23:05 Toronto. No API call. `song_cuts.py stage` was **not** run; the cut used `--src out`.
The cut was not judged.

## Step 1 — cut plan
```
wrote songs\a12-karadi-w3\cutplan.json: TA 29 slots 154.800 s, EN 24 slots 128.000 s, 21 clips — all slots fit their clips, no gaps
```
The `take` of all 4 CAa entries in `cutplan.json`: **`CAa-seed30313-w3-splice.mp4`**. OK.

## Step 2 — the cuts
`py comfy\song_cuts.py songs\a12-karadi-w3 cut --lang both --src out --tag ROUGH3` → exit 0. No ROUGH3 file existed before (nothing overwritten;
ROUGH and ROUGH2 untouched).
```
plan: 4644 frames (154.800 s)
wrote C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\A12-KARADI-MAMA-ROUGH3-TA.mp4 4644 video frames = plan 4644; container 154.800 s (audio 154.800 s)
plan: 3840 frames (128.000 s)
wrote C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\A12-KARADI-MAMA-ROUGH3-EN.mp4 3840 video frames = plan 3840; container 128.000 s (audio 128.000 s)
```
**"holds last frame" lines: none** in either cutlog (`A12-KARADI-MAMA-ROUGH3-TA.cutlog.txt` 0, `…-EN.cutlog.txt` 0).

| cut | frames (ffprobe `-count_frames`) | duration | size |
|---|---|---|---|
| `_cuts\A12-KARADI-MAMA-ROUGH3-TA.mp4` | 4644 | 154.800 s, 1920×1080, 30 fps | 186,633,482 bytes |
| `_cuts\A12-KARADI-MAMA-ROUGH3-EN.mp4` | 3840 | 128.000 s, 1920×1080, 30 fps | 153,389,709 bytes |

Cutlogs beside them: `A12-KARADI-MAMA-ROUGH3-TA.cutlog.txt` (2,082 bytes), `…-EN.cutlog.txt` (1,719 bytes).

## Step 3 — sheets (all in `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\`, ffmpeg `-n`)
| sheet | form | size |
|---|---|---|
| `A12-ROUGH3-TA-sheet.jpg` | 71 frames, one every 2.2 s, 240 wide, timestamp burned in, 10 columns × 8 rows (2400×1088) | 831,707 bytes |
| `A12-ROUGH3-EN-sheet.jpg` | 59 frames, same form, 10 × 6 (2400×816) | 675,140 bytes |
| `A12-ROUGH3-TA-slots.jpg` | 29 rows, one per slot: first / middle / last played frame, 240 wide, slot number + clip ID at the left (920×3944) | 1,373,376 bytes |
| `A12-ROUGH3-EN-slots.jpg` | 24 rows, same form (920×3264) | 1,126,013 bytes |

The 2.2 s sheets use the same form as the ROUGH2 sheets (ffmpeg `fps=1/2.2`, `drawtext` timestamp, `tile=10xN`); rows are 136 px high
(ROUGH2: 135) because the scaler rounds to an even height.

The slot frames come from the cutlog's per-slot frame counts summed in order (TA sum 4644, EN sum 3840 = the cuts' frame counts,
checked). **The first tile of slot 01 and the last tile of the final slot (TA 29, EN 24 = O3) are black.** That is the cut's own
fade-in at frame 0 and fade-out at the last frame (`song_cuts.py` applies `fade=t=in` / `fade=t=out`, line 139), not a missing frame.

## Step 4 — commit
Message `Karadi rev 2.8 batch: 10 clips rendered, ROUGH3 TA + EN cuts and sheets [skip ci]`, explicit paths:
`songs/a12-karadi-w3/shots.csv`, `songs/a12-karadi-w3/shots/10_CAb.raw.txt`, `songs/a12-karadi-w3/cutplan.json`,
`songs/a12-karadi-w3/batch_main.log` (the only changes under `songs/a12-karadi-w3/` outside `out/`),
`queue/2026-10-14-karadi-rev27b-gateB2` (its FABLE-VERDICT.md plus CC's done marker, LOG lines and report time fix),
`queue/2026-10-14-karadi-rev28-batch`, `queue/A12-WATCH-LOG.md`. The hash is in this folder's `LOG.md` and `item-02.done`
(this report is inside that commit).

## Spend
$0 in this item. Queue total $6.20 list (item-01). A12: $22.70 + $6.20 = **$28.90 list** of the $29.50 cap ($0.60 left).
