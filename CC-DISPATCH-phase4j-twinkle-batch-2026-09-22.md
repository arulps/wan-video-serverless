# CC-DISPATCH — Phase 4j: first full song batch — Twinkle Twinkle, 21 shots at 832×480 (2026-09-22)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC. **This is the first real song footage.**
**Budget: 2.5 h pod time** (H100 preferred ≈ $9; A100 ≈ $6 but slower) — `--max-minutes 150`, hard stop 3 h.
Fresh pod from R2, self-stop via the runner (proven in 4i), no persistent pods.

## 0 · Fable's frame check of 4i (`songs/_ab3-2026-09-22/out/`)
- **S03_full PASSES** the thing it was testing: three distinct people, the boy with his own short black hair, the girl
  with pigtails and violet dungarees, Appa alone rowing. (Appa took the stern seat instead of the middle — wording
  tightened; not a blocker.) `S03_order` (distilled) still gave the boy pigtails → **rule: any shot with both children
  runs `mode=full`**. 17 of Row's 21 rows and 7 of Twinkle's are now `full`.
- **T09a_early FAILS** — no wink at any frame, and the eyes degrade in the last second. Prompt timing does not steer
  the sampler. So T09a now uses the **`keyframe` column**: frame 0 is pinned to the clean wink frame from 4h
  (`songs/twinkle-twinkle/keyframes/T09a-wink-480.png`, the last frame of `T09a_full1`) and the prompt only holds it.
  Verified against ComfyUI source (`WanVaceToVideo` pads a 1-frame control video with 0.5 and a 1-frame mask with
  1.0, so one image + one zero mask pins exactly frame 0). Mock-tested: the graph gains `LoadImage`(15) +
  `SolidMask`(16) wired to `control_video`/`control_masks`; other rows untouched.
- Stop-cmd worked (exit 0, EXITED). Report paths every time — thank you.

## 1 · On disk (Fable; dry-run + mock verified; not committed)
| file | change |
|---|---|
| `comfy/run_comfy.py` | `add_first_frame_keyframe()` |
| `comfy/batch_runner.py` | `keyframe` column: uploads it, wires nodes 15/16, dry-run prints `keyframe=` and `!! KEYFRAME MISSING`, sidecar records it |
| `songs/twinkle-twinkle/shots.csv` | `keyframe` column; 7 rows `mode=full` (both children); **T09a: single-tile ref + keyframe + full** |
| `songs/twinkle-twinkle/shots/T09a.txt` | POSE "already winking", MOTION "holds the wink steady for the whole shot" |
| `songs/twinkle-twinkle/keyframes/T09a-wink-480.png` | the keyframe (832×480) |
| `songs/row-row-row-your-boat/shots.csv` | `keyframe` column; 17 rows `mode=full` |
| `songs/row-row-row-your-boat/shots/S03.txt` | "Appa on the middle seat" |
| `docs/PROMPT-PLAYBOOK.md`, `docs/SHOT-LIST-SPEC.md` | §3e 4i results; `keyframe` column |

## 2 · Steps
1. Dry-runs (no GPU): `_selftest` 2 / `twinkle-twinkle` 21 (7 `mode=full`, T09a shows `keyframe=…`, no MISSING) /
   `row-row-row-your-boat` 21 (17 full). No `OVER BUDGET`.
2. **Blocking pass = 832×480 for the whole song.** Do NOT edit 21 rows by hand: run with the size override
   `--size 832x480` if the runner has it — it does not yet, so use this one-liner on a *copy* of the CSV:
   ```
   python - <<'PY'
   import csv,io; p='songs/twinkle-twinkle/shots.csv'; r=list(csv.reader(open(p,encoding='utf-8',newline='')))
   i=r[0].index('size'); [row.__setitem__(i,'832x480') for row in r[1:]]
   w=io.StringIO(); csv.writer(w,lineterminator='\n').writerows(r); open(p,'w',encoding='utf-8',newline='').write(w.getvalue())
   PY
   ```
   (and put `1280x720` back the same way after the batch, before commit — the keepers run at 720p later with the
   same seeds). `git diff --stat` must show only the `size` cells changed.
3. `bash pod_bootstrap.sh wan-push`; fresh pod (H100 if any DC has one, else A100), env vars in the console, `pull`;
   then:
   ```
   cd /workspace/wan
   python comfy/batch_runner.py --song songs/twinkle-twinkle --hosts http://127.0.0.1:8188 --seed 30313 \
       --max-minutes 150 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/twinkle-twinkle && runpodctl stop pod $RUNPOD_POD_ID"
   ```
   Expected: 14 distilled rows ≈ 1–2 min each, 7 full rows ≈ 8 min each (H100) → ≈ 80–90 min; A100 ≈ 2 h.
   If `--max-minutes` interrupts, the CSV keeps `done` rows; a second run with the same command resumes the rest —
   that is fine, do it on a fresh pod, don't extend the budget by hand.
4. Pull `out/`; report **every clip's full path** (`…\songs\twinkle-twinkle\out\<shot>-seed30313-s<steps>.mp4` and
   `…\out\_qc\<shot>-strip.png`), wall time per shot, total GPU minutes and $, and the stop-cmd exit code.
   Say which rows failed (status `failed`) and why, without retrying.
5. **Commit** (this is the combined commit held since 4g): `git add comfy/ docs/ songs/` (all song folders incl.
   `_ab*`, `_untrimmed-*`, `keyframes/`; `out/` and `refs/` stay untracked) + this dispatch;
   message `songs: Twinkle + Row re-cut to budget, per-row mode/keyframe, A/B records 4g-4i; runner: mode + keyframe`.

## 3 · What happens next
Fable frame-checks all 21 strips and marks each row keep / retake (retakes = new seed or prompt edit, status
cleared). Arul looks at the same strips (paths above). Then Row's 21 at 480p (4k), then both songs' keepers at
1280×720 (4l), then the edit.
