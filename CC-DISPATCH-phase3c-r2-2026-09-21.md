# CC-DISPATCH — Phase 3c: wire Cloudflare R2 output storage (2026-09-21)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** Claude Code on the laptop.
**Cost:** one CI deploy (no rebuild — only the template env changes) + one selftest (~$0.02).
**Secrets rule:** read values from `.env`, never print, echo, log or commit them. `.env` is gitignored;
confirm it stays untracked (`git status` must not list it).

Arul has created the R2 bucket + token and put the values in `.env`. The worker code has supported an
S3-compatible endpoint since Phase 2 (`app/storage.py`: `S3_ENDPOINT_URL`, `AWS_REGION=auto`,
presigned URLs, `ContentType=video/mp4`); nothing in `app/` changes.

## 1 · Read the five values from `.env`

Accept either naming — Arul may have used the `.env.example` names or the `TPL_ENV_` names:

| template env var (what the worker reads) | `.env` key, either of |
|---|---|
| `S3_BUCKET` | `S3_BUCKET` / `TPL_ENV_S3_BUCKET` |
| `S3_ENDPOINT_URL` | `S3_ENDPOINT_URL` / `TPL_ENV_S3_ENDPOINT_URL` / `R2_ENDPOINT` |
| `AWS_REGION` | `AWS_REGION` / `TPL_ENV_AWS_REGION` (R2 wants `auto`; if empty, use `auto`) |
| `AWS_ACCESS_KEY_ID` | `AWS_ACCESS_KEY_ID` / `TPL_ENV_AWS_ACCESS_KEY_ID` / `R2_ACCESS_KEY_ID` |
| `AWS_SECRET_ACCESS_KEY` | `AWS_SECRET_ACCESS_KEY` / `TPL_ENV_AWS_SECRET_ACCESS_KEY` / `R2_SECRET_ACCESS_KEY` |

Sanity checks (report pass/fail, not values): endpoint URL starts with `https://` and contains
`.r2.cloudflarestorage.com`; bucket name is lowercase with no spaces; both keys non-empty
(R2 access key ids are 32 hex chars, secrets 64). Do NOT put the S3 API URL in
`S3_PUBLIC_BASE_URL` — leave that unset (presigned URLs are used).

## 2 · GitHub Actions secrets (values piped from `.env`, never typed)

PowerShell, from the repo root — reads each value and pipes it to `gh secret set` on stdin:
```powershell
$envl = Get-Content .env
function V($names) { foreach ($n in $names) { $l = $envl | ? { $_ -match "^\s*$n=" } | select -First 1; if ($l) { return (($l -split '=',2)[1]).Trim().Trim('"').Trim("'") } }; return $null }
$region = V @('AWS_REGION','TPL_ENV_AWS_REGION'); if (-not $region) { $region = 'auto' }
$map = @{
  TPL_ENV_S3_BUCKET             = V @('S3_BUCKET','TPL_ENV_S3_BUCKET')
  TPL_ENV_S3_ENDPOINT_URL       = V @('S3_ENDPOINT_URL','TPL_ENV_S3_ENDPOINT_URL','R2_ENDPOINT')
  TPL_ENV_AWS_REGION            = $region
  TPL_ENV_AWS_ACCESS_KEY_ID     = V @('AWS_ACCESS_KEY_ID','TPL_ENV_AWS_ACCESS_KEY_ID','R2_ACCESS_KEY_ID')
  TPL_ENV_AWS_SECRET_ACCESS_KEY = V @('AWS_SECRET_ACCESS_KEY','TPL_ENV_AWS_SECRET_ACCESS_KEY','R2_SECRET_ACCESS_KEY')
}
foreach ($k in $map.Keys) { if (-not $map[$k]) { throw "missing $k in .env" }; $map[$k] | gh secret set $k; "set $k (len $($map[$k].Length))" }
```

## 3 · Workflow (protected path — apply by hand)

In `.github/workflows/deploy.yml`, deploy job → step **Upsert template and endpoint** → `env:`,
add after `TPL_ENV_HF_TOKEN`:
```yaml
          TPL_ENV_S3_BUCKET: ${{ secrets.TPL_ENV_S3_BUCKET }}
          TPL_ENV_S3_ENDPOINT_URL: ${{ secrets.TPL_ENV_S3_ENDPOINT_URL }}
          TPL_ENV_AWS_REGION: ${{ secrets.TPL_ENV_AWS_REGION }}
          TPL_ENV_AWS_ACCESS_KEY_ID: ${{ secrets.TPL_ENV_AWS_ACCESS_KEY_ID }}
          TPL_ENV_AWS_SECRET_ACCESS_KEY: ${{ secrets.TPL_ENV_AWS_SECRET_ACCESS_KEY }}
```
`deploy.sh` already forwards every non-empty `TPL_ENV_*` into the template env (the Python block
near the top), so nothing else changes.

## 4 · Commit, push, verify

```
git add .github/workflows/deploy.yml CC-DISPATCH-phase3c-r2-2026-09-21.md
git commit -m "ci: pass R2 object-storage settings into the worker template env" ; git push
gh run watch
```
Deploy log: the template JSON's `env` now lists `S3_BUCKET`, `S3_ENDPOINT_URL`, `AWS_REGION` — the
key/secret values are masked as `***` by Actions; if any appear in clear, stop and report.
Then: `powershell -ExecutionPolicy Bypass -File scripts\first_video.ps1 -SelftestOnly` → the
selftest's `output.s3_bucket_set` and `s3_endpoint_url_set` must both be `true`.

**Do not run this deploy while a ladder is in flight** — the rotation drains workers and would kill it.

## 5 · What changes for every job from now on

- The result carries `"delivery": "s3"` and `"video": "<presigned URL, 24 h>"` pointing at the **raw
  quality-8 master** (`wan-video/<tmpname>.mp4` in the bucket, or the `output_key` the caller sets).
  No re-encode, no 10 MB cap. `first_video.ps1` and `step_ladder.ps1` download from the URL automatically.
- Suggested `output_key` convention for production: `songs/<song>/<shot>/<seed>-<steps>s.mp4` — pass it
  in the job input; the scripts don't set it yet (Phase 4 item).
- If the upload fails (bad key, wrong endpoint), the job **fails** with the boto3 error in `error` rather
  than silently falling back — intentional, so a misconfiguration can't hide.
- If any of the five values is later blanked, `deploy.sh` simply omits it and the worker returns to inline
  delivery — the selftest shows `s3_bucket_set: false`.
