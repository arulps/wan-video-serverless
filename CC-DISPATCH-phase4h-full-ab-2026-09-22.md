# CC-DISPATCH — Phase 4h: A/B round 2 — full sampling vs distilled on the two fragile shots (2026-09-22)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC. **Budget:** ≤ 20 min pod time (A100 ≈ $0.55).
Hard stop 30 min. **Fix the stop-cmd bug first (§1) — the pod must stop itself this time.**

## 0 · Fable's frame check of 4g (`songs/_ab-2026-09-22/out/`)
Your reading was right on every row, and the decision tree did not fit because both shots failed for the same
underlying reason: the distilled sampler does not follow fine instructions, and raising cfg makes it follow them
*less* — cfg 2 removed the expression entirely (no wink, no blink), and at cfg 1.5 the boy still wears the girl's
pigtails and both children hold oars against POSE + negative. What did work and is now a rule: **Appa between the
children → three people, correct seats** (both `between` rows). The ghost TV at seed 4242 (rows `_c2_s2`, `_s6`)
is the second tile of the same character on the wink sheet — one identity tile per character from now on.
Written up as playbook §3e. Boot-to-ready 260 s from R2 on a fresh A100 is the number we wanted.

## 1 · Two fixes before any GPU
1. **Pod env for the stop-cmd.** The runner's `--stop-cmd` runs in a subprocess of the runner, which inherits the
   *runner's* environment — a `export` in an earlier SSH session is not there. Put the four R2 vars (+ `RUNPOD_API_KEY`)
   in the pod's **Environment Variables in the RunPod console** (pod → Edit) so every shell on the pod has them, or
   start the runner from a shell that has them exported in the same session. Verify before the batch:
   `bash /workspace/pod_bootstrap.sh out-push songs/_ab-2026-09-22` by hand — it must push the 4g outputs that never
   reached R2 — and `runpodctl stop pod --help` must work in that same shell. Only then run the batch.
2. `python comfy\batch_runner.py --song songs\_ab2-2026-09-22 --hosts http://x --dry-run` → 5 rows, `mode=full`
   on three of them, no REF MISSING after `python scripts\build_song_refs.py --song twinkle-twinkle --no-cut`
   (adds the single-tile `minmini-front-16x9.png`).

## 2 · What changed on disk (Fable; verified with a fake ComfyUI submit — the `full` rows build a graph with no
LoRA node, `uni_pc`, 30 steps, cfg 5; sidecars record `mode`)
| file | change |
|---|---|
| `comfy/batch_runner.py` | new optional `mode` column: `distilled` (default) / `full` (no LoRA, uni_pc, defaults 30 / 5.0 unless the row sets steps/cfg); shown in dry-run and sidecar |
| `docs/SHOT-LIST-SPEC.md`, `docs/PROMPT-PLAYBOOK.md` | `mode` column; **§3e** — what the distilled sampler will not do, with the 4g evidence |
| `scripts/build_song_refs.py` | `twinkle-twinkle/refs/minmini-front-16x9.png` (single tile) |
| `songs/_ab2-2026-09-22/` | **new** — 5 rows, 832×480 (README inside) |

## 3 · The five rows
| row | what it tests | cost |
|---|---|---|
| `T09a_full` | full sampling, two-tile wink sheet, seed 30313 | ~4 min |
| `T09a_full1` | full sampling, **single-tile** sheet | ~4 min |
| `T09a_d1` | distilled cfg 1 seed 4242 single-tile — ghost check only (4g `_s6` had the ghost with two tiles) | ~1 min |
| `S03_full` | full sampling, Appa-between sheet | ~5 min |
| `S03_order` | distilled cfg 1.5, Appa-between, **Mintu first in `cast`** (his lock line was last = first to lose) | ~2 min |

```
cd /workspace/wan
python comfy/batch_runner.py --song songs/_ab2-2026-09-22 --hosts http://127.0.0.1:8188 --seed 30313 \
    --max-minutes 25 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/_ab2-2026-09-22 && runpodctl stop pod $RUNPOD_POD_ID"
```
Report the five strips + JSONs + wall times (the `full` wall times set the 720p production estimate for fragile shots).

## 4 · What decides what (Fable frame-checks)
- **T09a**: a `full` row winks (one eye closed, other open, mouth closed) → expression shots run `mode=full`; the
  single-tile vs two-tile result decides the sheet rule. Neither winks → keyframes (§3d step 3), no more sampling
  variants.
- **Ghost**: `T09a_d1` clean → the two-tile sheet was the ghost's cause (rule confirmed); ghost still there → it is
  seed 4242 and we avoid it (note in the song).
- **S03**: `S03_full` gives a cowlick boy in green in the stern, girl in violet in the bow, children's hands on the
  gunwales, Appa alone rowing → two-child shots run `mode=full`. `S03_order` alone fixes the hair → cast order is the
  cheap rule and distilled stays. Both fail → keyframes for two-child shots, or re-plan as singles + wide.

## 5 · Not in this dispatch
- The other 40 shots (they get `mode` + cast-order + sheet rules from this result, then one commit — including
  `songs/_ab-2026-09-22/` and `songs/_ab2-2026-09-22/` as the record, `out/` untracked).
