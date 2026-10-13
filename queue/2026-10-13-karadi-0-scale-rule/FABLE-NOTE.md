# Fable — karadi-0 blocked (13 Oct ~12:10) → re-issued as `queue\2026-10-13-karadi-1-scale-rule`

Cause (Fable's error): the regenerated `docs/CHARACTER-SCALE.md` was written with LF line endings, while `scale_line.py --table` writes
CRLF on Windows, and `fc /W` counts that as a difference on every line. Content was identical with CRs stripped (CC's report). CC was
right not to commit on its own reading of a failed check ($0). Fix: the re-issue compares the doc and the generator output inside Python
(text-mode `open()` treats CRLF and LF alike), so neither line endings nor the shell can trip it. This folder is kept as the record; do
not re-run it.
