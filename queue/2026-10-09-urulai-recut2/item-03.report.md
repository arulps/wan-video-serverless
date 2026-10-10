# item-03 — 4K master finished and checked. Both 4K cuts pass. $0.00.

The video was not judged.

## The run
- Window started 21:59:18; upscale 21:59:21 → 22:45:40 (about 46 min): 17 clips, 3,955 frames, `ALL DONE: 17 clips`.
  The log's final average is 0.70 s/frame (the first clips ran at about 0.45 s/frame, later ones slower).
- 4K cuts: TA written 22:49, EN written 22:52. **Total about 53 minutes** from start to the second cut.
- No error lines in `songs\l05-urulai-w3\upscale_4k.log`; the PowerShell window did not need to be looked at.
- Progress checks (one line each in `LOG.md`): 22:01 0/17 · 22:06 3/17 · 22:11 4/17 · 22:16 6/17 · 22:21 7/17 · 22:26 9/17 ·
  22:30 10/17 · 22:35 12/17 · 22:40 15/17 · 22:45 17/17 (TA cut appearing) · 22:50 both files present (EN still writing) ·
  22:55 both `wrote` lines in the log.

## The two 4K cuts — song folder `_cuts\` (ffprobe `-count_frames`)

| File | Video frames | Video | Audio | Size |
|---|---|---|---|---|
| `L05-URULAIKIZHANGU-V1-4K-TA.mp4` | **4448** (target 4448) | h264 3840×2160, 30 fps, 148.267 s | 1 × AAC, 148.261 s | 451,827,813 bytes (452 MB) |
| `L05-URULAIKIZHANGU-V1-4K-EN.mp4` | **4452** (target 4452) | h264 3840×2160, 30 fps, 148.400 s | 1 × AAC, 148.400 s | 452,817,577 bytes (453 MB) |

Log lines, verbatim:
```
plan: 4448 frames (148.267 s)
wrote C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\_cuts\L05-URULAIKIZHANGU-V1-4K-TA.mp4 4448 video frames = plan 4448; container 148.267 s (audio 148.261 s)
plan: 4452 frames (148.400 s)
wrote C:\Channel Contents\MinMiniKids\songs\L05-Urulaikizhangu chellakutti\_cuts\L05-URULAIKIZHANGU-V1-4K-EN.mp4 4452 video frames = plan 4452; container 148.400 s (audio 148.400 s)
```
"holds last frame" lines: none, in the log or in the two `V1-4K` `.cutlog.txt` files.

## Upscaled takes — `songs\l05-urulai-w3\out_4k\`
17 `.mp4` + 17 `.json` sidecars, all 3840×2160 at 30 fps. The I1 take is the splice (`I1-seed30313-w3-splice.mp4`).
ZO is the current third take.

## Existing files
- Nothing was renamed, moved or deleted. `ROUGH` and `ROUGH2` cuts, cut logs and sheets are untouched.
- As noted in item-01, the 4K cut step rewrote `song_cuts.py`'s own scratch files `_cuts\_graph-ta.txt` and `_graph-en.txt`
  (now dated 22:45 and 22:49).

## Repo
- `.gitignore`: added `songs/*/out_4k/` (it was not there), with a one-line comment. `out_4k\` is no longer listed as
  untracked for any song.
- Commit: `queue/2026-10-09-urulai-recut2`, `queue/L05-WATCH-LOG.md`, plus the two repo changes this queue made —
  `songs/l05-urulai-w3/cutplan.json` (rev 2, item-01) and the `.gitignore` line. See the last line of `LOG.md` for the hash.
- Left untracked because no item lists them: `queue\2026-10-09-urulai-recut1\` (the blocked queue's records),
  `queue\2026-10-09-urulai-cuts\FABLE-VERDICT.md`, and `songs\l05-urulai-w3\upscale_4k.log`.
