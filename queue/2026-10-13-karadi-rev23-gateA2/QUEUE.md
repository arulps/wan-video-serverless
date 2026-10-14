# CC QUEUE — 2026-10-13 "Karadi rev 2.3 Gate A (re-issue)": recover O1 by task id, retry-safe client, render what is missing

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

`2026-10-13-karadi-rev22-gateA` blocked at the render: two dropped TLS connections (HKa during the upload, before a task id; O1
during a poll after the service had accepted the task). CC was right not to re-run. Fable's fixes, mock-tested (`tests\test_wan3_retry_mock.py`,
9 checks): `comfy\wan3_api.py` now retries polls and downloads on connection-level errors (so a dropped poll never loses a paid task),
retries a submit **once** and only on a connection-level error before any HTTP response (never after the service answered, so a task
is never paid twice), and has `fetch <task_id> <dest.mp4>` to pull a finished task down without paying again.

**Spend: ≤ $1.60 list** (HKa $0.80; O1 $0.70 only if it cannot be recovered). Song cap $29.50 (`A12-WATCH.md`).

## Hard limits
- **API spend ≤ $1.60 at list price. Only `HKa` and, if not recovered in item-01, `O1`.** No pod, no GPU, no upscale. A failure
  is reported, not re-run; the client's own single resubmit is the only retry allowed.
- Never print `.env` values, keys, the workspace id or any URL (a task id is fine — earlier reports carry them). Never touch RunPod.
  Commits carry `[skip ci]`; never commit `.env`, `out/`, `out_4k/`, `tools/`.
- **Move or rename, never delete or overwrite.** Never overwrite a take, a staged clip or a cut.
- Song folder: write only into `_cuts\_gateA\`. Never touch the WAVs, `refs\`, `_gen\`, `_previews\` or the runsheet files.
- Do not edit generated files or the runner — **except**, in item-01 step 4, the `status` cell of the `O1` row in `shots.csv`
  (`todo` → `done`) after a successful recovery, which is what the runner itself would have written.

## Protocol (markers in `queue\2026-10-13-karadi-rev23-gateA2\`)
As before: `LOG.md` start/done lines, `item-N.report.md`, `item-N.done`, or `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>` (x = what was actually submitted in item-02), tell Arul
"Karadi Gate A (re-issue) done — Fable will review queue\2026-10-13-karadi-rev23-gateA2".
