# item-02 — review sheets, copies, report, commit ($0, ffmpeg stills only, no upscale)

In `songs\shorts-loops\out\`, for each rendered clip — `L03_w3b-seed4242-w3.mp4`, `L04_w3b-seed30313-w3.mp4`,
`L10_w3b-seed30313-w3.mp4` (use the actual file names the runner wrote):
```
ffmpeg -y -i <clip>.mp4 -vf "select='not(mod(n\,15))',scale=216:-2,tile=5x2" -vsync 0 -frames:v 1 _qc\<id>-contact.png
ffmpeg -y -stream_loop 2 -i <clip>.mp4 -c copy _qc\<id>-loop-x3.mp4
```
Copy the clip, `_qc\<id>-contact.png` and `_qc\<id>-loop-x3.mp4` to `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L03\`,
`...\renders\L04\` and `...\renders\L10\` respectively (next to the first-batch files; overwrite nothing else).

Seam number for Fable (read-only check, no judging): for each clip, mean absolute difference between the first and the last
frame on 0–255, e.g.
```
python -c "import cv2,sys,numpy as n;c=cv2.VideoCapture(sys.argv[1]);ok,a=c.read();b=a
while True:
  ok,f=c.read()
  if not ok: break
  b=f
print(round(float(n.abs(a.astype(int)-b.astype(int)).mean()),1))" <clip>.mp4
```
(any equivalent method is fine; say which one you used).

Write `CC-REPORT-shorts-retakes1.md` (repo root): the item-01 table, the 3 seam numbers, full Windows paths of every copy.
Commit `songs/shorts-loops/shots.csv` (status cells), `songs/shorts-loops/shots/L03-w3b.txt`, `L04-w3b.txt`, `L10-w3b.txt`,
`songs/shorts-loops/world-garden-rain.txt`, `queue/2026-09-28-shorts-retakes1` and the report, with `[skip ci]`; push.
**Do not judge the clips** — Fable reviews.

Housekeeping: delete `queue\_retakes1-combined.tmp` (Fable's scratch copy; never commit it).
