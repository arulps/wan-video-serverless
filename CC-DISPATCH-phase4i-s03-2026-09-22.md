# CC-DISPATCH — Phase 4i: the S03 rows 4h never reached + the wink timing rerun (2026-09-22)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC. **Budget: 45 min pod time** (A100 ≈ $1.20) —
full sampling is ~12 min per 480p shot, so `--max-minutes 40`, hard stop 50 min. Runs on a fresh pod from R2;
no persistent pods (4h §1.0 still applies if any pod is left).

## 0 · Fable's frame check of 4h (`songs/_ab2-2026-09-22/out/`)
- **`T09a_full1` PASSES the wink** — single tile, full sampling: left eye closes into a curved arc, right eye open,
  mouth closed, no ghost, no extra wings, clean world. It arrives at frames 75–80 (the last 0.4 s) instead of early
  and held; that is a prompt-timing fix, not a sampling problem. `T09a_full` (two-tile) never winked. Rules recorded in
  playbook §3e: one identity tile per character, expression shots `mode=full`, timing stated in MOTION.
- The stop-cmd bug was **mine** (`shlex.split` + `shell=False`); your `shell=True` fix and the pipefail fix are right and
  are in the mirror now. Thanks for finding it rather than working around it.
- 725 s per 480p full-sampled shot is the planning number: ~25–30 min ≈ $0.75 per 720p expression/two-child shot.

## 1 · On disk (Fable, dry-run verified; not committed)
| file | change |
|---|---|
| `songs/twinkle-twinkle/shots/T09a.txt` | MOTION: "within the first second … holds that wink steady to the very end" |
| `songs/twinkle-twinkle/shots.csv` | `mode` column added; **T09a → `refs/minmini-front-16x9.png`, `mode=full`** (production setting) |
| `songs/row-row-row-your-boat/shots.csv` | `mode` column added (empty = distilled) |
| `songs/_ab3-2026-09-22/` | **new** — 3 rows, cheapest first (see below) |
| `docs/PROMPT-PLAYBOOK.md` | §3e 4h result |

## 2 · Rows (in this order — the CSV order is the run order)
| row | what | est. |
|---|---|---|
| `S03_order` | distilled cfg 1.5, Appa-between sheet, **Mintu first in cast** | ~2 min |
| `S03_full` | full sampling, Appa-between sheet, 101 frames | ~15 min |
| `T09a_early` | full sampling, single tile, new timing wording | ~12 min |

```
python comfy\batch_runner.py --song songs\_ab3-2026-09-22 --hosts http://x --dry-run      (3 rows, no REF MISSING, no OVER BUDGET)
bash pod_bootstrap.sh wan-push                                                            (laptop, rclone env)
# fresh pod, env vars set in the console, pull, then:
cd /workspace/wan
python comfy/batch_runner.py --song songs/_ab3-2026-09-22 --hosts http://127.0.0.1:8188 --seed 30313 \
    --max-minutes 40 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/_ab3-2026-09-22 && runpodctl stop pod $RUNPOD_POD_ID"
```
Report the three strips + JSONs + wall times, and the `--stop-cmd exit code` line (it must be 0 and the pod must be
stopped by the runner this time — check `runpodctl get pod` after).

## 3 · What decides what (Fable frame-checks)
- **S03**: `S03_full` shows a cowlick boy in green in the stern, pigtail girl in violet in the bow, children's hands on
  the gunwales, Appa alone rowing → all two-child shots in both songs run `mode=full` (12 in Row, 4 in Twinkle; ≈ $12
  extra per batch, acceptable). `S03_order` alone fixes the hair → cast order is the rule and distilled stays for them.
  Both fail on hair → VACE keyframes for two-child shots (next dispatch); both fail on oars only → "hands on the
  gunwales" becomes a NOT-line + negative and we accept it.
- **T09a_early**: wink within ~1 s and held → T09a is done at 480p; production row already set. Wink still at the tail →
  keep the setting and note "trim to the wink" for the editor; no more test rows.

## 4 · After this
Fable applies the rules to the remaining 40 shots (mode per row, cast order, sheet order), then one commit of
`songs/` including `_ab*` folders as the record (`out/` untracked). Then **4j = the first full 480p batch of both
songs** — the first real song footage.
