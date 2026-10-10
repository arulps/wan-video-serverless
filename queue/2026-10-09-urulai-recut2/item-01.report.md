# item-01 — cutplan rev 2 written; ROUGH2 TA and EN cuts built. $0.00. No errors, no held frames, nothing renamed.

The cuts were not judged.

## Step 1 — cutplan rev 2
`py "C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\_gen\make_cutplan.py" songs\l05-urulai-w3` → exit 0, output:
```
wrote songs\l05-urulai-w3\cutplan.json: 33 slots, 17 clips, TA 148.261 s, EN 148.400 s — all slots fit their clips, no gaps
```
(The dash printed as a replacement character in the Windows console; the text is otherwise exactly this line.)
I1 slot in `cutplan.json`: slot `INTRO-01`, `"take": "I1-seed30313-w3-splice.mp4"`, `gen` 9.83. It is the only splice take.
git diff of `cutplan.json`: 2 lines changed (the I1 slot's `gen` and `take`).

## Step 2 — ROUGH2 cuts
`py comfy\song_cuts.py songs\l05-urulai-w3 cut --lang both --src out --tag ROUGH2` → exit 0. Full output:
```
01 INTRO-01=I1 in    0.000 use  9.300 slip 0.000 frames  279 hard-cut
02 CH1-02=SA in    9.288 use  4.333 slip 0.000 frames  130 hard-cut
04 CH1-03=ZK1 in   13.630 use  4.367 slip 0.400 frames  131 hard-cut
04 V1-04=ZK1 in   17.995 use  4.367 slip 4.765 frames  131 hard-cut
15 V1-05=CA in   22.361 use  4.367 slip 0.000 frames  131 hard-cut
03 CH2-06=SB in   26.726 use  4.333 slip 0.000 frames  130 hard-cut
05 CH2-07=ZK2 in   31.068 use  4.367 slip 0.400 frames  131 hard-cut
05 V2-08=ZK2 in   35.434 use  4.333 slip 4.766 frames  130 hard-cut
16 V2-09=CB in   39.776 use  4.367 slip 0.000 frames  131 hard-cut
02 CH3-10=SA in   44.118 use  4.333 slip 1.600 frames  130 hard-cut
06 CH3-11=Z3 in   48.460 use  4.333 slip 0.600 frames  130 hard-cut
11 V3-12=K3 in   52.802 use  4.367 slip 0.000 frames  131 hard-cut
15 V3-13=CA in   57.168 use  4.333 slip 0.800 frames  130 hard-cut
03 CH4-14=SB in   61.510 use  4.300 slip 1.600 frames  129 hard-cut
07 CH4-15=ZK4 in   65.805 use  4.333 slip 0.400 frames  130 hard-cut
07 V4-16=ZK4 in   70.147 use  4.367 slip 4.742 frames  131 hard-cut
16 V4-17=CB in   74.513 use  4.367 slip 0.800 frames  131 hard-cut
02 CH5-18=SA in   78.855 use  4.333 slip 0.800 frames  130 hard-cut
08 CH5-19=Z5 in   83.197 use  4.333 slip 0.000 frames  130 hard-cut
12 V5-20=K5 in   87.539 use  4.333 slip 1.200 frames  130 hard-cut
15 V5-21=CA in   91.858 use  4.300 slip 1.600 frames  129 hard-cut
03 CH6-22=SB in   96.177 use  4.367 slip 0.800 frames  131 hard-cut
09 CH6-23=Z6 in  100.519 use  4.333 slip 1.200 frames  130 hard-cut
13 V6-24=K6 in  104.861 use  4.300 slip 0.000 frames  129 hard-cut
16 V6-25=CB in  109.180 use  4.333 slip 1.600 frames  130 hard-cut
02 CH7-26=SA in  113.499 use  4.333 slip 2.400 frames  130 hard-cut
10 CH7-27=ZK7 in  117.818 use  4.300 slip 0.400 frames  129 hard-cut
10 V7-28=ZK7 in  122.137 use  4.333 slip 4.719 frames  130 hard-cut
15 V7-29=CA in  126.456 use  4.300 slip 0.400 frames  129 hard-cut
03 CH8-30=SB in  130.775 use  4.300 slip 2.400 frames  129 hard-cut
14 CH8-31=ZO in  135.070 use  4.333 slip 0.400 frames  130 hard-cut
14 OUTRO-32=ZO in  139.413 use  4.600 slip 4.743 frames  138 hard-cut
17 OUTRO-33=O2 in  144.013 use  4.267 slip 1.200 frames  128
plan: 4448 frames (148.267 s)
wrote C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\_cuts\L05-URULAIKIZHANGU-ROUGH2-TA.mp4 4448 video frames = plan 4448; container 148.267 s (audio 148.261 s)
01 INTRO-01=I1 in    0.000 use  9.700 slip 0.000 frames  291 hard-cut
02 CH1-02=SA in    9.685 use  4.333 slip 0.000 frames  130 hard-cut
04 CH1-03=ZK1 in   14.027 use  4.367 slip 0.400 frames  131 hard-cut
04 V1-04=ZK1 in   18.392 use  4.300 slip 4.765 frames  129 hard-cut
15 V1-05=CA in   22.688 use  4.433 slip 0.000 frames  133 hard-cut
03 CH2-06=SB in   27.123 use  4.333 slip 0.000 frames  130 hard-cut
05 CH2-07=ZK2 in   31.465 use  4.333 slip 0.400 frames  130 hard-cut
05 V2-08=ZK2 in   35.807 use  4.267 slip 4.742 frames  128 hard-cut
16 V2-09=CB in   40.080 use  4.433 slip 0.000 frames  133 hard-cut
02 CH3-10=SA in   44.492 use  4.333 slip 1.600 frames  130 hard-cut
06 CH3-11=Z3 in   48.834 use  4.333 slip 0.600 frames  130 hard-cut
11 V3-12=K3 in   53.153 use  4.267 slip 0.000 frames  128 hard-cut
15 V3-13=CA in   57.448 use  4.400 slip 0.800 frames  132 hard-cut
03 CH4-14=SB in   61.837 use  4.333 slip 1.600 frames  130 hard-cut
07 CH4-15=ZK4 in   66.156 use  4.300 slip 0.400 frames  129 hard-cut
07 V4-16=ZK4 in   70.475 use  4.267 slip 4.719 frames  128 hard-cut
16 V4-17=CB in   74.724 use  4.367 slip 0.800 frames  131 hard-cut
02 CH5-18=SA in   79.113 use  4.300 slip 0.800 frames  129 hard-cut
08 CH5-19=Z5 in   83.408 use  4.333 slip 0.000 frames  130 hard-cut
12 V5-20=K5 in   87.727 use  4.233 slip 1.200 frames  127 hard-cut
15 V5-21=CA in   91.953 use  4.367 slip 1.600 frames  131 hard-cut
03 CH6-22=SB in   96.342 use  4.333 slip 0.800 frames  130 hard-cut
09 CH6-23=Z6 in  100.661 use  4.233 slip 1.200 frames  127 hard-cut
13 V6-24=K6 in  104.910 use  4.300 slip 0.000 frames  129 hard-cut
16 V6-25=CB in  109.206 use  4.367 slip 1.600 frames  131 hard-cut
02 CH7-26=SA in  113.571 use  4.267 slip 2.400 frames  128 hard-cut
10 CH7-27=ZK7 in  117.843 use  4.300 slip 0.400 frames  129 hard-cut
10 V7-28=ZK7 in  122.139 use  4.233 slip 4.696 frames  127 hard-cut
15 V7-29=CA in  126.365 use  4.400 slip 0.400 frames  132 hard-cut
03 CH8-30=SB in  130.754 use  4.267 slip 2.400 frames  128 hard-cut
14 CH8-31=ZO in  135.026 use  4.533 slip 0.400 frames  136 hard-cut
14 OUTRO-32=ZO in  139.552 use  4.600 slip 4.926 frames  138 hard-cut
17 OUTRO-33=O2 in  144.152 use  4.233 slip 1.200 frames  127
plan: 4452 frames (148.400 s)
wrote C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\_cuts\L05-URULAIKIZHANGU-ROUGH2-EN.mp4 4452 video frames = plan 4452; container 148.400 s (audio 148.400 s)
```

| Cut (in the song folder's `_cuts\`) | Video frames | Video | Audio | Size |
|---|---|---|---|---|
| `L05-URULAIKIZHANGU-ROUGH2-TA.mp4` | **4448** = plan 4448 | h264 1920×1080, 30 fps, 148.267 s | 1 × AAC | 134,930,380 bytes (135 MB) |
| `L05-URULAIKIZHANGU-ROUGH2-EN.mp4` | **4452** = plan 4452 | h264 1920×1080, 30 fps, 148.400 s | 1 × AAC | 135,001,209 bytes (135 MB) |

Frame counts confirmed separately with ffprobe `-count_frames`.
**"holds last frame" lines: none** — 0 in the output above and 0 in both `ROUGH2` `.cutlog.txt` files.

## Step 3 — contact sheets (song folder `_cuts\`)
- `L05-ROUGH2-TA-sheet.jpg` — 68 frames (every 2.2 s), 10 columns × 7 rows, 240 wide each (2400×952), timestamp burned in
- `L05-ROUGH2-EN-sheet.jpg` — the same layout, 68 frames

## Existing files
- The six `ROUGH` files from the first cut (two mp4, two cut logs, two sheets) are untouched (still dated 18:05–18:09).
- Nothing was staged, renamed, moved or deleted. The staged `01_I1_…mp4` in the song folder is still the old (pre-splice) I1.
- **One thing that was overwritten:** `song_cuts.py` always writes its working files `_cuts\_graph-ta.txt` and
  `_cuts\_graph-en.txt`, so the cut step replaced the 18:05 copies with new ones (21:55). They are the tool's scratch files
  (the ffmpeg filter graph of the last cut), not deliverables, but they are existing files that changed. The 4K cut in item-02
  will replace them again.
- Repo: only `songs\l05-urulai-w3\cutplan.json` changed.
