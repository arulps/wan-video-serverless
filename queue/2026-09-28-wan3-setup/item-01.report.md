# item-01 report — preflight, tests, commit ($0)

- **Credentials:** `credentials present: True`; **region line:** `True` (values never printed).
- **L01 keyframe:** `C:\Channel Contents\MinMiniKids\YT Shorts\keyframes\` contains only `L01-KEYFRAME-BRIEF.md` —
  no `L01-start.png/.jpg/.jpeg`. **L01 skipped** (item-02 renders only the three `_ab7` rows).
- **Mock tests:**
  - `tests\test_flf2v_mock.py` → `PASS: 2 rows, distilled + full, loop and explicit last frame, uploads ['L01-start.png', 'L01-start.png', 'L01-end.png']`
  - `tests\test_wan3_mock.py` → **as written it fails on this laptop** (exit 1, last line
    `TypeError: argument of type 'NoneType' is not iterable`). Cause: the test runs the runner as a subprocess with
    `text=True`, Windows decodes its output as cp1252, a UTF-8 byte (0x9d) raises `UnicodeDecodeError` in the reader
    thread, stdout comes back `None`. Not the wan3 logic. Same test with `PYTHONUTF8=1` →
    `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
    **CC's judgment call:** treated as PASS and continued (flagged in 6e's first attempt too). Suggested fix for Fable:
    `encoding="utf-8"` in the test's `subprocess.run`.
- `py_compile` of `wan3_api.py`, `run_comfy.py`, `batch_runner.py`, `upscale_video.py` OK; `bash -n scripts/pod_bootstrap.sh` OK.
- **Dry-runs:** `_ab7`: 3 rows, `estimated $1.50 at list price`, no MISSING. `shorts-loops --only L01_w3`: `estimated $0.50`,
  `KEYFRAME MISSING` (expected, L01 skipped).
- **Commit `aa6ccb8`** `[skip ci]` — the 6e Part B add list + `queue/2026-09-28-wan3-setup`. `scripts/pod_bootstrap.sh` and
  `scripts/upscale_video.py` were already committed unchanged in `754d930` (the "3D queue / 3D-C" commit, which already has
  PULL_SKIP, the flf2v node check and the x3 ncnn scale), so their add was a no-op. No `.env`/`out/`/`outputs/` in the set;
  secret grep only matched variable names and the test's dummy `sk-test`.
- **Push:** `106906b..aa6ccb8` — this also published three earlier local commits not made by CC: `c2a5ee6`, `754d930`, `b11accb`
  ("3D queue / 3D-C").
- **gh run check:** `gh run list --workflow deploy.yml -L 1` → latest run is still `a3ea33b` (2026-09-23) — **no run for `aa6ccb8`**.
