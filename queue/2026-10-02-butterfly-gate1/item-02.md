# item-02 — stand-in cut test of the re-use map ($0, local ffmpeg)

1. md5 of every file directly in `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\` (not subfolders) → before.
2. `python tests\test_song_cuts_reuse.py 2>&1 | tee songs\a07-butterfly\cuts_standin.log` → last line `PASS: ...`.
   (Makes 33 test-pattern clips + two 480x270 preview cuts in a temp folder, deleted afterwards.)
3. md5 again → must equal step 1, with no new files in that folder.
**item-02.report.md:** PASS line; the two `wrote ... video frames = plan ...` lines from the log; md5 unchanged yes/no.
