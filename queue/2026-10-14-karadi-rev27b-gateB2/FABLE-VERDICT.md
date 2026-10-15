# FABLE VERDICT — A12 Karadi Mama, Gate B2 (rev 2.3): CAa + CQb at 6 s, CQa trim

**Fable, 14 Oct 2026, 21:50 Toronto.** Queue `C:\Projects\opencode\video_image\queue\2026-10-14-karadi-rev27b-gateB2\` (CC 21:05–21:13,
$1.20, commit `472671a`). A12: **$22.70 list of $29.50.**

**Result: both pass (CAa after a $0 splice). The batch `queue\2026-10-14-karadi-rev28-batch\` is released.**

| Clip | Verdict | What the frames show |
|---|---|---|
| CQb, 6 s (the pacing test) | **PASS, no trim** | One shot. All five in frame from frame 0; parents clapping; Appa's daypack and the valley view both read. **All eight moves land inside the slot (f12–173) and on the count:** bear paws sway f18–90 (counts 1–4), hand over the eyes f99–117 (counts 5–6), palms up f135–153 (count 7), point f162–171 (count 8). Nothing was dropped. **6 s works:** Wan still fills the clip, but the clip is now the slot. |
| CAa, 6 s (retake) | **PASS with a $0 splice** | No morph: Amma stays Amma and Appa stays Appa from f21 to the end. Gestures: he lifts the basket arm f54–99, the children point f81–108, everyone walks toward the camera from f144. **But the parents ghost in over f0–20** (`CAa-opening-ghost.png`), and the slot plays from f12. Splice `out\CAa-seed30313-w3-splice.mp4`: f21 held over f0–11 (never played), then f21–179 slowed ×1.07 over f12–179. Same 180 frames and same slips. `make_cutplan.py` points CAa at the splice (`SPLICE` map). Checked: parents in every played frame, gestures intact. |
| CQa at slip 1.9 | **PASS** | `_cuts\_gateB2\CQa-TA-slot14.mp4`: paws on counts 1–3, hand over the eyes on 4–6, palms up on 7, the point starts on 8. |

## Changes before the batch (rev 2.3.1, $0)
- **CAb** (not rendered yet) now opens with the question clips' wording, which kept the parents in frame from frame 0 in all four
  takes (CQ0, CQa, CQb, HKa). Only `shots\10_CAb.raw.txt` changed. Lint 21/0/0; dry-run $6.20.
- The batch item now checks that the splice exists, and that the cut plan uses it for CAa.

## Spend
$22.70 + batch $6.20 = **$28.90 of $29.50.**
