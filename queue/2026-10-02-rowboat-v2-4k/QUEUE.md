# CC QUEUE — 2026-10-02 "Rowboat V2 + 4K": hard-cut version of both cuts, then the 4K pipeline ($0 API)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.
Arul approved: **V2 = hard cuts on the beat** instead of 0.4 s dissolves wherever a clip has no spare frames (v1 froze the
outgoing clip's last frame for 0.4 s at 22 of 28 joins). Dissolves stay only where real frames exist (intro, and out of the
SFX shots). No mirroring. Then **4K**: every chosen take is upscaled (Real-ESRGAN animevideov3, Vulkan on the laptop GPU)
and both cuts are rebuilt at 3840x2160. The ROUGH (v1) cuts stay untouched for comparison.

Fable changed/added (tested with `--dry`: V2 cutlogs show 0 frozen frames; 4K graph scales to 3840x2160):
- `comfy\song_cuts.py`: `--transitions auto|dissolve` (auto = default), `--tag` (output `<SONG>-<TAG>-<LANG>.mp4`),
  `--height 1080|2160`, `--src out4k` (reads `songs\<slug>\out_4k\`), `--dry`.
- `scripts\upscale_song.py` (new): upscales every cutplan take to `songs\<slug>\out_4k\`, resumable, Vulkan only.
- `scripts\song_4k.ps1` (new): upscale_song + 4K cuts in one resumable command.
- `comfy\prompt_lint.py`: R0 (a song folder without `lint.json` fails) + the "pretend to be / mouse faces" warning.

## Hard limits
- **No API spend at all.** No batch_runner render, no pod, no RunPod.
- Never print, echo or log `.env` values, keys, workspace ids or video URLs. Commits carry `[skip ci]`.
- In `C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat\` write **only** inside `_cuts\`; do not touch the
  existing `*-ROUGH-*` files there.
- Never commit `songs/rowboat/out/` or `songs/rowboat/out_4k/` (video files).

## Protocol (markers in `queue\2026-10-02-rowboat-v2-4k\`)
As before: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time>`, tell Arul "Rowboat V2 cuts ready; 4K smoke test done — see item-02 report for the overnight command".
