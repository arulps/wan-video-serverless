# item-01 — fetch 5 reference videos, run the pacing probe on them + our ROUGH2-TA, commit ($0.00)

1. Tools (install only what is missing, user-level):
   ```
   py -m pip install --user -U yt-dlp opencv-python numpy
   ffmpeg -version
   ```
2. Download the five videos, video only, at most 720p, into `C:\Channel Contents\MinMiniKids\research\karadi-refs\`
   (create the folder). One command per link; **no playlists** (the links are bare watch URLs):
   ```
   py -m yt_dlp --no-playlist -f "bv*[height<=720][ext=mp4]/bv*[height<=720]/b[height<=720]" -o "C:\Channel Contents\MinMiniKids\research\karadi-refs\%(id)s.%(ext)s" <URL>
   ```
   | name | URL |
   |---|---|
   | isai-mix | https://www.youtube.com/watch?v=sUnJY8rcSok |
   | chutty-auto | https://www.youtube.com/watch?v=goKSn4_pytQ |
   | liza-trip | https://www.youtube.com/watch?v=M2yLXKqCh00 |
   | papertales | https://www.youtube.com/watch?v=G5Ilt-m-UgU |
   | liza-karadi | https://www.youtube.com/watch?v=bfJYdI1WEVM |

   If one link fails, note it and carry on with the rest; **blocked** only if all five fail.
3. Run the probe once over all of them, with the real downloaded file names (`.mp4` or `.webm`):
   ```
   py "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_gen\pacing_probe.py" "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_research\pacing" ours-ROUGH2-TA="C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\A12-KARADI-MAMA-ROUGH2-TA.mp4" isai-mix="...\karadi-refs\sUnJY8rcSok.mp4" chutty-auto="...\goKSn4_pytQ.mp4" liza-trip="...\M2yLXKqCh00.mp4" papertales="...\G5Ilt-m-UgU.mp4" liza-karadi="...\bfJYdI1WEVM.mp4"
   ```
   (write the full paths; `...` above is only to keep this short). Expect one printed line per video and
   `wrote ...\_research\pacing\PACING-SUMMARY.md`. Any traceback → **blocked**, with it verbatim.
4. Commit with `[skip ci]` and push: `queue/2026-10-13-karadi-pacing`, `queue/A12-WATCH-LOG.md`.

   **Do not judge the results** — Fable reviews the numbers and the strip sheets.

**item-01.report.md** must cover: step outputs verbatim (pip/yt-dlp: last lines only), the downloaded file names and sizes,
`PACING-SUMMARY.md` pasted in full, the list of files in `_research\pacing\`, and the commit hash.
