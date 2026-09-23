# CC QUEUE — overnight 2026-09-23 (multi-reference test: VACE separate refs → Phantom-14B)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC · **Manager:** Fable (polls this folder every ~20 min, frame-checks, writes verdicts).
Arul is asleep. Nobody will answer questions — when something is unclear, write the question into `LOG.md`,
mark the item `blocked` (see protocol) and wait; Fable answers in the verdict file.

## Hard limits (do not exceed, no matter what an item says)
- **Total GPU spend for this whole queue ≤ $6.** Track it in `LOG.md` after every pod stop (pod minutes × hourly rate).
- **One pod at a time, stopped (not just idle) before you wait for any verdict.** Never leave a pod running while waiting.
- No retakes, no extra seeds, no "one more try" — every GPU run must be written in an item file.
- Never touch the serverless endpoints, never delete/recreate anything on RunPod; `runpodctl stop pod` / `remove pod` for pods you created in this queue only.
- Never print `.env` values. R2 keys reach a pod only as console env vars, as in phase 4e–4j.
- Never `git restore` / overwrite `shots.csv`; edit cells only. No commits in this queue unless an item says so.

## Protocol (file markers in this folder — `queue/2026-09-23/`)
1. Wait for `READY` to exist (Fable is still writing the items). Poll:
   `powershell -c "while (-not (Test-Path READY)) { Start-Sleep 30 }"` (run from this folder; re-run if a shell timeout cuts it).
2. Items are `item-01.md`, `item-02.md`, … in order. For item N:
   - append `[<time>] item-N start` to `LOG.md`;
   - do exactly what the item says; keep every full Windows path of every mp4/strip/json you produce;
   - write `item-N.report.md` (the item says what it must contain), then create the empty marker `item-N.done`;
   - if you cannot finish, write what happened to `item-N.report.md` and create `item-N.blocked` instead;
   - **stop the pod** (and confirm it is stopped) before the next step;
   - wait for `item-N.verdict` to appear (same poll loop, file name `item-N.verdict`) — Fable writes it. First line is
     `GO` (continue to item N+1), `STOP` (end the queue, write a final summary to `LOG.md`, exit), or `REDO` followed by
     instructions (do them, then rewrite the report and re-create `item-N.done`; delete the old `item-N.verdict` first).
3. When there is no `item-(N+1).md` after a `GO`, or after `STOP`: append `QUEUE END <time> total $<x>` to `LOG.md` and exit.
4. `LOG.md` is append-only, one timestamped line per event (start/done/blocked/pod start/pod stop/$ so far). Fable reads it.

## Notes
- `.git\index.lock` (0 bytes, 05:26) is a stale lock left by Fable's sandbox `git status` — **delete it first**
  (`del .git\index.lock` from the repo root) if any git command complains; no commit is part of this queue anyway.
- Items: `item-01.md` (VACE separate refs, ~$1.75 cap), `item-02.md` (Phantom-14B, ~$2.35 cap). Everything else is on disk and
  dry-run verified; step 1 of item 1 re-verifies it on this machine.
