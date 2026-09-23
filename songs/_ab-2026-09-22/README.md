# A/B test rows for the two failed blocking shots (2026-09-22) — 832x480, cheap

Rows point at the real song files (shots, worlds, negatives, refs) via relative paths; only cast/ref/steps/cfg/seed
differ. Run: `python comfy/batch_runner.py --song songs/_ab-2026-09-22 --hosts <pod> --seed 30313`.
T09a: the 4-step/cfg-1 clip blinked with both eyes and opened its mouth (negatives are ignored at cfg 1.0).
S03: the two children merged into one (Minnu's pigtails + Mintu's shirt); prompt now binds each child by outfit and
position, and one sheet puts Appa between the two children.
