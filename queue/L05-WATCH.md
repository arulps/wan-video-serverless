# L05 WATCH — standing instructions for CC until L05 Urulaikizhangu is done

**Machine:** Beast. **Repo:** `C:\Projects\opencode\video_image`. **Started:** 2026-10-09 (Arul).
CC runs **one watch cycle** each time it is invoked (every ~10 min via `/loop`). Fable writes the queues; CC runs them.
Fable checks the same folder on its own schedule, reviews finished queues, and writes the next one.

## One watch cycle
1. **Stop check.** If `queue\L05-DONE` exists: append `<time> DONE seen — watcher stopping` to `queue\L05-WATCH-LOG.md`, tell Arul
   "L05 watcher stopped (song done)", and stop the loop. Do nothing else.
2. **Busy check.** If a queue is mid-run (a folder below has `item-N.started` but no matching `.done`/`.blocked`, and its render log
   was written in the last 45 min), do not start anything; append `<time> busy <queue>` and end the cycle.
3. **Find work.** Look only at folders `queue\2026-*-urulai-*` (sorted by name). Pick the **first** one that has a `READY` file,
   has **no** `QUEUE END` line in its `LOG.md`, and has **no** `*.blocked` file.
   - None → append `<time> idle` to `queue\L05-WATCH-LOG.md` and end the cycle. (One line per cycle; this is the heartbeat Fable reads.)
4. **Budget check.** Add up the `est $` of every finished L05 queue (`QUEUE END … est $x` lines in `queue\2026-*-urulai-*\LOG.md`)
   plus the new queue's own cap (`--max-usd` in its items). If the total would pass **$18.00 list (raised from $17 by Arul, 9 Oct 15:55, to keep CB)**, write `<queue>\item-01.blocked`
   with the numbers, tell Arul, append `<time> blocked budget <queue>`, and end the cycle.
5. **Run it.** Append `<time> start <queue>`. Then do exactly what that queue's `QUEUE.md` and `item-NN.md` files say, item by item,
   following its protocol and hard limits (markers, reports, commit). Never change a queue's files except the markers/reports it asks for.
6. **After it ends** (QUEUE END or blocked): append `<time> end <queue> <done|blocked> est $x` and tell Arul in one line
   "<queue> done — Fable will review" (or "blocked: <reason>"). End the cycle. Do **not** start a second queue in the same cycle.

## Hard limits (on top of each queue's own)
- Never write or edit a `QUEUE.md`, `item-NN.md` or `READY` file, and never create a queue — only Fable does.
- Never re-run a failed or blocked item on your own. Never retry a render. A failure is reported, not re-run.
- Song budget **$18.00 list (raised from $17 by Arul, 9 Oct 15:55, to keep CB)** across all L05 queues (step 4). Never touch `.env`, RunPod, other songs, or the song folder in
  `C:\Channel Contents\…` unless a queue item says so.
- Never print `.env` values, API keys, the workspace id or any video URL.
- If anything here conflicts with a queue's own hard limits, the stricter one wins.
