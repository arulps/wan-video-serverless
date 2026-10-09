# item-01 — BLOCKED at step 3 (mock test fails on Beast). Nothing rendered, $0.00 spent.

**Why blocked.** `py tests\test_wan3_mock.py` does not PASS on Beast, and the reason is **not** a missing Python module, so
step 2's "install just that module" does not apply. The test fails on its last check:

```
  File "C:\Projects\opencode\video_image\tests\test_wan3_mock.py", line 102, in main
    assert os.path.exists(os.path.join(song, "out", "_qc", "R2-strip.png"))
AssertionError
```

The strip is missing because Beast's ffmpeg (9.0.2) rejects the option the runner uses to make it:

```
note: ffmpeg QC strip failed for LOOP-seed30313-w3p.mp4 - ...
Unrecognized option 'vsync'.
Error splitting the argument list: Option not found
```

The option is in `comfy\batch_runner.py` line 536:
`cmd = ["ffmpeg", "-y", "-i", mp4_path, "-vf", vf, "-vsync", "0", "-frames:v", "1", out_png]`
(the only place in the repo's scripts; ffmpeg 9 removed `-vsync`, the replacement is `-fps_mode`). Same kind of problem as
`-filter_complex_script` in the Beast 4K queue. I did not change the runner or the test — that is Fable's fix.

Everything else in the mock test passed before that line: dry-run, refusal without `--max-usd`, the $1.20 cap, the API-rule
refusal, both request bodies, and no secrets or URLs in the sidecar.

## What was done

**Step 1 — tidy (done).** 16 rev 1.9 files moved from `songs\l05-urulai-w3\shots\` to
`_to_delete\l05-urulai-w3-shots-rev19\` (moved, not deleted):
`04_Z1`, `05_Z2`, `07_Z4`, `10_Z7`, `11_Z8`, `12_K1`, `13_K2`, `14_K3`, `15_K4`, `16_K5`, `17_K6`, `18_K7`, `19_CA`, `20_CB`,
`21_O1`, `22_O2` (each `.raw.txt`).
17 remain, one per `shots.csv` row, names match exactly:
I1, SA, SB, ZK1, ZK2, Z3, ZK4, Z5, Z6, ZK7, K3, K5, K6, ZO, CA, CB, O2.

**Step 2 — modules.** None installed. No module was missing.

**Step 3 — `py tests\test_wan3_mock.py`: FAIL** (above). → blocked here.

**Steps 4 and 5 — run in the same batch as step 3, before the failure was read:**
- Credentials: `credentials present: True`. No values were printed.
- `py tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`
- `py comfy\prompt_lint.py --song songs\l05-urulai-w3` → `LINT PASS: 17 shots, 0 fail, 0 warn`

**Steps 6–9 — not done.** No dry-run, no render, no sheets, no commit. `songs\l05-urulai-w3\` and this queue folder are
still untracked in git.

## For Fable
- The real render would probably still work: the runner prints the strip failure as a `note:` and carries on (both mock clips
  ended `done`). But the gate says the mock test must PASS, so it was not started.
- One more thing for step 9 when it is re-queued: `.gitignore` has a `refs/` line, so `songs/l05-urulai-w3/refs/` will need
  `git add -f` (the item says the commit includes `refs/`).
