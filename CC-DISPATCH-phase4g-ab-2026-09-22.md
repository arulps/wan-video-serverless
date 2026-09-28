# CC-DISPATCH — Phase 4g: A/B on the two failed blocking shots (2026-09-22)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC. **Budget:** ≤ 15 min pod time (~$0.90 on the H100)
+ nothing else. Hard stop 25 min. Pod stops itself via the runner's `--stop-cmd`.

## 0 · Fable's frame check of the 4f blocking shots (`songs/*/out/*-seed30313-s4.mp4`)
- **T09a** — identity, world and framing are exactly right (mint house, amber door, mat, railing, crescent moon;
  Minmini's TV head, antennae, wings, feet). Fails on the one thing it was testing: a symmetric two-eye blink with the
  mouth opening, plus a stray second wing + green sleeve fragment by the door from frame ~48. Both are cfg-1.0
  symptoms — every negative is ignored — not identity or reference problems.
- **S03** — Appa is excellent and **his T-pose did not leak** (the POSE clause held). The boat, river and the 101-frame
  (6.3 s) length all hold: **6.3 s clips are fine, no fallback to 81 frames needed.** Fails on the two children: one
  child with Minnu's pigtails and Mintu's shirt, and she is holding an oar. Cause: the two near-identical child tiles
  side by side plus "Minnu"/"Mintu" being near-identical tokens at the tail of a 558-token prompt.
- Your real token counts calibrated the runner: **1.7 tokens/word** (runner estimates now land within ±2 % of the
  pod's count). Every shared block in both songs was re-cut to the new budgets (playbook §3b); all 44 shots now
  estimate ≤ 512 (twinkle max 505, row max 508) — a final trim to ≤ 490 with margin happens after this A/B decides
  the two-child rule, so the 40 untouched shots are edited once, not twice.
- Yes: **delete the empty network volume `mmqwks2rxf`** — R2 works, it is $4.20/mo for nothing.

## 1 · What changed on disk (Fable, verified by dry-run; nothing committed)
| file | change |
|---|---|
| `comfy/batch_runner.py` | `T5_TOKENS_PER_WORD = 1.7` (was 1.4) — only that line |
| `docs/PROMPT-PLAYBOOK.md` | §3b budgets re-based on 1.7; **new §3c** (two children: bind by outfit + position, never by name; sheet keeps them apart; cfg 1.5 if merged) and **§3d** (the wink: cfg 2 + negatives → second seed → VACE first/last-frame keyframes) |
| `songs/twinkle-twinkle/` | `style.txt` 24 w, `world.txt` 21 + 57 w, `characters.txt` locks 24–30 w incl. short Mintu/Minnu overrides; `shots/T09a.txt` rewritten (asymmetry spelled out, negatives add `symmetrical blink, sleeves, extra wings`) |
| `songs/row-row-row-your-boat/` | all six world files 21 + 40–54 w with "the girl in the bow, the boy in the stern"; `style.txt`; `characters.txt` locks 22–26 w; `shots/S03.txt` rewritten per §3c (outfit + position binding, "all three people", merge negatives) |
| `songs/_selftest/` | `style.txt` + short `characters.txt` so the plumbing test is inside budget (was 559) |
| `scripts/build_song_refs.py` | **Mintu now comes from `Turnarounds\Mintu_Latest`** (Arul, 2026-09-22): four Gemini renders identified by eye — `c82nyx…` front (T-pose, open-mouth smile), `7euvr…` left profile, `hbj14k…` right profile, `t0cqro…` back; light-grey studio background → rembg cut. `mintu-4view-16x9.png` = front/left/right/back; every kids/pair sheet uses the new front. The old `Mintu-gemini2` bible set is dropped (yellow-plastic skin in S03). New sheet `minnu-appa-mintu-16x9.png` (Appa between the children). |
| `songs/*/negative.txt`, `shots/S03.txt` | `T-pose, arms spread wide, arms outstretched` added — Mintu's front view is now a T-pose like Appa's, so every Mintu sheet carries two T-poses; the POSE clause held for Appa in S03, and the negative bites at cfg ≥ 1.5 |
| `songs/_ab-2026-09-22/` | **new** — six A/B rows at 832×480 pointing at the real song files by relative path (see its README) |

## 2 · Steps
1. Sanity, no GPU:
   ```
   python comfy\batch_runner.py --song songs\_selftest --hosts http://x --dry-run          (2 shots, 0 over)
   python comfy\batch_runner.py --song songs\twinkle-twinkle --hosts http://x --dry-run    (21, 0 over, max ~505)
   python comfy\batch_runner.py --song songs\row-row-row-your-boat --hosts http://x --dry-run (21, 0 over, max ~508)
   python scripts\build_song_refs.py                                                    (rebuilds all 17 sheets: rembg runs on the 4 new Mintu sources, the rest are cached cutouts)
   python comfy\batch_runner.py --song songs\_ab-2026-09-22 --hosts http://x --dry-run    (6 rows, no REF MISSING, max ~508)
   ```
   **Look at** `twinkle-twinkle\refs\mintu-4view-16x9.png`, `row-row-row-your-boat\refs\appa-mintu-minnu-16x9.png` and
   `minnu-appa-mintu-16x9.png` before step 2: the grey studio background must be gone (no grey halo around Mintu),
   the four Mintu views must read front / left / right / back, and the profile tiles must not be tiny. If a cut-out is
   bad, fix that source (`outputs\cutouts\mintu_*.png`) and rebuild; report the three sheets with the strips.
2. `bash pod_bootstrap.sh wan-push` from the laptop (rclone env set) so the pod gets the new songs/, sheets and playbook.
3. Start the (stopped) H100 pod from 4f → `bash pod_bootstrap.sh pull` (models already on its disk → seconds) → then:
   ```
   cd /workspace/wan
   python comfy/batch_runner.py --song songs/_ab-2026-09-22 --hosts http://127.0.0.1:8188 --seed 30313 \
       --max-minutes 20 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/_ab-2026-09-22 && runpodctl stop pod $RUNPOD_POD_ID"
   ```
   Expect six clips, ~50 s each at cfg 1.0 and ~100 s at cfg 1.5–2.0 (two passes), ≈ 8 min warm.
4. Pull `out/` to the laptop; report the six strips + JSONs. **Also run the real token count on `S03_c15`'s sidecar
   prompt** (same recipe as before) so the 1.7 calibration is confirmed on a re-cut prompt.

## 3 · What decides what (Fable frame-checks; do not iterate on your own)
- **T09a**: any of the three rows shows one eye closed while the other stays open, mouth closed → that row's cfg/seed
  becomes the T09a production setting. All three blink → §3d step 3 (keyframes) is the next dispatch; do not try more
  seeds.
- Note: S03 also changes Mintu's reference (Mintu_Latest), so `S03_c15` vs the 4f clip is prompt + sheet + cfg together; the two `between` rows isolate the sheet order.
- **S03**: three distinct people with the girl in violet in the bow and the boy in green in the stern, Appa alone
  rowing. If both "between" rows pass and `S03_c15` (old sheet) fails → the Appa-between sheet order becomes the
  rule for every kids+someone sheet in both songs (`build_song_refs.py` SHEETS). If `S03_c15` also passes → the
  prompt rewrite alone was enough and cfg 1.5 is the two-child setting. If all three fail → two-child shots get
  re-planned as singles + a wide (playbook §3b), no more GPU on this framing.

## 4 · Not in this dispatch
- Trimming the other 40 shots to ≤ 490 and applying the §3c wording to every two-child shot — Fable, right after
  this A/B, so it is done once with the winning rule.
- Commit: hold until the A/B result is in, then one commit with the trims (`songs/_ab-2026-09-22/` is committed too,
  as the record; its `out/` stays untracked).
