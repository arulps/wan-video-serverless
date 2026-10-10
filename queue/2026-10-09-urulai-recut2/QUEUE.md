# CC QUEUE — 2026-10-09 "Urulai recut2": I1 intro splice, TA/EN 1080p re-cut, then the 4K master (no API spend, no renames)

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.

This replaces `queue\2026-10-09-urulai-recut1`, which was blocked at 21:26: the session guard refused the rename step. This queue
renames, moves and deletes **nothing**. Every output gets a new name instead:
- the 1080p cuts are written with tag `ROUGH2`, beside the untouched `ROUGH` ones;
- the cuts read the clips straight from `out\` (`--src out`), so nothing is re-staged in the song folder.

Content is unchanged from recut1: Arul approved the I1 intro splice (21:20).
- `out\I1-seed30313-w3-splice.mp4` is already on Beast: 295 frames, 9.83 s.
- `_gen\make_cutplan.py` rev 2 points the I1 slot at the splice.
- Fable tested 480p previews: TA 4448 and EN 4452 frames, no held frames.

Then the 4K master runs, tag `V1-4K`: about 1 h, in its own PowerShell window.

## Hard limits
- No API calls, no Wan renders, no pod. The only upscale is item-02 (Real-ESRGAN, local, $0). Never print `.env` values, keys, the
  workspace id or any URL.
- **No `mv`, `rm`, rename, move or delete of any existing file**, by any tool. Only create new files.
- Song folder: create only new files in `_cuts\`.
- Repo: change only `songs\l05-urulai-w3\cutplan.json` (and, in item-03, one `.gitignore` line). Commits carry `[skip ci]`;
  never commit `out/`, `out_4k/`.

## Protocol (markers in `queue\2026-10-09-urulai-recut2\`)
As before.
- After item-01, tell Arul "Urulai 1080p re-cut done (ROUGH2)".
- After item-03: `QUEUE END <time> est $0.00`, then tell Arul "Urulai 4K done — ask Fable to review queue\2026-10-09-urulai-recut2".
