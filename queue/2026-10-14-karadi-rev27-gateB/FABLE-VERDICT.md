# FABLE VERDICT — A12 Karadi Mama, Gate B (rev 2.7): CQ0, CQa, CAa, I1

**Fable, 14 Oct 2026, 17:35 Toronto.** Queue `C:\Projects\opencode\video_image\queue\2026-10-14-karadi-rev27-gateB\` (CC done 16:57,
$3.10, commit `eed4f0d`). A12 spend: **$21.50 list of the $29.50 cap.** Reviewed from the full-length takes (every 12th frame, then
every 5th/6th frame where it mattered) and the slot cuts in `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_cuts\_gateB\`.

**Result: 3 pass, 1 fail → the batch (`queue\2026-10-14-karadi-rev28-batch\`) is NOT released.** No READY written.

| Clip | Verdict | What the frames show |
|---|---|---|
| I1 long shot | **PASS** | One shot, no cuts. Starts on the whole hill path with four small figures, and the camera glides down and in as the family walks toward us. Appa's daypack reads as a real hiking pack (rolled mat underneath). Amma is in everyday clothes, and there are no caps. TA/EN slot 1 plays f0–172, which is the glide plus the walk-in. |
| CQ0 encounter | **PASS** | One shot. The family is in frame from frame 0, walking. Karadi Mama steps out from the trees at f12–36 (counts 1–2). Mintu points and Minnu's hands fly up at f48–96. He lifts the basket at f60–84 (the hello). Then hand over the eyes ("where?") at f120–140. The palms-up lands at the very end of the slot, and the point is cut. That is acceptable here: the meeting is this clip's job. Parents stay beside the children. Not scary: he smiles and never looms. |
| CQa question | **PASS with a trim** | One shot. The parents clap behind, and the daypack is visible. All four word-actions are there and correct (no tummy pats): bear-paws sway-stomp f12–118, hand over the eyes looking left then right f122–174, palms up with a head tilt f178–206, point down the path f210–239. **But Wan spread the 8 counts over the whole 8 s, not 5.4 s.** At slip 0.4 the slot ends at f173, so the palms and the point are lost. **Measured trim: `USE_FROM["CQa"] = 1.6`** (f48). That gives paws on counts 1–4, "where?" from count 4.6, and palms up from count 7.4 to the end. The point is lost (count 8 has no word). |
| CAa answer | **FAIL** | One shot, but **a parent pops in and morphs**. f0–45: only the children and Karadi Mama, with no parents. **f50: Amma appears from nowhere** behind the children. **f85–100: Amma turns into Appa** in the same place (see `CAa-parent-swap.png`). The rest is good: he lifts the basket arm at f75–110, the children point up the path at f108–156, and they all walk toward the camera from f192. A trim can't save it: the only clean stretch is f100–239 (4.7 s), and the slot needs 5.4 s. CAa plays 4 times (TA 4, TA 16, EN 3, EN 13), so it must be retaken. |

**Slot mapping (my error in the queue):** CQa's own slots are **TA 14 / EN 12**. The cuts to keep are `CQa-TA-slot14.mp4` and
`CQa-EN-slot12.mp4`. TA 8 / EN 7 belong to CQb. CC caught it and cut both pairs.

## The finding that matters for the batch: Wan fills the clip length
CQ0 and CQa both took **the full 8 s** for an 8-count written as a sentence chain. A slot is 5.4 s, so the last third of the
actions falls outside every slot. The same chain is in **CQb, CAb, JOIN and O2** in the batch, and they would come back the same way,
with the actions too slow and the ends cut. That is the pacing problem Arul asked us to fix.
**Fix: render every counted clip at 6 s, not 8 s** (slot 5.4 s + slip 0.4 s + 0.2 s spare). Wan 3.0 accepts 2–30 s, and 3–4 s jobs
already work. The model then has 6 s for the 8 moves, about one move per beat, which is the quick pacing Arul asked for. It is also
cheaper ($0.60, not $0.80). HKa and HKc stay at 8 s, because HKa's turn already lands on the count with its trim and HKc must match it.

## Proposed next step (needs Arul's OK: it is a retake and a plan change)
1. Builder rev 2.3: CQa trim 1.6. CAa retake prompt: "Amma and Appa stand together behind the children **from the first frame to the
   last**, Amma stays Amma and Appa stays Appa". Avoid: "a parent appearing partway, one parent turning into the other". Counted
   clips CQb, CAa, CAb, JOIN and O2 go to 6 s. Then self-test, lint, dry-run, and the director and audience passes.
2. **Gate B2 (≈ $1.20):** CAa and CQb at 6 s. This one gate retakes CAa and also tests the 6 s pacing on the clip that plays 4×.
3. If B2 passes: the batch, less CQb, at the new lengths (≈ $6.00). Spend comes to $21.50 + $1.20 + $6.00 ≈ **$28.70**, inside the $29.50 cap.
   If 6 s does not help, CQb and CAb stay at 8 s with trims like CQa's, and the cap still holds.
