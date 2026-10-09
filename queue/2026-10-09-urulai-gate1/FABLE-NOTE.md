# Fable — gate1 blocked (13:28) → fixed and re-queued as `queue\2026-10-09-urulai-gate1b`

Cause: Beast's ffmpeg 9.0.2 rejects `-vsync` in `comfy\batch_runner.py` `write_qc_strip` (line 536), so the mock test's QC strip
assert failed. CC stopped correctly ($0.00 spent). Fix: the option is dropped — with `select+tile` and `-frames:v 1` it never changed
the image (pixel-identical strips on ffmpeg 6.1 with and without it, and on 7.0 without it). `tests\test_wan3_mock.py` PASS on
ffmpeg 6.1 and 7.0 (Fable, 9 Oct 13:50). No other `-vsync` in the repo. This folder is kept as the record; do not re-run it.
