# Fable verdict — gate1b (ZK1 rendered, ZO failed at upload) — 2026-10-09 14:15

## ZK1 — the merge idea works; one rule problem: Brinjal never looks asleep
**Passed**
- Two-beat timing held: 0–2 s Baby Potato climbs in from the left, ~2.3–4.7 s settled beside Brinjal, the nudge starts ~5.3 s
  (f160) — the verse slot starts at f143 (TA/EN), so the action lands on the verse line. **No cut, framing locked** all 10 s.
- **Plain brinjals stay plain** — no faces at 100% (f075, f210). Exactly one Brinjal, one Baby Potato. Both on-model, same height.
- Brinjal at the front of the pile facing camera (rev 1.9 staging works). Clay-toy set and the widened rack read correctly.
- The cry: small pout, sits up at the rim (f224–236) — gentle and funny. No angry face anywhere.

**Failed — Arul's rule ("nobody is mean, everything is an accident")**
- **Brinjal's eyes are open dots in every frame** (f30, 100, 140, 165, 200, 260 — `FABLE-ZK1-brinjal-eyes.jpg`). The prompt asked for
  closed sleeping eyes; the reference image (open dot eyes) wins, as in learnings §2 (refs drive faces and pose). An awake,
  smiling Brinjal that shifts and the baby rolls away reads as "it did that", not "it was asleep".
- The kick reads as a body shift + stub-arm nudge (f158–170), not a leg kick — fine for toddlers, but with open eyes it looks
  deliberate.

**Root cause / fix:** the owners need **sleeping references** (same character, eyes closed as curved lines, peaceful smile). The
owners are asleep in every shot they appear in (Z, K, ZK, ZO), so a sleeping ref simply replaces the awake ref in those shots.

## ZO — not rendered: upload timed out (`<urlopen error The write operation timed out>`, no task id)
10 reference images sent as data URIs ≈ 25 MB of PNG (set 4.6 MB, Carrot 2.7 MB, Amma 2.4 MB…). Fix: send JPEG copies of the refs
(long side ≤ 1536 px, quality 92 → ~2 MB total; Wan does not need 2750 px refs). No re-run until the ref question is settled.
Unknown: whether Alibaba started (and billed) a task for ZO anyway — check the console's usage list for 17:57–18:01 UTC.

## Decision needed from Arul (nothing queued until then)
A) Make 7 sleeping refs in Gemini (prompt in Fable's message) → rebuild → re-run ZK1 + ZO. Recommended.
B) Accept ZK1 as is (open eyes, smiling, never looks at the baby) and keep awake refs for all owners.
