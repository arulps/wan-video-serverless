# item-05 addendum (Fable, 2026-10-08) — read before doing item-05 step 2

The first run's cut step failed: Beast's ffmpeg 9.0.2 rejects `-filter_complex_script`. Fable fixed
`comfy/song_cuts.py` (picks `-/filter_complex` on ffmpeg 7+) and added version checks to
`tests/test_song_cuts_reuse.py`. Arul ran the test on Beast (PASS) and re-ran `song_4k.ps1`; the log shows:
- `A07-BUTTERFLY-ROUGH3-4K-TA.mp4` 6481 video frames = plan 6481 (216.040 s)
- `A07-BUTTERFLY-ROUGH3-4K-EN.mp4` 6665 video frames = plan 6665 (222.167 s)

For item-05 step 2, in addition to the checks in QUEUE.md:
1. Note in `item-04.report.md` that the first cut attempt failed on the ffmpeg option and was re-run on 8 Oct ~00:44.
2. Run `py tests\test_song_cuts_reuse.py` once more → must print PASS.
3. Commit (with `[skip ci]`) alongside the queue records: `comfy/song_cuts.py`, `tests/test_song_cuts_reuse.py`,
   this addendum. Message: `song_cuts: use -/filter_complex on ffmpeg 7+ (Beast ffmpeg 9); Butterfly 4K verified [skip ci]`.
   Nothing under `tools/`, `out*/`, `_to_delete/`.
