# item-01 — install the retry-safe client, test it, recover O1 by task id ($0.00)

1. **Client patch is in place** (Fable wrote the files; verify, don't edit): `comfy\wan3_api.py` contains `def fetch(` and
   `RETRY_BACKOFF_S`; `tests\test_wan3_retry_mock.py` exists. `py -m py_compile comfy\wan3_api.py` → no output.
2. Tests: `py tests\test_wan3_retry_mock.py` → last line `PASS test_wan3_retry_mock: 9 checks`; `py tests\test_wan3_mock.py` → PASS
   (the existing mock; if it fails because it stubs `_call` or `urlopen` with an old signature, paste the traceback and **block** —
   Fable adapts the test, nothing is rendered).
3. **Find O1's task id** in `songs\a12-karadi-w3\batch_gateA.log`: the line `  wan3 submitted task <id>` for the O1 row (there is
   exactly one; HKa never got one). Report the id.
4. **Recover O1 (no new charge):**
   ```
   py comfy\wan3_api.py fetch <id> songs\a12-karadi-w3\out\O1-seed30313-w3.mp4 --timeout-min 10
   ```
   - On `fetched task … bytes` → check `ffprobe -count_frames` (expect 210 frames, 7.0 s, 1280×720), write the QC strip the runner
     would have written (`out\_qc\O1-strip.png`, same tool as before), set the `O1` row's `status` to `done` in `shots.csv`
     (that cell only), and report **"O1 recovered, $0"**.
   - If the task is reported `FAILED`, `CANCELED`, `UNKNOWN`, not found, or the fetch itself fails after its retries → report the
     message verbatim and **"O1 not recoverable — item-02 renders it"**. Do not render anything in this item.
5. Commit with `[skip ci]` and push: `comfy/wan3_api.py`, `tests/test_wan3_retry_mock.py`, `queue/2026-10-13-karadi-rev22-gateA`
   (its blocked record), `queue/2026-10-13-karadi-rev23-gateA2`, `queue/A12-WATCH-LOG.md`, and `songs/a12-karadi-w3/shots.csv` if
   step 4 changed it. Message: `wan3_api: retry polls/downloads on dropped connections, one connection-level submit retry, fetch by task id; A12 gate A re-issue [skip ci]`

**item-01.report.md:** steps 1–2 output lines, the task id, the fetch output verbatim, the ffprobe line and strip path if recovered,
the commit hash.
