# item-01 report — checks, render RA, sheet, commit (≤ $0.90 list)

- **Mock:** `tests\test_wan3_mock.py` → `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Lint:** `tests\test_prompt_lint.py` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`.
  `prompt_lint.py --song songs\a07-butterfly` → **`LINT PASS: 33 shots, 0 fail, 0 warn`**.
- **Plan test:** `tests\test_song_cuts_reuse.py --plan-only` → `PASS (plan only): rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit`.
- **Dry-run, all 33 rows:** 33 rows, all `720P 16:9 audio=off`, **`estimated $17.50`**, 0 MISSING/ERROR/OVER BUDGET hits.
  - Refs per row: 12× 3, 4× 4, 4× 5, 2× 6, 11× 8 (max 8).
  - **RA row:** `wan3.0-video 720P 16:9 8s audio=off, est $0.80 (list price); refs=6 labels=['Mintu', 'Minnu', 'Leo', 'Priya', 'Amma', 'Mrs Meena']`.
- **Render window:** **16:59:49 → 17:03:23 UTC, 2026-10-02** (12:59:49 → 13:03:23 Toronto EDT). `--max-usd 0.90`; the runner exited 0.

| clip | status | task id | wall s | length | frames | refs | est (list) |
|---|---|---|---|---|---|---|---|
| RA | done | `f625fb16-da8a-42a5-85a8-88f323a84f47` | 212.2 | 8 s | 240 | 6 (Mintu, Minnu, Leo, Priya, Amma, Mrs Meena) | $0.80 |

- **Failures:** none. The video is 1280×720 @ 30 fps (ffprobe `-count_frames`: 240), video only (audio off).
- The sidecar prompt equals `shots\03_RA.raw.txt` verbatim. No URL or key appears in the sidecar or the log.
- **Sheet / stills** (`C:\Projects\opencode\video_image\songs\a07-butterfly\out\_qc\`):
  - `RA-contact.png`: 5×2, frames 0, 27, 53, 80, 106, 133, 159, 186, 212, 239, 384 wide → 1920×432
  - `RA-f000.png`, `RA-f060.png`, `RA-f120.png`, `RA-f180.png`, `RA-f239.png` (1280×720 each)
- Clip: `C:\Projects\opencode\video_image\songs\a07-butterfly\out\RA-seed30313-w3.mp4` (+ `.json`, `_qc\RA-strip.png`)
- Log: `C:\Projects\opencode\video_image\songs\a07-butterfly\batch_gate1.log`
- Nothing was written to `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`.
- **Commit:** the `[skip ci]` commit containing this file. The hash is in `item-02.report.md` and in CC's chat reply.
