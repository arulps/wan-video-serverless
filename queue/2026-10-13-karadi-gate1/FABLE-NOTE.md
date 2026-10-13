# Fable — gate1 blocked (13 Oct ~13:05) → re-issued as `queue\2026-10-13-karadi-gate1b`

Cause (Fable's error): the A12 builder wrote the cast keys `the-rabbit` / `the-squirrel` into `shots.csv` and `characters.txt`, but
`comfy\batch_runner.py` only accepts lock-line keys matching `^[A-Z][A-Za-z0-9_-]*:` (LOCK_NAME_RE), so CQa could not assemble. Lint
passed because it reads `ref_labels`, not `cast`. CC stopped correctly at the dry-run ($0) and its diagnosis was right.
Fix: builder rev 1.3 writes `Rabbit` / `Squirrel` and asserts every cast key against the runner's pattern; prompts are byte-identical.
Fable now runs the runner's own `--dry-run` (all rows) on a mirror before writing any render queue. Do not re-run this folder.
