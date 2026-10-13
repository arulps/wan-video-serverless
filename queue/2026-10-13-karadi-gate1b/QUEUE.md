# CC QUEUE — 2026-10-13 "Karadi gate 1b": A12 Karadi Mama rev 1.3 — CAa + CQa (first Wan render of the song)

**Re-issue of `queue\2026-10-13-karadi-gate1`** (blocked 13 Oct ~13:05 at item-01 step 5, $0: the runner rejected the cast key
`the-rabbit` — `batch_runner.py` LOCK_NAME_RE only accepts keys starting with a capital). Builder **rev 1.3** writes the cast keys
`Rabbit` and `Squirrel` in `shots.csv` and `characters.txt` (and asserts every key against the runner's pattern). Prompts, refs,
labels and durations are byte-identical to rev 1.2. Fable ran the real runner's `--dry-run` on a mirror of the folder this time:
all 18 rows assemble, $12.40; CAa + CQa = $1.60. The gate1 folder is kept as the record — never run it.

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast (`arulps-beast`) · **Executor:** CC (Sonnet is fine) ·
**Manager:** Fable (frame-checks after).
Song folder `songs\a12-karadi-w3\` (built 13 Oct by `_gen\build_karadi_runsheet.py` rev 1.3 from
`C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\`; 18 clips, 124 s, $12.40 list, cap $15 for the song).
Rev 1.2 (Arul's review, 13 Oct): the six re-used clips (CQa/CQb, CAa/CAb, HKa/HKb) are **8 s** (was 7 — at slip 1.6 a 7 s clip left
one frame spare); V1A keeps the basket in his paw; V4A joins Gate 2. Fable's checks on the rebuilt folder: **LINT PASS 18/0/0**,
`test_prompt_lint` PASS, every re-used slot ≥ 1.0 s spare.
This gate tests the two riskiest ideas before any batch: **CAa (8 s, Karadi Mama's spin-and-skip with the honeycomb stick and
basket — the hardest motion in the song) and CQa (8 s, Mintu, Minnu, the rabbit and the squirrel doing the bear walk, Amma and Appa
behind; first SIZES-line render with both children — Fable measures the head tops) = 16 s, $1.60 list.**

## Hard limits
- **API spend ≤ $1.70 at list price.** Only `CAa,CQa`. No pod, no GPU, no upscale. A failure is reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`. Never commit `.env`, `logs.txt`, `nil`, `out/`, `tools/`,
  `_to_delete/`.
- Do **not** write anything into `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\`. Do not touch other songs.
- Do not edit generated files (`shots\*.raw.txt`, `shots.csv`, `lint.json`, `scale.json`, `world.txt`, `characters.txt`, `refs\send\*`)
  or the runner. Move or rename, never delete.

## Protocol (markers in `queue\2026-10-13-karadi-gate1b\`)
As before: `LOG.md` start/done lines, `item-N.report.md`, `item-N.done`, or `item-N.blocked` + stop.
After item-01: `QUEUE END <time> est $<x>`, tell Arul "Karadi gate 1b done — Fable will review queue\2026-10-13-karadi-gate1b".
