# CC QUEUE — 2026-10-10 "scale rule": character sizes and builds in every video prompt + Priya's height in the Oviyan canon

**Machine:** Beast. **Repos:**
- `C:\Projects\opencode\video_image` for item-01.
- `C:\Projects\oviyan` for item-02.

**Executor:** CC (Sonnet is fine). **Manager:** Fable.
**Spend: $0.** This queue does no rendering and makes no API calls.

## Why
In L05, Minnu came out about half a head shorter than Mintu (I1 close shot, O2). In canon they are level: Mintu 1.00 m, Minnu
1.02 m. Arul's rule (9 Oct): **every character's physical dimensions and characteristics are passed to the video, from a table
of all character heights.**

Arul's canon rulings (9–10 Oct):
- **Priya** is the same height as Minnu, 1.02 m (was 1.15 m). The bible is updated to v62.
- **Minmini** (10 Oct): a small flier, about a child's hand, in most scenes; up to 0.50 m (half a child's height) only when
  perched, still or close up.
- **Chiku** (10 Oct): no bigger than a child's hand (~0.10 m, was 0.5 m).

Both Minmini and Chiku are corrected in non-human bible v26.

## What Fable already wrote on Beast (do not edit; verify and commit)
**video_image, new files:**
- `comfy/character_scale.json`: the canon, 91 characters.
- `comfy/scale_line.py`: prints the SIZES line for a shot (`--mode Minmini=perched` for still or close-up shots) and generates
  the table.
- `docs/CHARACTER-SCALE.md`: the table, generated.
- `songs/l05-urulai-w3/scale.json` and `songs/a07-butterfly/scale.json`: song-only characters.

**video_image, changed files:**
- `comfy/prompt_lint.py`: new rules R9 (the SIZES line must be in the prompt) and R10 (lock-line ages must match canon).
- `tests/test_prompt_lint.py`: cases for R9 and R10.
- `docs/PROMPT-PLAYBOOK.md`: §8 Minnu 6–8 → 5–6, and a new §9.
- `characters.txt` in `songs/row-row-row-your-boat`, `songs/shorts-learning`, `songs/shorts-loops`, `songs/twinkle-twinkle` and
  `songs/_selftest`:
  stale ages fixed (Minnu 6-8 → 5-6, Thatha 70s → 65-70, Paati 70s → 63-68, Kollu-Thatha 90s → 88-92).

**oviyan, changed files** (Priya 1.15 → 1.02):
- `docs/CHARACTER-HEIGHTS.md`;
- `src/data/characterCanon.ts`;
- `src/engine/__tests__/characterCanon.test.ts`.

**Outside git** (already in place; nothing to do):
- `C:\Channel Contents\MinMiniKids\charecter bible\minimini_full_bible_v62.html`;
- `minmini_nonhuman_bible_v26.html` and `NONHUMAN-BIBLE-V26-CHANGES-2026-10-10.md` (same folder);
- `HUMAN-BIBLE-V62-CHANGES-2026-10-10.md`;
- `WAN3-PRODUCTION-LEARNINGS.md` v3.4.

## Hard limits
- No renders, no API calls, no pod, no GPU.
- Never print `.env` values, API keys, the workspace id or any video URL. Never touch RunPod.
- Commit **only** the files each item lists; other threads may have uncommitted work in either repo. `git add` by explicit path,
  never `git add -A` or `.`.
- In video_image, commits carry `[skip ci]`. In oviyan, follow `docs\DISPATCH-CONVENTIONS.md` for the commit message.
- Move or rename, never delete. Don't edit Fable's files. If a check fails, write `item-N.blocked` with the output and stop.
- Never touch the Oviyan database or vault in this queue. Priya's vault height is Arul's UI step.

## Protocol (markers in `queue\2026-10-10-scale-rule\`)
- `LOG.md` gets the start and done lines.
- Each item writes `item-N.report.md`, then `item-N.done` on success, or `item-N.blocked` and stops.
- After item-02, add `QUEUE END <time> est $0`, then tell Arul: "scale rule committed — ask Fable to review
  queue\2026-10-10-scale-rule".
