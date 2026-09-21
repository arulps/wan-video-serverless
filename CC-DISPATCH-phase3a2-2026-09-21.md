# CC-DISPATCH — Phase 3a.2: execution timeout via REST PATCH (2026-09-21)

**Repo:** `C:\Projects\opencode\video_image` · **HEAD:** `f1ea752` · **No GPU jobs.** One CI deploy.
**Decision taken (Fable):** put the timeout in `deploy.sh` via the REST API, not the console — a
console-only value is invisible to the repo and drifts.

## What changed (working tree, uncommitted)

| file | change |
|---|---|
| `scripts/deploy.sh` | after the runpodctl update: `PATCH https://rest.runpod.io/v1/endpoints/$EP_ID` with `{"executionTimeoutMs": <config·1000>, "gpuTypeIds": [...]}`. Method, URL and field names verified on docs.runpod.io/api-reference (`EndpointUpdateInput`). Non-2xx → `exit 1` with the response body printed, so a silent miss like today's is impossible. `gpuTypeIds` comes from `endpoint.gpuTypeIds` (priority list) or falls back to the single `gpuId`. |
| `config/endpoint.json` | `gpuTypeIds: ["NVIDIA GeForce RTX 4090"]` made explicit (same GPU as today; append `"NVIDIA L40S"` later for a 48 GB fallback — Arul's call, it changes $/s). |

`bash -n` clean; body construction and the empty-key fallback exercised offline.

## Steps
1. `git diff scripts/deploy.sh config/endpoint.json` — one new block after `updated endpoint …`, one new key.
2. `git add scripts/deploy.sh config/endpoint.json CC-DISPATCH-phase3a2-2026-09-21.md` · commit (below) · push · `gh run watch`.
3. In the deploy log confirm, in order: `== REST PATCH endpoint wv9oneserd7vj6: {"executionTimeoutMs": 3600000, …}`,
   a `HTTP 200` line, `endpoint PATCH applied`, then the drain countdown and restore to `0 / 3`.
4. `runpodctl serverless get wv9oneserd7vj6 -o json` → `executionTimeoutMs: 3600000`, `modelReferences` still present.
5. If the PATCH returns 4xx: paste the body. Likely causes are a field-name mismatch (the docs say
   `executionTimeoutMs`) or the key lacking REST scope; the endpoint is otherwise unchanged. Do not
   fall back to the console silently — report first.

## Commit
```
deploy: set execution timeout and GPU list via REST PATCH (runpodctl update lacks the flags)

runpodctl 2.14.0 `serverless update` has no --execution-timeout (CI run
35636080696 failed on it), so executionTimeoutSec never reached the live
endpoint. After the CLI update, PATCH rest.runpod.io/v1/endpoints/{id} with
executionTimeoutMs and gpuTypeIds from config; fail the deploy on non-2xx.
Make gpuTypeIds explicit in config (single 4090 today).

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01K74qgLLkw1m2TCrreoB84E
```

## Also: the optional `-SelftestOnly` (~$0.02)
Yes, run it once after this deploy. It is the only way to confirm a *fresh* worker shows
`alloc_conf=expandable_segments:True` and `runpod_cached_snapshot` on the post-3a template — and it
exercises the new drain logic end to end. Report the two fields.
