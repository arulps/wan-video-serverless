# opencode task: deploy Wan 2.2 serverless video endpoint

Project root: `C:\Projects\opencode\video_image`
Configuration and secrets live in the project's `.env` file. Read it. NEVER print or log any secret value (RUNPOD_API_KEY, HF_TOKEN, AWS_*).

## Context

A stateless RunPod serverless video-generation endpoint. CI builds the Docker image on GitHub runners, pushes it to GHCR, then deploys a RunPod template + endpoint via `scripts/deploy.sh`. No local Docker, no network volumes, no datacenter binding.

## Steps, in order

1. Verify prerequisites (report results, do not fix silently):
   - `git --version`, `gh auth status` (expect repo + workflow scopes), `py --version`
   - Read `C:\Projects\opencode\video_image\.env` and confirm these are non-empty:
     `RUNPOD_API_KEY`, `TEMPLATE_IMAGE`, `GITHUB_REPO`. If empty, STOP and ask the user to fill them.
2. If the project is not yet a git repo (`git rev-parse --is-inside-work-tree` fails), run:
   - `git init` inside the project root
   - `git add .` (verify `.env` and `__pycache__` are gitignored first)
   - `git commit -m "Wan 2.2 stateless serverless scaffold"`
3. Create and push the GitHub repo (idempotent — skip if it already exists and is synced):
   - `gh repo create <GITHUB_REPO> --private --source . --remote origin --push`
   - If repo already pushed, `git push -u origin main`.
4. Set GitHub Actions secrets from `.env` (idempotent; use `gh secret set`):
   - `RUNPOD_API_KEY` from `.env` -> `RUNPOD_API_KEY`
   - `HF_TOKEN` from `.env` -> `HF_TOKEN` (skip if empty, note it as optional)
5. Trigger the deploy workflow:
   - It auto-runs on push to main. If the push already triggered it, run `gh run list --workflow build-deploy --limit 3`; otherwise `gh workflow run build-deploy`.
6. Watch it: `gh run watch` until both jobs (build, deploy) finish.
7. Extract the serverless ENDPOINT ID from the deploy job log — look for the line
   `Done. Endpoint: wan-video-serverless (<id>)` (`gh run view <run-id> --log | grep "Done. Endpoint"`).
8. Write the endpoint id into `.env` under `WAN_ENDPOINT_ID=` (replace the key's value only).
9. Smoke test from the project root:
   `py client/generate.py --prompt "two anthropomorphic cats in boxing gear fight on a spotlighted stage" --out smoke.mp4`
   - The client auto-loads `.env` from the working directory.
   - Report the job status transitions and confirm `smoke.mp4` was written (size > 0).
10. Summarize: repo URL, workflow run link, endpoint id, GPU pool, and the final
    verified command to generate a video.

## Rules

- Never print or echo secret values; if you must reference them, say "field is set".
- Do not modify code unless a step fails; if a step fails, diagnose from logs and fix minimally, then report.
- If `RUNPOD_API_KEY` or the workflow fails with an auth error, STOP and ask the user to verify `.env` / RunPod account.
- Keep the commit message exactly as specified.