# FABLE VERDICT — A12 Gate A (rev 2.2 → 2.5 queues): HKa + O1 — **both re-render; root cause found and fixed in the builder**

Fable, 14 Oct 2026 09:25. Reviewed on the slot cuts with the music (`_cuts\_gateA\*.mp4`, `gateA-slots.png`) and every 4th frame
(`out\_qc\HKa-every4-all.png`, `O1-every4-all.png`), plus a 2-frame strip of HKa's turn (f48–76).

## What worked
- **The quick turn itself.** HKa f52–76: one full 360° in ~0.8 s (24 frames), round belly leading, lands facing the camera — the quick
  move Arul asked for. Stick stays on the right shoulder, basket in the left paw, honeycomb stays on the stick, no morphing.
- **The plates.** HKa's forest path = `11-set-path-low` (same trees, sunbeams, path curve); O1's hut under the big tree = `13-set-home`.
- **Appa's daypack** reads as a trekking pack (straps, bottle), on him only. Faces on-model; the children's head tops level.
- O1's action is right: berries into cupped hands, the rabbit and squirrel nibbling, everyone laughing.

## Why both fail
1. **Each clip came back as three shots.** HKa: hard cuts at f94 (3.1 s) and f134 (4.5 s) — wide → closer → wide with the parents.
   O1: a dissolve f80–92 and a hard cut at f134 — wide → close-up of the children and animals (no bear) → group. Our prompts said
   "one continuous take … never cuts", but the beat tables were written into the prompt as **"from about 0.4 to 1.1 seconds, …; from
   about 1.1 to 2.4 seconds, …"** — that is Wan 3.0's *multi-shot storyboard* format (the wan3.0 prompt guide: "Shot 1 [0-3s] …",
   "[00:00-00:03] …"). The model did what the format asks. (Rev 1.x prompts had no time ranges and stayed single shots.)
2. **Amma and Appa are missing for the first 4.5 s of both** — they only appear in the last shot. In a single shot the "everyone in
   frame from the first frame" line held before; the storyboard split overrode it.
3. **HKa: the children don't dance.** They stand at the left watching while he turns. The prompt had them "ready to copy him" at the
   side — a spectator position. Arul's rule is that the kids dance it *with* him.
4. Neither clip's key window survives in its slot (cut mid-move, parents popping in) — the KEY check assumed one shot.

## Fix (builder rev 2.2, verified: self-test OK, LINT PASS 21/0/0, dry-run $12.20, kept verse answers byte-identical, cut plan no gaps)
- Every new clip: line 2 (right after the image legend; lint needs the legend first) = **"Generate single shot. One continuous shot
  from the first frame to the last: no cuts throughout, no shot splits, no scene changes, no close-up inserts, no dissolves — the
  same camera position and framing the whole time."** (the guide's own wording), and Avoid adds "frequent shot cuts, shot splits, a
  second shot, a close-up insert or a dissolve".
- The beat tables now become **one sentence chain with no times** ("First … Then … Right after that … Next … Finally …", "one move per
  musical beat"). The tables still drive the KEY windows and trims; the timing is set after the render with USE_FROM, as planned.
- HKa: **the three of them dance together, side by side in one row facing the camera** (Mintu left, Minnu right), all three spin at
  the same moment; Amma and Appa a step behind, clapping.
- All 17 new prompts get this (they all used the time-range form) — nothing else in the batch is rendered yet, so nothing is lost.

## Retake (needs Arul's OK — from the $1.60 buffer)
HKa $0.80 + O1 $0.70 = **$1.50**. Spend so far $16.90; after the retake $18.40 of the $29.50 cap; the plan total becomes $29.10
(the buffer is then used up — later retakes would need a new OK).
Optional: O1's three-shot version is a usable little story on its own (hand-out → close-up eating → group) — if Arul likes it, keep it
($0) and accept the parents appearing late in the finale, and re-render HKa only ($0.80).

Learning → `WAN3-PRODUCTION-LEARNINGS.md` §15: never write time ranges into a Wan 3.0 prompt you want as one shot.
