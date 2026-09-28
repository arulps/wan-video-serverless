# item-02 — review sheets, copies, report, commit ($0, light laptop work: ffmpeg stills only, no upscale)

In `songs\shorts-loops\out\`, for every rendered `Lxx_w3-seed30313-w3.mp4` (xx = 02..20):
```
ffmpeg -y -i Lxx_w3-seed30313-w3.mp4 -vf "select='not(mod(n\,15))',scale=216:-2,tile=5x2" -vsync 0 -frames:v 1 _qc\Lxx_w3-contact.png
ffmpeg -y -stream_loop 2 -i Lxx_w3-seed30313-w3.mp4 -c copy _qc\Lxx_w3-loop-x3.mp4
```
Then copy `Lxx_w3-seed30313-w3.mp4`, `_qc\Lxx_w3-contact.png` and `_qc\Lxx_w3-loop-x3.mp4` to
`C:\Channel Contents\MinMiniKids\YT Shorts\renders\Lxx\` (create the folder per Short).
Also build one overview image of all contact sheets (e.g. `ffmpeg` vstack or PIL) → `_qc\shorts-batch1-overview.png` and copy it to
`C:\Channel Contents\MinMiniKids\YT Shorts\renders\`.

Write `CC-REPORT-shorts-batch1.md` (repo root): the item-01 table + full Windows paths of every copy and the overview.
Commit `songs/shorts-loops` (shots.csv statuses, shots/L*-w3.txt, world-*.txt, characters.txt, refs/amma-front-9x16.png,
refs/thatha-front-9x16.png, refs/paati-front-9x16.png, refs/mintu-front-9x16.png — refs need `git add -f`), `queue/2026-09-28-shorts-batch1`
and the report, with `[skip ci]`; push. **Do not judge the clips** — Fable reviews.
