# CC-DISPATCH — wan-video-serverless Phase 3a: make the deploy pipeline unable to regress (2026-09-21)

**Repo:** `C:\Projects\opencode\video_image` → `github.com/arulps/wan-video-serverless`
**Branch:** `main` (HEAD `2f76d58`, the Phase-2b image that produced the first video)
**Executor:** Claude Code on the laptop. **No GPU jobs in this dispatch.** The push triggers one CI
deploy (template + endpoint update + rotation); that is the only RunPod write, and it costs nothing.
**Prepared by:** Fable, after job `13d179ba` produced `outputs\20260921-134106-ti2v-5B-seed30313-81f-20s.mp4`.

---

## 0 · Why

Today's run only succeeded after a manual worker rotation, and the cached-model reference was
never guaranteed across deploys. Three config values the measurements say to change are bundled in
so one deploy carries them all.

## 1 · Changes in the working tree (all written by Cowork, uncommitted)

| file | change | why |
|---|---|---|
| `scripts/deploy.sh` | rotation: scale to 0, then **poll `/health` every 15 s until every worker count is 0** (cap `ROTATE_MAX_WAIT_SEC`, default 420) before restoring min/max; warns and continues if the cap is hit | the fixed 30 s sleep left FlashBoot's warm idle workers serving the old image; the selftest refused, CC rotated by hand |
| `scripts/deploy.sh` | `--model-reference "$MODEL_REF"` passed on **every** endpoint update and on create; value from `endpoint.modelReference` in config or `MODEL_REFERENCE` env | a deploy could otherwise drop the cached model and put the 34 GB billed download back |
| `scripts/deploy.sh` | `--execution-timeout` passed on update (previously only on create) | so the config value below actually reaches the existing endpoint |
| `config/endpoint.json` | `endpoint.modelReference = https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B:main` | same format CC attached by hand today |
| `config/endpoint.json` | `executionTimeoutSec` 1800 → **3600** | measured 18.5 s/step: 50 steps ≈ 15.5 min sampling + 148 s cold load + decode ≈ 20 min at 81 f; 121 f would exceed 30 min |
| `config/endpoint.json` | `containerDiskGb` 200 → **50** | the in-container download path is unused now; image ≈ 10 GB + /tmp outputs |
| `SESSION-HANDOFF-…` §11, `RUNBOOK.md` §9.2 | first-video result, numbers, Phase 3 order | record |

`bash -n scripts/deploy.sh` clean. `config_get.py … --default ''` verified to return empty for a missing key
(so an endpoint config without `modelReference` still deploys).

## 2 · Steps

1. `git status` / `git diff scripts/deploy.sh config/endpoint.json` — confirm the three deploy.sh hunks
   (poll loop, `MODEL_REF_ARGS`, `--execution-timeout` on update) and the three config values.
2. Stage specific files:
   ```
   git add scripts/deploy.sh config/endpoint.json RUNBOOK.md SESSION-HANDOFF-2026-09-21-WAN-SERVERLESS-REVIEW.md CC-DISPATCH-phase2b-2026-09-21.md CC-DISPATCH-phase3a-2026-09-21.md
   ```
   `outputs/` and `logs.txt` stay untracked (the mp4 is a build output, not source).
3. Commit (§4), push, `gh run watch`. **Read the deploy log for these, in order:**
   - `updated endpoint wv9oneserd7vj6 (template 25514mi5ae, model ref https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B:main)`
   - the echoed endpoint JSON shows `executionTimeoutMs: 3600000`
   - the template JSON shows `containerDiskInGb: 50`
   - `drain: workers=N after Ns` lines counting down to `workers=0`, then the restore to `0 / 3`
4. **If the deploy fails on an unsupported flag** (`--execution-timeout` or `--model-reference` on
   `update` — both confirmed in runpodctl ≥ 2.14.0 release notes / README, but not exercised on
   `update` by this project until now): the endpoint is unchanged (no `|| true`, the error is real).
   Paste the error; do not delete/recreate anything. Fallback is to move the flag to a separate
   `runpodctl serverless update` guarded by `|| echo WARNING`.
5. Verify after the deploy, without a job: `runpodctl serverless get wv9oneserd7vj6 -o json` — look for
   the model reference and `executionTimeoutMs`. Optionally `scripts\first_video.ps1 -SelftestOnly`
   (one worker boot, ~$0.02) to confirm `alloc_conf` and `runpod_cached_snapshot` on a fresh worker.

## 3 · Not in this dispatch (Phase 3b, needs Arul's decisions)

- **Object storage.** Pick S3 or Cloudflare R2 and create the bucket + key; then set
  `TPL_ENV_S3_BUCKET`, `TPL_ENV_S3_ENDPOINT_URL` (R2), `TPL_ENV_AWS_REGION`, `TPL_ENV_AWS_ACCESS_KEY_ID`,
  `TPL_ENV_AWS_SECRET_ACCESS_KEY` as GitHub Actions secrets. The code path is already live; production
  should keep the raw quality-8 file, not the crf-23 review copy.
- **Production step count / frames.** Run seed 30313 at 20 / 30 / 40 / 50 steps (same prompt) and
  pick by eye; ≈ 18.5 s per step at 81 f. Then set `DEFAULT_TASK`-side defaults.
- **GPU priority list** (`gpuTypeIds`: 4090 first, L40S fallback) — capacity only; memory is solved.
- **Batching**: submit a song's clips within one 300 s idle window so the 148 s pipeline load is paid once;
  `workersMax 3` = three clips in parallel.

## 4 · Suggested commit

```
deploy: drain workers until /health reports 0, keep model reference across deploys, 3600 s timeout

The 30 s post-scale sleep did not retire FlashBoot's warm idle workers, so a
deploy could leave old-image workers serving (seen 2026-09-21: selftest on a
stale worker, manual rotation needed). Poll /health until every worker count
is 0 before restoring min/max. Pass --model-reference on every update/create
from config so the cached Wan2.2-TI2V-5B model can never be dropped by a
deploy, and pass --execution-timeout on update. Config: executionTimeoutSec
3600 (measured 18.5 s/step on a 4090), containerDiskGb 50 (download path
unused with the cached model), modelReference set. Record the first video.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01K74qgLLkw1m2TCrreoB84E
```
