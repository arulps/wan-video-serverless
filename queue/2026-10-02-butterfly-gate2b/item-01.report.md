# item-01 report — keep old V2a, checks, render V2a, sheets, commit (≤ $0.60 list)

## 1. Renames (V2a only; V1a kept as is)
In `songs\a07-butterfly\out\`: `V2a-seed30313-w3.mp4/.json` → `V2a-seed30313-w3-v1.mp4/.json`.
In `out\_qc\`: `V2a-contact.png`, `V2a-every10.png`, `V2a-f000.png`, `V2a-f074.png`, `V2a-f149.png`, `V2a-strip.png` → the same names
with `-v1` before `.png`. The strip was renamed **before** the render.
- 8 files in total, md5 the same after the rename. No target name existed beforehand.
- After the render and the sheets, the md5 of the 8 `-v1` files is unchanged, and so is the md5 of the 38 other files in `out\`
  (RA, RB, V1a, the `-v1-tall-priya` RA, all their `_qc` images).

## 2–5. Checks
- **Mock:** `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Gates:**
  - `test_prompt_lint` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`;
  - `prompt_lint --song songs\a07-butterfly` → **`LINT PASS: 33 shots, 0 fail, 0 warn`**;
  - `test_song_cuts_reuse --plan-only` → `PASS (plan only): rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit`.
- **Dry-run** (`--only V2a`): 1 row, `wan3.0-video 720P 16:9 5s audio=off`, refs=3 (`Minnu, Priya, the yellow butterfly`),
  **`estimated $0.50`**, 0 MISSING/ERROR hits.
- The rev 3.3 lines are present in `shots\11_V2a.raw.txt`:
  - "the top of Priya's head is level with the top of Minnu's head";
  - "Every child named in this shot is already in the frame from the very first frame to the last".

## 6. Render
**Window: 18:43:03 → 18:45:01 UTC, 2026-10-02** (14:43:03 → 14:45:01 Toronto EDT). `--max-usd 0.60`; the runner exited 0.

| clip | status | task id | wall s | length | frames | refs | est (list) |
|---|---|---|---|---|---|---|---|
| V2a | done | `cd8816fd-c353-4074-b558-e283ad8aaeae` | 116.9 | 5 s | 150 | 3 (Minnu, Priya, the yellow butterfly) | $0.50 |

- **Failures:** none. 1280×720 @ 30 fps (ffprobe counted 150 frames), video only.
- The sidecar prompt equals `shots\11_V2a.raw.txt` verbatim. No URL or key appears in the sidecar or the log.

## 7. Sheets and stills
In `C:\Projects\opencode\video_image\songs\a07-butterfly\out\_qc\`:
- `V2a-contact.png`: 5×2, 10 frames evenly spaced, 384 wide → 1920×432.
- `V2a-every10.png`: frames 0, 10 … 140 (15 frames), 256 wide, tiled 5×3 → 1280×432.
- `V2a-f000.png`, `V2a-f074.png`, `V2a-f149.png`: 100% stills, 1280×720.
- `V2a-strip.png`: new, written by the runner.
- Old take, for comparison: `..\V2a-seed30313-w3-v1.mp4` (+ `.json`) and `V2a-contact-v1.png`, `V2a-every10-v1.png`, `V2a-f000-v1.png`,
  `V2a-f074-v1.png`, `V2a-f149-v1.png`, `V2a-strip-v1.png`.

Clip: `C:\Projects\opencode\video_image\songs\a07-butterfly\out\V2a-seed30313-w3.mp4` (+ `.json`).
Log: `C:\Projects\opencode\video_image\songs\a07-butterfly\batch_gate2b.log`.
Nothing was written to `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`. `songs\rowboat\` was not touched.

## 8. Commit
The `[skip ci]` commit containing this file. It holds `songs/a07-butterfly/` except `out/` (rev 3.3 `shots/*.raw.txt`, `shots.csv`,
`cutplan.json` (RB trim ≥ 1.0 s), `batch_gate2b.log`) and the queue folder. The hash is in CC's chat reply.
