# item-01 — preflight, tests, commit ($0)

1. **Credentials** (Arul put them in `.env`: `DASHSCOPE_API_KEY`, `DASHSCOPE_WORKSPACE_ID`, `DASHSCOPE_REGION=ap-southeast-1`,
   Singapore). Check without printing:
   `python -c "import sys; sys.path.insert(0,'comfy'); import wan3_api; print('credentials present:', wan3_api.credentials_present())"`
   Also confirm the region line exists without showing values:
   `python -c "print('region line:', any(l.strip().startswith('DASHSCOPE_REGION=ap-southeast-1') for l in open('.env')))"`
   Both must print True, else **blocked** (say which one is False).
2. **L01 keyframe** — dispatch 6e Part A2: if `C:\Channel Contents\MinMiniKids\YT Shorts\keyframes\L01-start.png`
   (or .jpg/.jpeg) exists, fit it to `songs\shorts-loops\keyframes\L01-start.png` with the one-liner from
   `CC-DISPATCH-phase6d-flf2v-L01-2026-09-28.md` Part A1. If it does not exist, note "L01 skipped" and continue.
3. **Tests + dry-runs + commit** — dispatch 6e Part B exactly (both mock tests PASS, py_compile, `bash -n`, the two
   dry-runs, git add list **plus `queue/2026-09-28-wan3-setup`**, commit with `[skip ci]`, push, `gh run list --workflow deploy.yml -L 1` shows no run for it).
   Any test not PASS → **blocked**.

**item-01.report.md:** the two True/False results; keyframe fitted (source size, cropped or not) or skipped; the last
line of each mock test; dry-run estimates; commit hash; the gh run check.
