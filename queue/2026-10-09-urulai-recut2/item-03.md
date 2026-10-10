# item-03 — wait for the 4K job and check it ($0.00)

1. Every 5 minutes, for up to 120 minutes, check:
   - `songs\l05-urulai-w3\upscale_4k.log`;
   - the song folder's `_cuts\` for `L05-URULAIKIZHANGU-V1-4K-TA.mp4` and `L05-URULAIKIZHANGU-V1-4K-EN.mp4`.

   Append one progress line per check to `LOG.md` (clips done / total from the log). Learnings §11: if the log says "ALL DONE" but no
   4K file shows up within ~5 minutes, look at the job's PowerShell window — the cut error appears there, not in the log.
2. When both files exist, check that:
   - each is 3840×2160;
   - the video frame counts are TA 4448 and EN 4452;
   - the audio is present.

   Report sizes, frame counts and the log's total time. A mismatch, an error, or no files after 120 min → **blocked**, with what
   the window or log shows.
3. Commit with `[skip ci]` and push: `queue/2026-10-09-urulai-recut2` and `queue/L05-WATCH-LOG.md`. Never commit `out_4k/`; add
   `songs/*/out_4k/` to `.gitignore` if it isn't already there.

   **Do not judge the video.**
