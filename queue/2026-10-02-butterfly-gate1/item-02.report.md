# item-02 report — stand-in cut test of the re-use map ($0, local ffmpeg)

- **Before:** md5 of the 11 files directly in `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`: BUTTERFLY-WAN3-RUNSHEET.md,
  BUTTERFLY-YOUTUBE.html, RENDER-HANDOFF.md, STRUCTURE-CHECK-EN.mp3, STRUCTURE-CHECK-TA.mp3, butterfly (1).mp3, butterfly (1).wav,
  butterfly english (1).mp3, butterfly english (1).wav, butterfly-shots.json, lyrics.md.
- `python tests\test_song_cuts_reuse.py` → exit 0, **17:04:36 → 17:05:30 UTC**. The log is
  `C:\Projects\opencode\video_image\songs\a07-butterfly\cuts_standin.log`. **Last line:**
  `PASS: rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit, both stand-in cuts frame-exact`
- **`wrote … video frames = plan …` lines:** only one is in the log:
  `wrote C:\Users\arulp\AppData\Local\Temp\tmp0n9brx8x\cuts\A07-BUTTERFLY-ROUGH-EN-PREVIEW.mp4 6665 video frames = plan 6665; container 222.167 s (audio 222.160 s)`
  - The **Tamil line is not in the log**, because the test prints only the last 1500 characters of `song_cuts.py`'s stdout
    (`print(r.stdout[-1500:])`), and the TA line scrolled out of that window.
  - The test still **asserts** `r.stdout.count("video frames = plan") == 2` (both lines present in the full stdout), that no clip
    holds a last frame, and exit 0, all before printing PASS. `song_cuts.py` itself fails loudly on any frame-count mismatch.
    So both stand-in cuts were frame-exact; only the TA line's text was not captured.
  - Suggestion for Fable: print the `wrote` lines in full (e.g. `grep`-style filtering instead of the 1500-char tail).
- The temp folder `...\Temp\tmp0n9brx8x\` (33 test-pattern clips + two 480×270 preview cuts) no longer exists after the test.
- **After:** md5 of the same folder → **unchanged: yes**. 11 files before and after, 0 new, 0 changed.
- `songs\rowboat\` was not touched (the 304 rowboat render files' md5 are unchanged; the test only read its cutplan).
