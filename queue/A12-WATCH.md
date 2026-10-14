# A12 WATCH — standing instructions for CC until A12 Karadi Mama is done

**Machine:** Beast. **Repo:** `C:\Projects\opencode\video_image`. **Started:** 2026-10-13 (Fable; replaces `L05-WATCH.md`, which
stopped on `queue\L05-DONE`).
CC runs **one watch cycle** each time it is invoked (every ~10 min via `/loop`). Fable writes the queues; CC runs them.
Fable checks the same folder on its own schedule, reviews finished queues, and writes the next one.

## One watch cycle
1. **Stop check.** If `queue\A12-DONE` exists: append `<time> DONE seen — watcher stopping` to `queue\A12-WATCH-LOG.md`, tell Arul
   "A12 watcher stopped (song done)", and stop the loop. Do nothing else.
2. **Busy check.** If a queue is mid-run (a folder below has `item-N.started` but no matching `.done`/`.blocked`, and its render log
   was written in the last 45 min), do not start anything; append `<time> busy <queue>` and end the cycle.
3. **Find work.** Look at `queue\2026-*-karadi-*` folders sorted by name. (Rev 2.x queues are named `karadi-rev2N-…` so they sort
   after the rev 1.x ones and run in order: `rev20-build` → `rev21-refs` → `rev22-gateA` → … ; each render queue checks its predecessor's
   `item-01.done` in its step 0.) The first runnable one is `2026-10-13-karadi-1-scale-rule`
   (the $0 prerequisite — character sizes in every prompt; it must finish before any A12 render, and gate1's step 0 checks it).
   `queue\2026-10-10-scale-rule` and `queue\2026-10-13-karadi-0-scale-rule` are blocked records — never run them. Pick the **first** one that
   has a `READY` file, has **no** `QUEUE END` line in its `LOG.md`, and has **no** `*.blocked` file.
   - None → append `<time> idle` to `queue\A12-WATCH-LOG.md` and end the cycle. (One line per cycle; this is the heartbeat Fable reads.)
4. **Budget check.** Add up the `est $` of every finished A12 queue (`QUEUE END … est $x` lines in `queue\2026-*-karadi-*\LOG.md`)
   plus the new queue's own cap (`--max-usd` in its items). If the total would pass **$29.50 list** (the song cap: $15 at rev 1.2,
   $17 for the rev 1.5 re-stage, **$29.50 from 13 Oct 23:00 for rev 2.x "the family trek"** — Arul approved the re-plan at 22:18 and
   "let's proceed" at 22:58: 17 new clips $12.20 on top of $15.40 spent, plus a $1.60 retake buffer that is spent only on Fable's ask), write `<queue>\item-01.blocked` with the numbers, tell Arul, append `<time> blocked budget <queue>`,
   and end the cycle. (The scale-rule queues are $0 and do not count.)
5. **Run it.** Append `<time> start <queue>`. Then do exactly what that queue's `QUEUE.md` and `item-NN.md` files say, item by item,
   following its protocol and hard limits (markers, reports, commit). Never change a queue's files except the markers/reports it asks for.
6. **After it ends** (QUEUE END or blocked): append `<time> end <queue> <done|blocked> est $x` and tell Arul in one line
   "<queue> done — Fable will review" (or "blocked: <reason>"). End the cycle. Do **not** start a second queue in the same cycle.

## Hard limits (on top of each queue's own)
- Never write or edit a `QUEUE.md`, `item-NN.md` or `READY` file, and never create a queue — only Fable does.
- Never re-run a failed or blocked item on your own. Never retry a render. A failure is reported, not re-run.
- Song budget **$29.50 list** across all A12 queues (step 4; $15 → $17 → $29.50, Arul 13 Oct). Never touch `.env`, RunPod, other songs, or the song folder in
  `C:\Channel Contents\…` unless a queue item says so.
- Never print `.env` values, API keys, the workspace id or any video URL.
- Move or rename, never delete.
- If anything here conflicts with a queue's own hard limits, the stricter one wins.
