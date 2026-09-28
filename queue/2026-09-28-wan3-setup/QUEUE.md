# CC QUEUE — 2026-09-28 "Wan setup": Wan 3.0 via Alibaba Model Studio (engine=wan3), first real test

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (reads this folder
when Arul asks; frame-checks the results). Full technical detail: `CC-DISPATCH-phase6e-wan3-api-2026-09-28.md` (repo
root) — the items below point at its parts; if an item and the dispatch disagree, the item wins.

## Hard limits (no matter what an item says)
- **Total API spend for this queue ≤ $2.10 at list price** (the runner's `--max-usd` enforces it per run). No pod, no GPU.
- No retakes, no extra seeds, no "one more try": only the rows in the item files.
- **Never print, echo, log or paste `.env` values, the API key or the workspace id.** Check them only with the
  `credentials_present()` one-liner (prints True/False). No key or video URL may appear in any report.
- Never touch RunPod (pods, serverless endpoints) in this queue. Never `git restore` / overwrite a `shots.csv`.
- If `.git\index.lock` exists and no git process is running, delete it (stale) before git commands.
- Commits carry `[skip ci]` (the commit touches `scripts/`, which would otherwise redeploy the serverless endpoint).

## Protocol (file markers in `queue\2026-09-28-wan3-setup\`)
1. Wait for `READY` (it exists already when Fable hands this over).
2. Items `item-01.md` → `item-03.md` run **back to back without waiting for a verdict** — this queue has no GPU and
   a hard dollar cap, so the gates are the checks inside each item. For item N:
   - append `[<time>] item-N start` to `LOG.md`;
   - do exactly what the item says; keep every full Windows path you produce;
   - write `item-N.report.md` (contents listed in the item), then create the empty marker `item-N.done`;
   - if a check fails or something is unclear: write what happened into `item-N.report.md`, create `item-N.blocked`,
     append the question to `LOG.md` and **stop the queue** (do not continue to item N+1). Arul/Fable answer in
     `item-N.verdict` (`GO` = continue, `STOP` = end, `REDO` + instructions).
3. After item-03: append `QUEUE END <time> est $<x>` to `LOG.md`, and tell Arul in chat:
   "Wan setup queue done — ask Fable to check queue\2026-09-28-wan3-setup".
4. `LOG.md` is append-only, one timestamped line per event (start / done / blocked / API task submitted / $ so far).
