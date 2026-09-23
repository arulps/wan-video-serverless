# CC-DISPATCH — Phase 4k: Twinkle 480p retakes (4 shots) (2026-09-23)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC. **Budget: 30 min pod time** (H100 ≈ $1.75).
`--max-minutes 25`, hard stop 35 min. Fresh pod from R2, self-stop. Step 0b of 4j (endpoints at 0/0, no pods, no
volumes, balance check) still applies — confirm in one line.

## 0 · Fable's frame check of 4j
17 of 21 keep, 4 retake — full table in `songs/twinkle-twinkle/REVIEW-480p-2026-09-23.md` (committed with this).
Retakes: **T05** (a person at the door in a no-cast shot), **T09b** (Minmini orange in profile), **T10** (two
Minminis), **T19** (a hand-lantern prop). The keyframe wink (T09a) works for ~2 s then wobbles — kept, cut at 2 s.
Also found: full-sampled terrace shots render a lime house, distilled ones mint — decision for the 720p run, see the
review §"Continuity finding". Note: the laptop `shots.csv` had **all statuses blank** after the size round-trip
(the batch statuses were lost when the file was restored) — Fable set the 17 keepers to `done` and cleared the 4.

## 1 · On disk (Fable, dry-run verified: 4 pending, 0 over budget)
| file | change |
|---|---|
| `songs/twinkle-twinkle/shots.csv` | 17 rows `status=done`; T05 seed 4242; T09b/T10/T19 `mode=full`; notes say why |
| `shots/T05.txt` | SHOT excludes door/wall; NEGATIVE adds person/door terms |
| `shots/T09b.txt` | NEGATIVE adds orange/recolour terms |
| `shots/T10.txt` | "one single Minmini"; NEGATIVE adds duplicate/twin/clone |
| `shots/T19.txt` | tail glow "at his back end", "nothing in his hands"; NEGATIVE adds hand lantern/lamp terms |
| `songs/twinkle-twinkle/REVIEW-480p-2026-09-23.md` | the review |

## 2 · Steps
1. `python comfy\batch_runner.py --song songs\twinkle-twinkle --hosts http://x --dry-run` → exactly 4 pending
   (T05 distilled, T09b/T10/T19 full), no OVER BUDGET.
2. Set the 4 rows' `size` to `832x480` (same one-liner as 4j but only for rows with blank status), `wan-push`.
3. Fresh pod, `pull`, then
   ```
   cd /workspace/wan
   python comfy/batch_runner.py --song songs/twinkle-twinkle --hosts http://127.0.0.1:8188 --seed 30313 \
       --max-minutes 25 --stop-cmd "bash /workspace/pod_bootstrap.sh out-push songs/twinkle-twinkle && runpodctl stop pod $RUNPOD_POD_ID"
   ```
   Expect ~1 + 3×6 min ≈ 20 min on an H100. The four new files overwrite the old ones with the same name
   (T05 gets `-seed4242-`; the old `T05-seed30313-s6.mp4` stays — leave it).
4. Restore `size` to `1280x720` on those 4 rows; **keep the `done` statuses** this time (do not restore the CSV from
   git — edit the cells). Pull `out/`. Report the 4 clips' full paths + strips + wall times + stop-cmd exit code.
5. Commit `songs/twinkle-twinkle/` (CSV, 4 shot files, the review) + this dispatch:
   `twinkle: 480p review — 17 keep, 4 retakes (T05 T09b T10 T19)`.

## 3 · Next
Fable checks the 4; then Arul's decision on the house-colour option; then 720p keepers (4l) — or Row's 480p batch
first if Arul prefers to see both songs blocked before spending on 720p.
