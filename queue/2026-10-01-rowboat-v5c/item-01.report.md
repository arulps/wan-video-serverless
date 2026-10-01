# item-01 report — render V5c, sheet, commit (≤ $0.50 list)

- **Mock:** `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Lint:** `tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`. `prompt_lint.py --only V5c` →
  `LINT PASS: 1 shots, 0 fail, 0 warn`.
- **Dry-run:** 1 row, `wan3.0-video 720P 16:9 4s audio=off`, refs=6 (`Appa, Appa, Mintu, Mintu, Minnu, Minnu`), **`estimated $0.40`**,
  0 MISSING/ERROR hits.
- The prompt contains the new line "Their faces stay exactly their own: no whiskers, no animal nose, no face paint, nothing drawn on
  their faces." It was sent verbatim (the sidecar prompt equals `shots\24_V5c.raw.txt`).
- **Protected:** 294 files (the 28 done shots' files, every `*-v1-*` / `*-v2-*` / `*splice*`), md5 unchanged after the render and
  after the sheets. The old take `V5c-seed30313-w3-v2-mouse-nose.*` is untouched.
- **Render window:** **22:55:01 → 22:56:58 UTC, 2026-10-01** (18:55:01 → 18:56:58 Toronto EDT). `--max-usd 0.50`; the runner exited 0.

| shot | status | task id | wall s | length | frames | refs | est (list) |
|---|---|---|---|---|---|---|---|
| V5c | done | `76c18a79-eac9-4f16-b720-da23be6edf4d` | 116.4 | 4 s | 120 | 6 (family) | $0.40 |

- **Failures:** none. 1280×720 @ 30 fps, video only. No URL or key appears in the sidecar or the log.
- **Sheet / stills:**
  - `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\V5c-contact.png` (5×2, 10 frames evenly spaced, 384 wide → 1920×432)
  - `C:\Projects\opencode\video_image\songs\rowboat\out\_qc\V5c-f012.png`, `V5c-f060.png`, `V5c-f114.png` (1280×720)
- Clip: `C:\Projects\opencode\video_image\songs\rowboat\out\V5c-seed30313-w3.mp4` (+ `.json`)
- Log: `C:\Projects\opencode\video_image\songs\rowboat\batch_v5c.log`
- **Commit:** the `[skip ci]` commit containing this file. The hash is in `item-02.report.md` and in CC's chat reply.
