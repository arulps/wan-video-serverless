# item-01 report — keep old RA, checks, render RA + RB + V1a + V2a, sheets, commit (≤ $2.80 list)

## 1. Old RA kept (renamed, not copied or deleted)
- `songs\a07-butterfly\out\RA-seed30313-w3.mp4` → `RA-seed30313-w3-v1-tall-priya.mp4`, and `RA-seed30313-w3.json` →
  `RA-seed30313-w3-v1-tall-priya.json`. md5 is the same before and after the rename.
- Step 7 would also have overwritten the old RA's review images, so before building the new ones CC renamed these in `_qc\`:
  - `RA-contact.png` → `RA-contact-v1-tall-priya.png`, as the item asks;
  - `RA-f000/f060/f120/f180/f239.png` → `…-v1-tall-priya.png`. The new `RA-f000.png` / `RA-f239.png` would otherwise have replaced
    the first and last of these.
  - Fable's `RA-flap-40-100.png` is untouched.
- ⚠ **`_qc\RA-strip.png` was overwritten by the runner itself.** `batch_runner.py` writes `<ID>-strip.png` automatically when a clip
  finishes (13:28:31 local, when the new RA finished). The item says the `_qc\RA-*` files stay as they are, but this one is
  replaced on any re-render of RA. **Restored:** CC regenerated the old strip from the kept old take with the runner's own
  `write_qc_strip()` (frames 0/20/40/60/80) → `_qc\RA-strip-v1-tall-priya.png`. `RA-strip.png` now belongs to the new RA.
  Suggestion for Fable: future redo items should also rename `<ID>-strip.png` before rendering.

## 2–5. Checks
- **Mock:** `PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars`.
- **Credentials:** `credentials present: True`. No values were printed.
- **Gates:**
  - `test_prompt_lint` → `PASS: prompt_lint catches 4 failure patterns, passes 2 fixed ones`;
  - `prompt_lint --song songs\a07-butterfly` → **`LINT PASS: 33 shots, 0 fail, 0 warn`**;
  - `test_song_cuts_reuse --plan-only` → `PASS (plan only): rowboat order unchanged; butterfly 47/48 slots, re-use + trims fit`.
- **Dry-run** (`--only RA,RB,V1a,V2a`): 4 rows, all `720P 16:9 audio=off`, **`estimated $2.60`**, 0 MISSING/ERROR hits.
  - RA 8 s refs=6 (Mintu, Minnu, Leo, Priya, Amma, Mrs Meena)
  - RB 8 s refs=4 (Mintu, Minnu, Leo, Priya)
  - V1a 5 s refs=3 (Mintu, Leo, the red butterfly)
  - V2a 5 s refs=3 (Minnu, Priya, the yellow butterfly)

## 6. Render
**Window: 17:25:16 → 17:35:58 UTC, 2026-10-02** (13:25:16 → 13:35:58 Toronto EDT). `--hosts api` (one at a time), `--max-usd 2.80`;
the runner exited 0.

| clip | status | task id | wall s | length | frames | refs | est (list) | stills |
|---|---|---|---|---|---|---|---|---|
| RA | done | `bd00942f-cdea-44ca-84fe-2e2f610fea04` | 189.1 | 8 s | 240 | 6 (Mintu, Minnu, Leo, Priya, Amma, Mrs Meena) | $0.80 | f000 / f119 / f239 |
| RB | done | `9ef158f1-3bb4-420b-bc37-116ab8f53fba` | 172.7 | 8 s | 240 | 4 (Mintu, Minnu, Leo, Priya) | $0.80 | f000 / f119 / f239 |
| V1a | done | `60e3eefe-b3c7-4de9-b6de-5aa7bd404d6d` | 154.7 | 5 s | 150 | 3 (Mintu, Leo, the red butterfly) | $0.50 | f000 / f074 / f149 |
| V2a | done | `cfeaaefb-e714-4747-9066-4984b0a24b4a` | 116.0 | 5 s | 150 | 3 (Minnu, Priya, the yellow butterfly) | $0.50 | f000 / f074 / f149 |

- **Total: 26 s, estimated $2.60 at list price** (~$1.82 with the 30% discount); cap $2.80.
- **Failures:** none. All four are 1280×720 @ 30 fps (frames counted by ffprobe), video only. Each sidecar prompt equals its
  `*.raw.txt`. No URL or key appears in the sidecars or in the log. All 4 status cells are `done`.

## 7. Sheets and stills
In `C:\Projects\opencode\video_image\songs\a07-butterfly\out\_qc\`:
- `<ID>-contact.png`: 5×2, 10 frames evenly spaced, 384 wide → 1920×432.
- 100% stills of the first, middle and last frame (1280×720): `RA-f000.png`, `RA-f119.png`, `RA-f239.png`; `RB-f000.png`, `RB-f119.png`,
  `RB-f239.png`; `V1a-f000.png`, `V1a-f074.png`, `V1a-f149.png`; `V2a-f000.png`, `V2a-f074.png`, `V2a-f149.png`.
- Old RA, kept: `RA-contact-v1-tall-priya.png`, `RA-f000/f060/f120/f180/f239-v1-tall-priya.png`, `RA-strip-v1-tall-priya.png`
  (regenerated), and `..\RA-seed30313-w3-v1-tall-priya.mp4` (+ `.json`).

Clips: `C:\Projects\opencode\video_image\songs\a07-butterfly\out\RA-seed30313-w3.mp4`, `RB-seed30313-w3.mp4`, `V1a-seed30313-w3.mp4`,
`V2a-seed30313-w3.mp4` (+ `.json` each). Log: `C:\Projects\opencode\video_image\songs\a07-butterfly\batch_gate1b.log`.
Nothing was written to `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\`. `songs\rowboat\` was not touched.

## 8. Commit
The `[skip ci]` commit containing this file. It holds `tests/test_song_cuts_reuse.py`, `songs/a07-butterfly/` except `out/` (new
`refs/08-priya-front.jpg`, the updated `shots/*.raw.txt`, `shots.csv`, `batch_gate1b.log`) and the queue folder. The hash is in
CC's chat reply.
