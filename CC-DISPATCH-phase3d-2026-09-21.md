# CC-DISPATCH — Phase 3d: R2 masters, framing fix, two gentle-motion clips (2026-09-21)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** Claude Code on the laptop.
**Cost:** one CI deploy (image rebuild, ~4 min) + selftest (~$0.02) + two 30-step clips (~$0.25).
**Order matters** — each part depends on the one before. No ladder is in flight.

## 0 · What the first ladders showed (Fable reviewed the frames)

Identity passed on both characters (right-brow cowlick, both pigtails + bows, same face at frame 81,
no mark in any corner). The failure was **framing + motion + review encode**, not steps:
- full-figure start frames left the character ~40 % of frame height → hands ~40 px → the model
  smeared/doubled them while waving;
- "wave" is the hardest motion (fast, small extremity), and Mintu started from a T-pose;
- the inline review copies were crf 23 (~470 kbps), which smears exactly that detail; the 2 MB
  masters were discarded.
20 vs 50 steps made no visible difference → **30 steps is the production default**; budget goes to
start frames and motion design instead.

## 1 · Part A — R2 (re-run Phase 3c; `.env` is now filled)

Follow `CC-DISPATCH-phase3c-r2-2026-09-21.md` exactly. Two reminders: the `.env` reader takes the
**first** matching line (a duplicate empty `TPL_ENV_S3_ENDPOINT_URL=` at the top of the file would
shadow the real one — check `.env` has each key once); report key names + value lengths, never values.
Apply the `deploy.yml` env lines by hand (protected path) but **do not push yet** — Part B pushes once.

## 2 · Part B — commit the worker + script changes, push once, watch CI

Working tree (all written by Cowork; tests pass offline):

| file | change |
|---|---|
| `app/generator.py` | result carries `gpu`; decode guard logs free/allocated/reserved at decode start and on OOM; a bf16 retry that also fails reports both causes; a non-OOM decode error is labelled "not OOM" with its type (the two ladder failures were unreadable — this makes the next one self-explaining) |
| `app/storage.py` | review-copy encode `COMPACT_CRF` env, default **18** (was hard-coded 23) |
| `handler.py` | reports the crf actually used |
| `scripts/step_ladder.ps1` | **`-Framing waist|close|full` (default `waist`)**: finds the figure's bounding box (background = mean of the 4 corner pixels; refs are ~245 grey or transparent, not pure white; 4-px scan, noise-tolerant), keeps the top `-TopFrac` (0.58 = waist-up, `close` = 0.40) and fills 96 % of the canvas height. Simulated on the Mintu ref: figure bbox 742,26–2076,1504 → medium shot, hands ≈120 px (was ≈40). Default `-Steps 30`; default prompt is slow motion (turn, smile, blink, breeze). |
| `tests/test_decode_guard.py`, `tests/test_handler.py` | updated (four guard cases; crf18) |
| `.github/workflows/deploy.yml` | the five R2 env lines from Part A |

```
git add app/generator.py app/storage.py handler.py scripts/step_ladder.ps1 tests/test_decode_guard.py tests/test_handler.py .github/workflows/deploy.yml CC-DISPATCH-phase3d-2026-09-21.md CC-DISPATCH-phase3c-r2-2026-09-21.md
git commit -m "worker: decode diagnostics + gpu in result, crf18 review copies; ladder: waist framing, 30-step default; ci: R2 env"
git push ; gh run watch
```
Deploy log: template env lists `S3_BUCKET`, `S3_ENDPOINT_URL`, `AWS_REGION` (secrets masked), PATCH `HTTP 200`,
drain to 0, restore 0/3. Then `scripts\first_video.ps1 -SelftestOnly` → `s3_bucket_set: true`,
`s3_endpoint_url_set: true`, `alloc_conf` set, cached snapshot found.

## 3 · Part C — two clips, gentle motion, waist framing, masters on R2

```
cd C:\Projects\opencode\video_image
powershell -ExecutionPolicy Bypass -File scripts\step_ladder.ps1 `
  -Image "C:\Channel Contents\MinMiniKids\charecter bible\generation-refs-2026-08-31\Minnu\body-relaxed.png" `
  -Label minnu-waist -SkipSelftest `
  -Prompt "Minnu slowly turns her head to look at the camera and smiles warmly, blinks once; her two pigtails with red bows sway in a gentle breeze; slow natural motion, soft matte children's picture-book look, camera steady, no text"

powershell -ExecutionPolicy Bypass -File scripts\step_ladder.ps1 `
  -Image "C:\Channel Contents\MinMiniKids\Model_Animation library\Charecters\Turnarounds\Mintu - gemini2\Gemini_Generated_Image_hzdq4fhzdq4fhzdq.png" `
  -Label mintu-waist -SkipSelftest -CropPx "0,0,2470,1536" -CanvasColor "#F4F4F4" `
  -Prompt "Mintu slowly lowers his arms to his sides, tilts his head and grins at the camera, blinks once; the cowlick above his right brow stays in place; slow natural motion, soft matte children's picture-book look, camera steady, no text"
```
(`-CanvasColor #F4F4F4` matches Mintu's own ~245 background so there is no visible box; Minnu's PNG is
transparent, so the default cream canvas is fine.)

Before each submit, open `outputs\ladder\<label>-startframe-1280x704.jpg`: it must be a **waist-up
medium shot**, head near the top, hands clearly visible and large. If the bbox went wrong (figure tiny
or cut through the face), stop and report the printed `framing=waist: figure bbox …` line.

With R2 live, each result carries `delivery: s3` and a URL; the script saves the **master** (raw
quality-8, ~2 MB) — that is what Arul should judge this time.

**Report:** the two `framing=…` lines, the two meta JSONs (`gpu`, `t_sample_s`, `vae_decode_*`,
`delivery`), file paths, and — if anything fails at decode — the full error, which now names its cause.

## 4 · Not in this dispatch

- Re-running the two failed ladder rungs (not needed; steps question is answered).
- The 14B I2V model on a 48 GB endpoint for hero close-ups — Phase 4, only if waist-framed 5B clips
  still fall short on hand/face motion.
