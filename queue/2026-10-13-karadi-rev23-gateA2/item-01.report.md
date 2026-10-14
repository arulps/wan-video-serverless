# item-01 report — DONE: retry-safe client verified, **O1 recovered, $0**

Run by CC (A12 watcher), 2026-10-13 23:36–23:42 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
Nothing was rendered in this item. The clip was not judged.

## Step 1 — client patch in place
- `comfy\wan3_api.py` contains `def fetch(` (1 match) and `RETRY_BACKOFF_S` (7 matches).
- `tests\test_wan3_retry_mock.py` exists (4,506 bytes).
- `py -m py_compile comfy\wan3_api.py` → no output, exit 0.

## Step 2 — tests
- `py tests\test_wan3_retry_mock.py` → last line `PASS test_wan3_retry_mock: 9 checks`
- `py tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`

## Step 3 — O1's task id
From `songs\a12-karadi-w3\batch_gateA.log`, line 4 (the only `submitted task` line): **`6d24e073-4519-4515-801e-31a553879f70`**.

## Step 4 — recovery
`py comfy\wan3_api.py fetch 6d24e073-4519-4515-801e-31a553879f70 songs\a12-karadi-w3\out\O1-seed30313-w3.mp4 --timeout-min 10`
→ exit 0. Output, verbatim (no URL was printed):
```
  wan3 task 6d24e073-4519-4515-801e-31a553879f70: SUCCEEDED
fetched task 6d24e073-4519-4515-801e-31a553879f70 -> songs/a12-karadi-w3/out/O1-seed30313-w3.mp4 (9782104 bytes, usage {'duration': 7.0, 'input_video_duration': 0.0, 'output_video_duration': 7.0, 'fps': 30, 'video_count': 1, 'SR': 720, 'ratio': '16:9'})
```
- No file existed at that path before the fetch, so nothing was overwritten. The fetch also wrote the sidecar
  `out\O1-seed30313-w3.json` (482 bytes; checked: no URL in it).
- `ffprobe -count_frames` → `1280,720,30/1,7.000000,210` — **210 frames, 7.000 s, 1280×720, 30 fps**, as expected. 9,782,104 bytes.
- QC strip: `songs\a12-karadi-w3\out\_qc\O1-strip.png` (6400×720), written with the runner's own `write_qc_strip`.
- `shots.csv`: the `O1` row's `status` set to `done` with the runner's own `read_shots` / `set_status`, that cell only.
  **It was `failed`, not `todo`** (the runner marked it when gate A's connection dropped).

**O1 recovered, $0** (no new charge; the task itself was submitted in gate A, so its $0.70 is real spend — see below).

## For Fable
1. **HKa's status is `failed`, not `todo`.** The gate A runner set both rows to `failed`. Item-02 step 1 requires HKa `todo` and says
   any mismatch → blocked, and this queue allows CC to edit only O1's cell. See item-02's report.
2. **The submit retry is not quite "never paid twice".** `_call` retries a POST once on any connection-level error. A connection
   that drops *after* the service has read the whole request but *before* its answer arrives looks the same from here as one that
   drops during the upload, so in that one case the retry would submit a second paid task. It is bounded (one retry, one clip), and
   whether it is worth guarding against is Fable's call — CC changed nothing.
3. Spend: gate A's O1 task did succeed, so its **$0.70 is spent** (CC's conservative figure was right). A12 = **$16.10 list**.

## Step 5 — commit
Message as given. Explicit paths: `comfy/wan3_api.py`, `tests/test_wan3_retry_mock.py`, `queue/2026-10-13-karadi-rev22-gateA`,
`queue/2026-10-13-karadi-rev23-gateA2`, `queue/A12-WATCH-LOG.md`, `songs/a12-karadi-w3/shots.csv`. The hash is in this folder's
`LOG.md` and `item-01.done` (this report is inside that commit). Not in the list and still uncommitted:
`songs/a12-karadi-w3/batch_gateA.log` and `queue/A12-WATCH.md` (the 23:00 edit).
