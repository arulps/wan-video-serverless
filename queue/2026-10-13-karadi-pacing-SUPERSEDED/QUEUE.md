# CC QUEUE — 2026-10-13 "Karadi pacing": measure the pacing of 5 reference Karadi Mama videos vs our ROUGH2 (no API spend)

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

Arul (13 Oct) wants our A12 cut compared with five current Karadi Mama videos on **pacing**: how fast shots change, how fast and how
big the dance movements are. Fable wrote `_gen\pacing_probe.py` in the song folder and ran it on our ROUGH2-TA in the cloud workspace
(it found all 28 cuts of the 29-slot plan exactly). The cloud workspace cannot reach YouTube, so the reference videos are fetched
and measured here. **API spend: $0.00** — yt-dlp download + local ffmpeg/OpenCV only. Arul approved the download in chat.

## Hard limits
- No API calls, no renders, no pod. Never print `.env` values, keys, the workspace id or any video URL other than the five
  YouTube links in item-01.
- The five reference videos are **for measurement only**: keep them in `C:\Channel Contents\MinMiniKids\research\karadi-refs\`;
  never copy them into a song folder, the repo or any render input, and never commit them.
- In the song folder `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\` write **only** `_research\pacing\`. Never touch the
  WAVs, `refs\`, `_cuts\`, `_gen\` or the runsheet files.
- Repo: commit only this queue folder and `queue/A12-WATCH-LOG.md`, with `[skip ci]`. Move, never delete.

## Protocol (markers in `queue\2026-10-13-karadi-pacing\`)
As before: `LOG.md` start/done lines, `item-N.report.md`, `item-N.done`, or `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $0.00`, tell Arul "Karadi pacing probe done — Fable will review queue\2026-10-13-karadi-pacing".
