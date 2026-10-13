# Fable — scale-rule blocked (13 Oct 10:22) → doc regenerated, re-issued as `queue\2026-10-13-karadi-0-scale-rule`

Cause: `docs/CHARACTER-SCALE.md` is generated from every `songs\*\scale.json`; `songs\a12-karadi-w3\scale.json` (written 13 Oct for
Karadi Mama) is newer than this queue, so the generated table gained an `a12-karadi-w3` section the doc lacked. CC stopped correctly
($0.00, nothing committed). Fix: Fable regenerated the doc (diff = exactly that section; without it the generator reproduces the old doc
byte for byte) and re-issued the queue, which also commits `songs/a12-karadi-w3/scale.json`. This folder is kept as the record (the new
queue commits it); do not re-run it.
