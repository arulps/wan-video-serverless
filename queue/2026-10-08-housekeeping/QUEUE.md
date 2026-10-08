# CC DISPATCH — 2026-10-08 "housekeeping": move stale files to delete folders (on Beast)

**Machine:** Beast (`arulps-beast`). **Repo:** `C:\Projects\opencode\video_image` · **Content:** `C:\Channel Contents\MinMiniKids`
**Executor:** CC (Haiku/Sonnet is fine) · **Manager:** Fable · **Cost:** $0 — file moves and one commit only.

## Why
Arul approved (8 Oct) moving `songs\learning-loops\` to a delete folder. It is an early 29 Sep draft of the Learning Shorts
set (78 prompts, shots.csv, world/style files, 9×16 refs, no renders), superseded by `songs\shorts-learning\`. Also the
stray `.learn_tmp.md` left in the Butterfly `_rev2\` folder. Arul empties the delete folders himself.

## Hard limits
- **Move, never delete.** No `rm`, `Remove-Item`, `git rm`, `git clean`. Use `Move-Item`.
- Don't touch anything else: not `songs\shorts-learning\`, not `songs\a07-butterfly\` (a 4K upscale may still be running
  there in its own window — leave that window alone), not the `queue\2026-10-07-beast-4k\` files.
- If `git ls-files songs/learning-loops` lists **any** file (i.e. it is tracked, not untracked as expected) → stop → blocked.
- If a destination already exists, add a suffix `-2` (don't merge or overwrite).
- No commits of `.env`, `tools/`, `out*/`, videos. Commit carries `[skip ci]`.

## Protocol
Use `queue\2026-10-08-housekeeping\` (this file is `QUEUE.md`); keep `LOG.md`, `item-N.report.md`, `item-N.done` /
`item-N.blocked` as in earlier queues. Run from the repo root. When finished: `QUEUE END <time>` and tell Arul
"housekeeping done — ask Fable to review queue\2026-10-08-housekeeping".

---

## item-01 — move `songs\learning-loops\` to the repo's delete folder
1. `git ls-files songs/learning-loops` → must print nothing (else blocked). Record `git status --short` before.
2. Record the file count and total size of `songs\learning-loops\` (expect ~100 files, ~3 MB).
3. Create `C:\Projects\opencode\video_image\_to_delete\` if missing, then
   `Move-Item songs\learning-loops _to_delete\learning-loops`.
4. Add to `.gitignore` (after the `tools/` block):
   ```
   # Arul's delete folder — reviewed, waiting for him to empty it; never committed
   _to_delete/
   ```
5. Check: `songs\learning-loops` no longer exists; `_to_delete\learning-loops` has the same file count and size;
   `git status --short` no longer lists `songs/learning-loops/` and lists nothing under `_to_delete/`.
**item-01.report.md:** before/after `git status --short`, counts and sizes, the `.gitignore` diff.

## item-02 — move the stray Butterfly temp file
1. Move `C:\Channel Contents\MinMiniKids\songs\A07-Butterfly\_rev2\.learn_tmp.md` →
   `C:\Channel Contents\MinMiniKids\_to_delete\A07-Butterfly-_rev2-.learn_tmp.md` (folder already exists).
2. Check the source is gone and the destination exists with the same size (13,519 bytes).
**item-02.report.md:** source/destination paths and sizes.

## item-03 — commit
Commit `.gitignore` and `queue/2026-10-08-housekeeping/` with message
`housekeeping: move learning-loops draft to _to_delete, ignore _to_delete/ [skip ci]` and push.
Nothing else is staged (check `git diff --cached --name-only` before committing; the pre-existing modified
`songs/shorts-learning/REVIEW-learning-batch1-2026-09-29.md` stays **unstaged**).
**item-03.report.md:** commit hash, `git diff --cached --name-only` output, push result.
