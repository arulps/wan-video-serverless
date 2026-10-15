# item-01 report — DONE: all 10 batch clips rendered ($6.20), no scene cuts found in any, sheets

Run by CC (A12 watcher), 2026-10-14 21:51–22:49 Toronto. Repo `C:\Projects\opencode\video_image`, branch `main`.
One render run, no retries. The clips were not judged.

## Step 0
`queue\2026-10-14-karadi-rev27b-gateB2\item-01.done` exists. OK. (Gate B2's `FABLE-VERDICT.md` is in place.)

## Step 1 — rebuild (repo path quoted)
```
ok 21 clips 136 s $13.60 list $16.30 w/ reserve slots TA 29 EN 24 set image
SELFTEST OK: place, facing, word-action, pacing, camera rules all refuse a bad clip
```
- Lint → `LINT PASS: 21 shots, 0 fail, 0 warn`
- Status: `done` = I1 CQ0 CQa CQb HKa CAa V1A V2A V3A V4A O1 (the 11); `todo` = HKc HKb JOIN CAb V1Q V2Q V3Q V4Q O2 O3 (the 10). OK.
- `git diff --stat songs/a12-karadi-w3/shots` → `songs/a12-karadi-w3/shots/10_CAb.raw.txt | 2 +-` — only CAb. OK.
- `out\CAa-seed30313-w3-splice.mp4` exists: 4,181,613 bytes, `6.000000,180` (180 frames, 6.000 s). OK.

## Step 2 — rev 1.x leftovers renamed (`mv -n`, nothing deleted, no collisions)
No batch ID had an `.mp4` at the top of `out\` (the rev 1.x takes are in `out\_rev1x-2026-10-13\`). Their **sidecars** were, and their
**QC sheets** were in `out\_qc\` under the plain names; as in gates B and B2, CC renamed them with `-v1-picnic` so nothing would be
overwritten:
- sidecars (8): `HKb`, `CAb`, `V1Q`, `V2Q`, `V3Q`, `V4Q`, `O2`, `O3` `-seed30313-w3.json` → `…-seed30313-w3-v1-picnic.json`
- `out\_qc\` (82 files): every `HKb-`, `CAb-`, `V1Q-`, `V2Q-`, `V3Q-`, `V4Q-`, `O2-`, `O3-*.png` without `-v1-` → `<name>-v1-picnic.png`
  (contact, every4-all, every4-first2s where present, f000…f150, last frame, strip). HKc and JOIN had none.

## Step 3
- `py tests\test_wan3_retry_mock.py` → `PASS test_wan3_retry_mock: 10 checks`
- Credentials check → `credentials present: True`

## Step 4 — dry-run
10 rows, all `720P 16:9 audio=off`; no `ERROR` / `MISSING` / `OVER BUDGET` / `Traceback`:

| row | length | refs | est |
|---|---|---|---|
| HKc | 8 s | 7 | $0.80 |
| HKb | 6 s | 9 | $0.60 |
| JOIN | 6 s | 9 | $0.60 |
| CAb | 6 s | 7 | $0.60 |
| V1Q | 6 s | 6 | $0.60 |
| V2Q | 6 s | 6 | $0.60 |
| V3Q | 6 s | 9 | $0.60 |
| V4Q | 6 s | 7 | $0.60 |
| O2 | 6 s | 9 | $0.60 |
| O3 | 6 s | 10 | $0.60 |

Total: `engine=wan3 rows: estimated $6.20 at list price`.

## Step 5 — render: all 10 DONE
Command as given, log `songs\a12-karadi-w3\batch_main.log` (checked: no URL in it or in any of the 10 sidecars).

**Run window:** 2026-10-15 01:52:32 – 02:48:38 UTC = 2026-10-14 21:52:32 – 22:48:38 Toronto (EDT).

| Clip | Status | Task id | Wall s | Frames | Est | Retry lines | Scene-cut frames |
|---|---|---|---|---|---|---|---|
| HKc | done | `9b99c035-3724-475a-9f4b-5472106606b3` | 353.4 | 240 (8.000 s) | $0.80 | none | none |
| HKb | done | `be94d7ff-c409-4a50-a511-f6581318b53c` | 295.4 | 180 (6.000 s) | $0.60 | none | none |
| JOIN | done | `8f931f4c-b2b9-4edf-9862-24896eb4e6a1` | 306.0 | 180 (6.000 s) | $0.60 | none | none |
| CAb | done | `325c344c-8751-4c1c-b7d1-c0b3734be657` | 418.9 | 180 (6.000 s) | $0.60 | none | none |
| V1Q | done | `0bc3c876-fd73-4875-ad0a-6310b9e0ce43` | 290.0 | 180 (6.000 s) | $0.60 | none | none |
| V2Q | done | `9becfbdc-ce3f-4a7e-9562-f6df37b1bdd4` | 320.3 | 180 (6.000 s) | $0.60 | none | none |
| V3Q | done | `a3549bb5-09ea-4aca-bb2c-8c3a44b78d8d` | 417.0 | 180 (6.000 s) | $0.60 | none | none |
| V4Q | done | `e30fc120-2666-4192-9b72-d8b0c6177ad0` | 291.0 | 180 (6.000 s) | $0.60 | none | none |
| O2 | done | `35eb7e36-df6a-4aa5-883c-b144604b9061` | 362.7 | 180 (6.000 s) | $0.60 | none | none |
| O3 | done | `f6ed17f6-a462-4ab5-804c-9f987485ab40` | 305.5 | 180 (6.000 s) | $0.60 | none | none |

All 1280×720, 30 fps. Every task went submitted → RUNNING → SUCCEEDED; no failure lines, no fetch needed. `shots.csv`: all 10 → `done`
(runner's own update). The runner's table and total, verbatim:
```
SHOT       STATUS       WALL_S  FILE
HKc        done          353.4  songs/a12-karadi-w3\out\HKc-seed30313-w3.mp4
HKb        done          295.4  songs/a12-karadi-w3\out\HKb-seed30313-w3.mp4
JOIN       done          306.0  songs/a12-karadi-w3\out\JOIN-seed30313-w3.mp4
CAb        done          418.9  songs/a12-karadi-w3\out\CAb-seed30313-w3.mp4
V1Q        done          290.0  songs/a12-karadi-w3\out\V1Q-seed30313-w3.mp4
V2Q        done          320.3  songs/a12-karadi-w3\out\V2Q-seed30313-w3.mp4
V3Q        done          417.0  songs/a12-karadi-w3\out\V3Q-seed30313-w3.mp4
V4Q        done          291.0  songs/a12-karadi-w3\out\V4Q-seed30313-w3.mp4
O2         done          362.7  songs/a12-karadi-w3\out\O2-seed30313-w3.mp4
O3         done          305.5  songs/a12-karadi-w3\out\O3-seed30313-w3.mp4

total GPU-minutes (done shots): 56.0
```
**Runner's final estimate: $6.20** (`[O3] done … running list-price estimate $6.20`).

## Step 6 — sheets and cut check
**Scene-cut check** (`select='gt(scene,0.35)',showinfo`): **no frames printed for any of the 10 clips.**

In `songs\a12-karadi-w3\out\_qc\` (new files, ffmpeg `-n`), for each of the 10:
- `<ID>-contact.png` (5×2, tiles 384 wide, 1920×432; burned number = tile index 0–9, source frames evenly spaced first → last)
- `<ID>-every4-all.png` (every 4th frame, source frame number burned in, 192 wide, 10 per row; HKc 60 tiles, the others 45)
- stills: HKc `f000`, `f060`, `f120`, `f180`, `f239`; the 6 s clips `f000`, `f060`, `f120` and the last, `f179` — a 6 s clip has no
  frame 180, so its "180" still is the last frame.
