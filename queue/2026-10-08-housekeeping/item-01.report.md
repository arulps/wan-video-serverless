# item-01 — move `songs\learning-loops\` to the repo's delete folder — DONE

- `git ls-files songs/learning-loops` → printed nothing (untracked, as expected).
- Before: `songs\learning-loops\` = **96 files, 1,890,945 bytes** (1.8 MB; dispatch expected ~100 files, ~3 MB).
- `_to_delete\` did not exist → created; `Move-Item songs\learning-loops _to_delete\learning-loops` (no suffix needed).
- After: `songs\learning-loops` does not exist; `_to_delete\learning-loops\` = **96 files, 1,890,945 bytes** (same).
- `git status --short` after: no `songs/learning-loops/` line, nothing under `_to_delete/`.

## .gitignore diff
```diff
diff --git a/.gitignore b/.gitignore
index 9970030..a9d1921 100644
--- a/.gitignore
+++ b/.gitignore
@@ -16,3 +16,6 @@ nil
 
 # local binaries (Real-ESRGAN etc.) — installed per machine, never committed
 tools/
+
+# Arul's delete folder — reviewed, waiting for him to empty it; never committed
+_to_delete/
```

## git status --short — before
```
 M songs/shorts-learning/REVIEW-learning-batch1-2026-09-29.md
?? SESSION-HANDOFF-2026-10-07-BUTTERFLY-BEAST_1.md
?? queue/2026-10-08-housekeeping/
?? songs/a07-butterfly/out_4k/
?? songs/a07-butterfly/upscale_4k.log
?? songs/learning-loops/
?? songs/rowboat/batch_final.log
?? songs/rowboat/batch_gate.log
?? songs/rowboat/batch_gate2.log
?? songs/rowboat/batch_v5c.log
?? songs/rowboat/batch_w1.log
?? songs/rowboat/batch_w1fix_w2.log
?? songs/rowboat/batch_w2fix_w3w4.log
?? songs/rowboat/cuts_rough1.log
?? songs/rowboat/cuts_rough2.log
?? songs/rowboat/cuts_v2.log
?? songs/rowboat/out_4k/
?? songs/rowboat/upscale_4k_smoke.log
?? songs/shorts-learning/batch_learning1.log
?? songs/shorts-learning/batch_learning2.log
?? songs/shorts-learning/batch_learning3.log
?? songs/shorts-learning/batch_learning4.log
?? songs/shorts-learning/batch_learning5.log
?? songs/shorts-learning/batch_pilot.log
?? songs/shorts-learning/batch_tamil_test.log
?? songs/shorts-loops/REVIEW-shorts-batch1-2026-09-28.md
?? songs/shorts-loops/batch_6f.log
?? songs/shorts-loops/batch_6g.log
?? songs/shorts-loops/batch_retakes1.log
?? songs/shorts-loops/batch_retakes2.log
?? songs/shorts-loops/batch_retakes3.log
?? songs/shorts-loops/batch_shorts1.log
```

## git status --short — after
```
 M .gitignore
 M songs/shorts-learning/REVIEW-learning-batch1-2026-09-29.md
?? SESSION-HANDOFF-2026-10-07-BUTTERFLY-BEAST_1.md
?? queue/2026-10-08-housekeeping/
?? songs/a07-butterfly/out_4k/
?? songs/a07-butterfly/upscale_4k.log
?? songs/rowboat/batch_final.log
?? songs/rowboat/batch_gate.log
?? songs/rowboat/batch_gate2.log
?? songs/rowboat/batch_v5c.log
?? songs/rowboat/batch_w1.log
?? songs/rowboat/batch_w1fix_w2.log
?? songs/rowboat/batch_w2fix_w3w4.log
?? songs/rowboat/cuts_rough1.log
?? songs/rowboat/cuts_rough2.log
?? songs/rowboat/cuts_v2.log
?? songs/rowboat/out_4k/
?? songs/rowboat/upscale_4k_smoke.log
?? songs/shorts-learning/batch_learning1.log
?? songs/shorts-learning/batch_learning2.log
?? songs/shorts-learning/batch_learning3.log
?? songs/shorts-learning/batch_learning4.log
?? songs/shorts-learning/batch_learning5.log
?? songs/shorts-learning/batch_pilot.log
?? songs/shorts-learning/batch_tamil_test.log
?? songs/shorts-loops/REVIEW-shorts-batch1-2026-09-28.md
?? songs/shorts-loops/batch_6f.log
?? songs/shorts-loops/batch_6g.log
?? songs/shorts-loops/batch_retakes1.log
?? songs/shorts-loops/batch_retakes2.log
?? songs/shorts-loops/batch_retakes3.log
?? songs/shorts-loops/batch_shorts1.log
```
