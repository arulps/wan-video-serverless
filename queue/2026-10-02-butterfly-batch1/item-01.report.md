# item-01 report — checks + first half (72 s, ≤ $7.50 list)

## 1. Renames
None, as the item says: V5a is kept as rendered in gate 3 and is not in this queue. None of the 27 new IDs had files in `out\`
beforehand. The 79 existing files in `out\` (all kept takes + review images) were fingerprinted (md5) before the render; they are
unchanged after the render and after the sheets.

## 2–4. Checks
- **Mock:** `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Gates:**
  - `test_prompt_lint` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`;
  - `prompt_lint --song songs\a07-butterfly` → **`LINT PASS: 33 shots, 0 fail, 0 warn`**;
  - `test_song_cuts_reuse --plan-only` → `PASS (plan only): rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit`.

## 5. Dry-run, all 27
27 rows, all `720P 16:9 audio=off`. I1 and O4 are 7 s; the other 25 are 5 s (139 s total). Refs per row are 3–8.
**`estimated $13.90`**, 0 MISSING/ERROR/OVER BUDGET hits.

## 6. Render, first half
**Window: 20:40:24 → 21:12:11 UTC, 2026-10-02** (16:40:24 → 17:12:11 Toronto EDT). One at a time, `--max-usd 7.50`; the runner exited 0.

| clip | status | task id | wall s | length | frames | refs | est (list) | stills | every10 |
|---|---|---|---|---|---|---|---|---|---|
| I1 | done | `428e2b8c-0bdf-4807-a4ee-e467149d236a` | 182.0 | 7 s | 210 | 6 | $0.70 | f000/f104/f209 | 21 frames 7x3 1792x432 |
| I2 | done | `10b57b03-1cf1-42fc-ae8d-ea74998b1b44` | 151.1 | 5 s | 150 | 8 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| CH3 | done | `3476efcb-c222-4bb6-8a66-4c93ef36b51a` | 133.2 | 5 s | 150 | 4 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| CH4 | done | `4f23e8f3-893c-41a5-a160-8f8ef5f6d245` | 131.1 | 5 s | 150 | 4 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V1b | done | `80edd1b9-4e6f-44c0-bbdf-8c0c7b6a0962` | 116.6 | 5 s | 150 | 3 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V1c | done | `d2a8e50b-b56d-4d31-bc6e-a9e2af296d1a` | 133.0 | 5 s | 150 | 3 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V1d | done | `c81d4106-284c-4229-b4e3-f180b88756b7` | 132.5 | 5 s | 150 | 3 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V2c | done | `4674b241-1d66-4557-ac39-ed8213489c81` | 132.2 | 5 s | 150 | 3 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V2d | done | `fb942a98-75d7-40ea-815e-4cbedc985c6f` | 116.2 | 5 s | 150 | 3 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V3a | done | `81120d54-2f42-482d-b9d3-c7d00edf6bff` | 132.3 | 5 s | 150 | 3 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V3b | done | `b6233584-cab0-4dd7-9b9b-76b33d1972a8` | 133.7 | 5 s | 150 | 3 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V3c | done | `6c9caeff-e446-4821-8a07-7b19a2ff3b61` | 131.6 | 5 s | 150 | 3 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| V3d | done | `29efb093-a3a7-4c17-a9e8-ac8d709a6021` | 133.2 | 5 s | 150 | 3 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |
| BRKb | done | `dc85baa0-e06c-4b63-8e6a-272c3d4a0b36` | 131.5 | 5 s | 150 | 4 | $0.50 | f000/f074/f149 | 15 frames 5x3 1280x432 |

- **First half: 14/14 done, 72 s, estimated $7.20 at list price** (cap $7.50).
- **Failures:** none. All are 1280×720 @ 30 fps (frames counted by ffprobe), video only. Each sidecar prompt equals its `*.raw.txt`.
  No URL or key appears in the sidecars or in the log `C:\Projects\opencode\video_image\songs\a07-butterfly\batch1a.log`.

## 7. Sheets and stills
In `C:\Projects\opencode\video_image\songs\a07-butterfly\out\_qc\`, per clip:
- `<ID>-every10.png`: every 10th frame, 256 wide; I1 7×3 (21 frames → 1792×432), the others 5×3 (15 frames → 1280×432);
- `<ID>-f000.png` / `-fMID` / `-fLAST` (I1: f000/f104/f209; 5 s clips: f000/f074/f149), 1280×720;
- `<ID>-strip.png` (written by the runner).

Clips: `C:\Projects\opencode\video_image\songs\a07-butterfly\out\<ID>-seed30313-w3.mp4` (+ `.json`), for ID = I1, I2, CH3, CH4,
V1b, V1c, V1d, V2c, V2d, V3a, V3b, V3c, V3d, BRKb.
