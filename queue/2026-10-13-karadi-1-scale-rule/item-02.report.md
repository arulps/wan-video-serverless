# item-02 report — DONE (Priya 1.15 → 1.02 m committed and pushed)

Run by CC (A12 watcher), 2026-10-13 12:21–12:30. Repo `C:\Projects\oviyan`, branch `thatha-hand-sprites`. $0. Vault/DB not touched.

## Step 1 — git state before the commit
- `git log -1 --format=%h` → `a1499f8`
- `git status --short` → 521 lines in total (other threads' uncommitted and untracked work; not listed here, not touched).
  The three files of this item:
  ```
   M docs/CHARACTER-HEIGHTS.md
   M src/data/characterCanon.ts
   M src/engine/__tests__/characterCanon.test.ts
  ```
- `git diff --stat` for the three files:
  ```
   docs/CHARACTER-HEIGHTS.md                   | 8 ++++++--
   src/data/characterCanon.ts                  | 8 ++++----
   src/engine/__tests__/characterCanon.test.ts | 6 ++++--
   3 files changed, 14 insertions(+), 8 deletions(-)
  ```
- Diff read line by line: every hunk is about Priya's height (1.15 → 1.02, "same height as Minnu") or the bible pin v60 → v62.
  No other thread's edits in these files. Nothing was staged before this item.

## Step 2 — canon test
`npx vitest run src/engine/__tests__/characterCanon.test.ts` → **1 file passed, 9 tests passed**.

## Step 4 — full suite
`npx vitest run` → **Test Files 135 passed | 1 skipped (136); Tests 2277 passed | 6 skipped (2283)**; 0 failed; 217 s.
No stash was needed (nothing failed).

## Step 5 — commit
- `273289f` — `canon: Priya same height as Minnu, 1.02 m (bible v62, Arul 2026-10-09)` — exactly the three files
  (3 files changed, 14 insertions, 8 deletions). Commit hooks ran and passed.
- Pushed: `origin/thatha-hand-sprites` `4d34f40..273289f`. The branch had no upstream configured, so the push named the branch
  explicitly (`git push origin thatha-hand-sprites`). The remote branch was behind local by earlier commits of other threads; those
  were already on other remote branches, and went up to this branch with the push.
- `docs\DISPATCH-CONVENTIONS.md` gives no commit-message template beyond the repo's `area: what` subjects; the item's subject was
  used as given. Its report rule (a report under `docs/dispatch-reports/` or `handoff/`) was **not** followed, because the item says
  to commit only the three files — this file is the report.

## Step 6 — for Arul
- **Set Priya's vault height in the Oviyan UI: Vault → Priya → Edit → Height 1.02.** (Not done here; the DB is yours.)
  Note `docs/dispatch-reports/CAST-MODEL-RECONCILIATION-2026-09-14.md` lists Priya as NOT-IN-VAULT — if she still is not bound,
  there is no row to edit yet.
- Chiku / Minmini: the hits below are asset-manifest names and descriptions and a bible build script. **No size in metres for
  Chiku or Minmini is visible in `src/` or `tools/` from these greps** (v26: Chiku 0.10 m; Minmini hand-sized, 0.50 m only when still).

## Hits that still say Priya is 1.15 m (for Fable; nothing changed)
- `docs/DECISIONS.md:452` — locked decision 14.23 "Priya keeps 1.15 m; age 7–8 → 6–7" (09-12, bible v60).
- `docs/DISPATCH-07C-CHARACTER-CANON.md:21` — "priya 1.15" in the seed list.
- `docs/bedtime/SESSION-HANDOFF-2026-09-12-BEDTIME-FORMAT.md:22` — "Priya keeps 1.15 m … now the visibly older friend".
- `docs/CHARACTER-HEIGHTS.md` — its remaining 1.15 mentions are the history notes (Minnu's "do not restore 1.15" and the new
  Priya exception), i.e. intended.
The other `1.15` hits (506 in all) are mostly shot-timing TSVs, test fixtures and ratios; CC did not classify them one by one.

## Step 3 — grep hits, verbatim (nothing changed; Fable decides on each)

### `git grep -n -i "priya" -- src docs tools` (after the commit)

```
docs/CHARACTER-HEIGHTS.md:31:| Priya | Minnu's best friend | 6–7 | **1.02** | same height as Minnu (v62, Arul 2026-10-09); still a year older |
docs/CHARACTER-HEIGHTS.md:36:| Mr. Rajan | Priya's dad | late 30s | 1.63 | |
docs/CHARACTER-HEIGHTS.md:37:| Meena | Priya's mom | early 30s | 1.52 | |
docs/CHARACTER-HEIGHTS.md:55:- **Priya is the second exception (v62, Arul 2026-10-09):** "she is of same height as minnu" — 1.02 m, not the 1.15
docs/CHARACTER-HEIGHTS.md:56:  her age ratio gives; age stays 6–7. Her model (Priya+·+Minnu's+Best+Friend.glb, 7 heads) is RESCALED, not
docs/DECISIONS.md:452:| 14.23 | **Priya keeps 1.15 m; age 7–8 → 6–7** | **09-12** | human bible v60 |
docs/DISPATCH-07C-CHARACTER-CANON.md:21:  paati 1.48 · kollu_thatha 1.45 · leo 0.95 · mila 0.95 · priya 1.15 ·
docs/bedtime/SESSION-HANDOFF-2026-09-12-BEDTIME-FORMAT.md:22:| 8 | **Priya keeps 1.15 m; her age moves 7–8 → 6–7** — now the visibly older friend | bible v60 |
docs/dispatch-reports/CAST-MODEL-RECONCILIATION-2026-09-14.md:11:| NOT-IN-VAULT | 18 (Paati, Kollu Thatha, Leo, Mila, Priya, Ms. Sophie, Mr. David, Mr. James, Amara, Mr. Rajan, Meena, Driver Uncle, Postman Uncle, Police Uncle, Ice Cream Anna, Salavaikkarar, Santa, Kalla v2) |
docs/dispatch-reports/CAST-MODEL-RECONCILIATION-2026-09-14.md:73:Leo → `Leo+·+Mintu's+Best+Friend (2).glb` · Mila → `Mila+·+Mintu's+Next-Door+Friend.glb` · Priya → `Priya+·+Minnu's+Best+Friend.glb` · Ms. Sophie → `Ms.+Sophie+·+Leo's+Mom.glb` · Mr. David → `Mr.+David+·+Leo's+Dad (1).glb` · Mr. James → `Mr.+James+·+Mila's+Dad.glb` · Amara → `Ms.+Amara+·+Mila's+Mom.glb` · 
docs/dispatch-reports/CAST-MODEL-RECONCILIATION-2026-09-14.md:96:| Priya | — (not in vault) | — | `Priya · Minnu's Best Friend.glb` | **NOT-IN-VAULT** | Bind when scheduled |
docs/dispatch-reports/CAST-MODEL-RECONCILIATION-2026-09-14.md:101:| Mr. Rajan | — (not in vault) | — | `Mr. Rajan · Priya's Dad.glb` | **NOT-IN-VAULT** | Bind when scheduled |
docs/dispatch-reports/CAST-MODEL-RECONCILIATION-2026-09-14.md:102:| Meena | — (not in vault) | — | `Mrs. Meena · Priya's Mom.glb` | **NOT-IN-VAULT** | Bind when scheduled |
docs/dispatch-reports/DISPATCH-RUN-ORDER-2026-09-12-REPORT.md:42:No write performed. Priya is not in the vault at all, so "do not touch Priya" is trivially satisfied.
docs/dispatch-reports/set-pilot-clinic/yaw0-2026-08-31/REPORT.md:206:Mintu, Minnu, Appa, Amma, Thatha, Paati, Kollu Thatha, Leo, Mila, Priya, Mr. David, Ms. Sophie,
src/data/assetManifest.json:4575:    "name": "Mr. Rajan · Priya's Dad",
src/data/assetManifest.json:4576:    "relPath": "Charecters/Mr.+Rajan+·+Priya's+Dad.glb",
src/data/assetManifest.json:4584:    "name": "Mrs. Meena · Priya's Mom",
src/data/assetManifest.json:4585:    "relPath": "Charecters/Mrs.+Meena+·+Priya's+Mom.glb",
src/data/assetManifest.json:4647:    "name": "Priya · Minnu's Best Friend",
src/data/assetManifest.json:4648:    "relPath": "Charecters/Priya+·+Minnu's+Best+Friend.glb",
src/data/characterCanon.ts:50:  { key: 'priya', name: 'Priya', name_tamil: '', // TODO: bible v43 has no Tamil name
src/data/characterCanon.ts:53:    aliases: ['priya', "minnu's best friend"], age: '6-7', height_meters: 1.02,
src/data/characterCanon.ts:65:    aliases: ['mr rajan', 'rajan', "priya's dad"], age: 'late 30s', height_meters: 1.63 },
src/data/characterCanon.ts:67:    aliases: ['mrs meena', 'meena', "priya's mom"], age: 'early 30s', height_meters: 1.52 },
src/engine/__tests__/characterCanon.test.ts:31:  it('Priya is older than Minnu but the same height (bible v62, Arul 2026-10-09)', () => {
src/engine/__tests__/characterCanon.test.ts:32:    const priya = CHARACTER_CANON.find((c) => c.key === 'priya')!
src/engine/__tests__/characterCanon.test.ts:34:    expect(priya.age).toBe('6-7')
src/engine/__tests__/characterCanon.test.ts:35:    expect(priya.height_meters).toBe(1.02)
src/engine/__tests__/characterCanon.test.ts:36:    expect(priya.height_meters).toBe(minnu.height_meters)
src/engine/__tests__/clipResolve.test.ts:45:    const r = resolveMovement({ action: 'reaches up above the head', demandedBy: 'Priya card', performer: 'child' }, CATALOG, BANNED)
src/engine/__tests__/clipResolve.test.ts:49:    expect(r.brief).toMatchObject({ id: r.clipName, action: 'reaches up above the head', demandedBy: 'Priya card', performer: 'child' })
tools/scripts/qc-tools/QC-TOOLS-README.md:43:against asymmetric dressing: Priya's sunflower clip and Kadai Anna's shoulder
tools/scripts/qc-tools/glb_turnaround.py:27:Cross-checked against asymmetric dressing: Priya's sunflower clip (her right)
```

### `git grep -n "1\.15" -- src docs tools`

```
docs/CHARACTER-HEIGHTS.md:41:  (3–4 yr ≈ 0.95 · 4–5 yr ≈ 1.00 · 6–7 yr ≈ 1.15).
docs/CHARACTER-HEIGHTS.md:43:  Mintu but at the SAME height — 1.02 m, not the 1.15 the age ratio would give.
docs/CHARACTER-HEIGHTS.md:51:  the day; cause of the "Minnu looks smaller" observation, fixed 2026-07-26 to 1.15.
docs/CHARACTER-HEIGHTS.md:54:  same height. **Do not "restore" 1.15.**
docs/CHARACTER-HEIGHTS.md:55:- **Priya is the second exception (v62, Arul 2026-10-09):** "she is of same height as minnu" — 1.02 m, not the 1.15
docs/DECISIONS.md:425:| 14.70 | ✅ **English pace is uniform (0.90 per 14.72). Spec v2 §4's pace curve (×1.15 / plateau / wind-down) is not applied to narration speed** — the word-count step in the script already makes the opening denser (14.27 pace-step check). Revisit only after script one is
docs/DECISIONS.md:452:| 14.23 | **Priya keeps 1.15 m; age 7–8 → 6–7** | **09-12** | human bible v60 |
docs/DISPATCH-07C-CHARACTER-CANON.md:20:  mintu 1.00 · minnu 1.15 · appa 1.65 · amma 1.55 · thatha 1.55 ·
docs/DISPATCH-07C-CHARACTER-CANON.md:21:  paati 1.48 · kollu_thatha 1.45 · leo 0.95 · mila 0.95 · priya 1.15 ·
docs/DISPATCH-22.1-QA-AUTOMATION-SWEEP.md:17:  height ≤ any kid's height × 1.15.
docs/PHASE-C1-ROSTER-REPORT.md:18:- Minnu_v42  — height → SET 1.15 (CORRECTED 2026-07-25: bible v43 says BIG
docs/bedtime/SESSION-HANDOFF-2026-09-12-BEDTIME-FORMAT.md:22:| 8 | **Priya keeps 1.15 m; her age moves 7–8 → 6–7** — now the visibly older friend | bible v60 |
docs/bedtime/bedtime-stories-format-spec-v2.md:167:| 1–5 | 0–6 | plateau × 1.15 | the place · who lives here · **the small want** (never a problem) |
docs/direction/DIRECTOR-KNOWLEDGE.md:168:  - **R17 (c) on a mouth that closes by the lips (2026-10-09, I-063).** Under rule M2 the closure is the lip-zip (`mouthClose` with its corrective), so a word can go from open lips to shut with the jaw nearly still (Minnu, D1 shot 2, "மின்மினி
docs/dispatch-reports/DISPATCH-22.1-REPORT.md:7:| 22.1.1 Character-height sanity gate | `src/engine/renderGates.ts` | DONE | Extended `heightSanityWarnings()` with: (a) role-based absolute ranges (adult 1.40–1.90, kid 0.80–1.30, animal 0.20–0.80), (b) relative adult-vs-kid check (adult must be
docs/dispatch-reports/DISPATCH-RUN-ORDER-2026-09-12-REPORT.md:41:**DB step was already done.** Vault reads `Minnu_v46 → height_meters 1.02` (eye 0.805), not 1.15.
docs/dispatch-reports/DISPATCH-d1-direction-pass-REPORT.md:40:- 3.0 Vault: `Minnu_v46.height_meters` **1.15 → 1.02** (rev 4's write had never reached this DB).
docs/dispatch-reports/classroom-kit-split-2026-08-31/REPORT.md:194:| **Mintu (1.00 m) seated** | seat 0.285 m, **0.159 m of thigh clearance** under the slab | he fits, with room; Minnu at 1.15 m also fits |
docs/dispatch-reports/classroom-kit-split-2026-08-31/qc-additions-2026-08-31.classroom-kit.PROPOSED.csv:2:classroom child chair (kit split 2026-08-31).glb,review,"PROP, split from preschool+classroom+3d+model.glb 2026-08-31 by loose parts (component 6 of 18); x14 child chairs in the source (13 free-
docs/dispatch-reports/env01-v2-pilot-2026-08-31/v3-2026-09-01/db-write-pack/sets-calibration-2026-09-01.sql:34:    blocked_rects     = '[{"x": 0.964, "z": -0.72, "width": 1.082, "depth": 1.178, "topY": 3.469}, {"x": -0.776, "z": 0.775, "width": 0.658, "depth": 0.317, "topY": 0.79}, {"x": 0.541, "z":
docs/dispatch-reports/indoor-set-survey/recalibration-2026-08-31/toy-kitchen/measurements.json:9449:      "implied_room_height_m": 1.15,
Binary file docs/dispatch-reports/motion-prototypes-2026-08-31/M-followup/Cook_Stir_Pot_v2_Dad.glb matches
docs/dispatch-reports/motion-prototypes-2026-08-31/M-followup/REPORT.md:50:| 1b | Wrist→fingertip chain in metres | **PASS, but smaller than the brief expected** | Mintu **4.8955 → 0.0490 m** model = 0.0496 m canon (brief expected 0.08–0.10); Dad 0.0663 → 0.1111 canon; Minnu 0.0614 → 0.070
docs/dispatch-reports/motion-prototypes-2026-08-31/M-followup/_twist4.json:880:  "k": 1.1521344382009533,
docs/dispatch-reports/motion-prototypes-2026-08-31/M-followup/_twist4.json:881:  "canon": 1.15,
docs/dispatch-reports/motion-prototypes-2026-08-31/M-followup/_twist4.json:1028:  "k": 1.1521344382009533,
docs/dispatch-reports/motion-prototypes-2026-08-31/M-followup/_twist4.json:1029:  "canon": 1.15,
docs/dispatch-reports/motion-prototypes-2026-08-31/M-followup/_twist4.json:1176:  "k": 1.1521344382009533,
docs/dispatch-reports/motion-prototypes-2026-08-31/M-followup/_twist4.json:1177:  "canon": 1.15,
docs/dispatch-reports/motion-prototypes-2026-08-31/M-followup/stir_poses_v2.json:1:[{"Spine1": [0.12985212949036032, -0.054999747493715855, -0.09399298063896061], "Spine2": [-0.1532115472667487, -0.05879377437187696, 0.20284348870175], "Neck": [0.6330876301881982, 0.06911565781944234, -0.10291185385
docs/dispatch-reports/motion-prototypes-2026-08-31/_geom.json:4254:      1.1529340233618173
docs/dispatch-reports/motion-prototypes-2026-08-31/_probe.json:384:    171.15646702731863,
docs/dispatch-reports/motion-prototypes-2026-08-31/_probe.json:2598:    171.15612817994395,
docs/dispatch-reports/oldmc-full-2026-09-04/L8-REPORT.md:152:sheep      14.393       -  15.952  19.445  21.157
docs/dispatch-reports/oldmc-full-2026-09-04/L8-REPORT.md:155:rooster    25.303  21.157  35.807  28.812       -
docs/dispatch-reports/set-kitchen-v2/REPORT.md:74:| 5.0 | 3.07 m | 3.87 m | 2.05 m | h ~1.15, fov 36–38.5 |
docs/dispatch-reports/set-kitchen-v2/readiness-2026-08-31/REPORT.md:255:`--cast` adds capsule proxies at 1.78 / 1.55 / 1.15 / 1.00 m, spaced by the engine's own
docs/dispatch-reports/set-kitchen-v2/readiness-2026-08-31/REPORT.md:302:- **`…fov34.2-cast.png`** — four capsules at 1.78 / 1.55 / 1.15 / 1.00 m, anchors at
docs/dispatch-reports/set-kitchen-v2/readiness-2026-08-31/probe/kitchen-gemini-sf60-void-probe.json:22:      1.15,
docs/dispatch-reports/set-kitchen-v2/readiness-2026-08-31/probe/kitchen-gemini-sf60-void-probe.json:37:        "height": 1.15,
docs/dispatch-reports/set-kitchen-v2/readiness-2026-08-31/probe/kitchen-v2-sf45-void-probe.json:22:      1.15,
docs/dispatch-reports/set-kitchen-v2/readiness-2026-08-31/probe/kitchen-v2-sf45-void-probe.json:37:        "height": 1.15,
docs/dispatch-reports/set-kitchen-v2/readiness-2026-08-31/scripts/bar-staging-check.ts:4:const hs=[1.78,1.55,1.15,1.00]; const rs=hs.map(h=>h*FOOTPRINT_RADIUS_PER_HEIGHT)
docs/dispatch-reports/set-kitchen-v2/readiness-2026-08-31/scripts/bite-test-9rects.ts:10:  { name: 'bar anchor 3 (0.48,-0.45) 1.15', x: 0.48, z: -0.45, h: 1.15 },
docs/dispatch-reports/set-pilot-bedroom/kitchen-blocked-rects.json:1:[{"x":-0.053,"z":0.246,"width":0.892,"depth":0.821,"topY":0.8},{"x":0.997,"z":-1.027,"width":0.63,"depth":0.986,"topY":2.44},{"x":-1.469,"z":-1.151,"width":0.734,"depth":0.821,"topY":2.44},{"x":-2.151,"z":-0.329,"width":0.734,"dept
docs/dispatch-reports/set-pilot-clinic/yaw0-2026-08-31/REPORT.md:214:(1.78/1.55/1.15/1.00 m). The task specifically asks for a 2-person doctor+child cast, so I added one
docs/dispatch-reports/set-pilot-clinic/yaw0-2026-08-31/REPORT.md:274:| 4 | 1.152 | 0.458 | 0.611 | 0.227 | 0.901 | bench forward lip |
docs/dispatch-reports/set-pilot-clinic/yaw0-2026-08-31/REPORT.md:521:| `tools/scripts/probe-set-void.mjs` | **+11 lines.** New optional `--cast-heights h1,h2,...` flag (default unchanged: falls back to the existing hardcoded `[1.78, 1.55, 1.15, 1.0]`), plus one usage-string line. | The task explicit
docs/dispatch-reports/set-pilot-clinic/yaw0-2026-08-31/bite-test.ts:20:  { x: 1.152, z: 0.458, width: 0.611, depth: 0.227 },   // 4 bench forward lip
docs/dispatch-reports/set-pilot-clinic/yaw0-2026-08-31/clinic-yaw0-blocked-rects-sf4.6875.json:31:    "x": 1.152,
docs/dispatch-reports/set-pilot-clinic/yaw0-2026-08-31/environment_sets-row-clinic.json:26:      { "x": 1.152, "z": 0.458, "width": 0.611, "depth": 0.227, "topY": 0.901 },
docs/dispatch-reports/set-pilot-clinic/yaw0-2026-08-31/make-and-overlay-rects.py:23:    {"x": 1.152, "z": 0.458, "width": 0.611, "depth": 0.227},
docs/dispatch-reports/set-pilot-clinic/yaw0-2026-08-31/repro/blocked-rects-sf4.6875.txt:16:[{"x":0.964,"z":-0.72,"width":1.082,"depth":1.178},{"x":-0.776,"z":0.775,"width":0.658,"depth":0.317},{"x":0.541,"z":-0.72,"width":0.423,"depth":0.408},{"x":-0.306,"z":0.322,"width":0.376,"depth":0.453},{"x":1
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:37:33	76.2500	78.2167	1.9667	NOFACE	0	nan	static	2.1480	189.6125	0.4320	1.1524	30.0000	0.1393	1	cut	0.0000	milk bottle (prop, split-screen)	ECU	two identical bottles are held out in a mirrored split-screen, one in each child's hand, b
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:71:67	160.7500	163.9667	3.2167	WS	0	0.8512	complex	14.4584	170.2314	0.5342	1.1551	30.0000	0.7616	1	cut	0.0256	barn (red, establishing)	EWS	static exterior, clouds drift overhead, two ducklings peck near the haypiles at its base	duckli
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:272:268	653.5000	656.2500	2.7500	NOFACE	0	nan	complex	15.7002	169.6549	0.3634	1.5544	30.0000	1.1569	0	cut	0.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:388:384	933.8167	935.3167	1.5000	MCU	1	0.5352	pan_R	23.2690	193.6452	0.3109	1.1544	40.0000	0.8105	1	cut	1.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:516:512	1268.2000	1269.7333	1.5333	EWS	0	0.9449	tilt_up	20.9859	135.0033	0.4268	1.1557	50.0000	3.5386	0	cut	0.0556							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:536:532	1340.7000	1343.5333	2.8333	NOFACE	0	nan	pan_L	29.0942	187.6328	0.5889	0.4286	200.0000	1.1564	0	cut	0.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:557:553	1377.3167	1380.0333	2.7167	MCU	1	0.6814	static	11.1576	216.8544	0.5874	0.4236	200.0000	1.3765	1	cut	0.5455							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:562:558	1392.3167	1394.4000	2.0833	NOFACE	0	nan	pan_L	27.7077	200.7367	0.4928	1.1566	0.0000	2.1282	1	cut	0.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:566:562	1405.2833	1413.9833	8.7000	MS	1	0.7441	pan_R	25.0064	229.4309	0.2218	1.1534	0.0000	2.0892	1	cut	0.5962							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:580:576	1466.4000	1470.5667	4.1667	MS	0	0.8343	complex	15.8384	230.2836	0.2109	1.1547	0.0000	1.5231	0	cut	0.5000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:636:632	1610.6500	1612.6500	2.0000	MCU	2	0.6647	static	4.3087	221.5252	0.5000	0.8188	200.0000	1.1516	1	cut	1.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:691:687	1802.2000	1806.6167	4.4167	MCU	0	0.7258	pan_R	231.1560	191.4644	0.5221	2.1194	40.0000	0.8030	1	cut	0.0377							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:704:700	1845.9500	1848.7833	2.8333	WS	1	0.5127	pull	14.1064	140.0991	0.4849	1.1552	80.0000	4.0723	0	cut	0.7059							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:732:728	1908.0667	1911.1500	3.0833	WS	1	0.5488	complex	16.5528	132.3870	0.4686	1.3977	40.0000	3.8694	0	cut	0.8919							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:733:729	1911.1500	1913.6167	2.4667	WS	1	0.3574	pan_R	26.0233	138.6142	0.5174	1.2357	80.0000	1.0783	1	cut	0.8667							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:786:782	2029.9000	2032.9500	3.0500	MS	1	0.4941	pan_L	25.5990	207.6003	0.4317	1.1549	80.0000	2.0517	0	cut	1.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:858:854	2216.7333	2218.4500	1.7167	MS	1	0.5225	pan_R	22.8498	188.8595	0.3746	1.1572	100.0000	0.5344	0	cut	0.6190							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:889:885	2280.8167	2283.6500	2.8333	CU	0	0.5375	static	4.8646	208.2646	0.3210	1.1577	40.0000	0.6117	0	cut	0.3529							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:944:940	2431.6500	2434.9333	3.2833	MCU	1	0.5018	unknown	nan	234.6897	0.3463	0.7592	190.0000	1.1509	1	cut	0.9500							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:1006:1002	2576.8500	2578.4333	1.5833	MS	1	0.5874	static	0.1054	161.1548	0.4603	1.0817	80.0000	0.4193	0	cut	1.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:1022:1018	2607.9833	2611.1500	3.1667	MCU	0	0.6748	tilt_down	39.1769	132.9049	0.3308	0.7538	210.0000	0.9962	1	cut	0.1842							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:1023:1019	2611.1500	2612.9833	1.8333	MCU	3	0.8405	pan_L	20.7674	179.8841	0.4253	0.8340	240.0000	1.7482	1	cut	1.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:1039:1035	2648.5667	2651.1500	2.5833	MS	3	0.4114	static	0.1421	152.9627	0.5193	1.2534	30.0000	0.2102	1	cut	1.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:1040:1036	2651.1500	2653.2333	2.0833	EWS	1	0.5695	static	0.7588	174.5544	0.3377	0.8812	200.0000	0.1592	0	cut	0.6400							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:1102:1098	2814.4833	2816.8167	2.3333	MCU	2	0.4026	static	20.1915	207.4679	0.4773	1.1501	100.0000	1.7589	1	cut	1.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:1199:1195	3012.3833	3015.0500	2.6667	MS	2	0.5518	static	8.4603	173.3825	0.5064	1.0175	30.0000	1.1582	1	cut	1.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:1336:1332	3310.3500	3311.4333	1.0833	CU	1	0.3590	static	1.1504	204.5740	0.2419	1.0104	60.0000	1.1120	1	cut	1.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:1400:1396	3418.0833	3418.3333	0.2500	NOFACE	0	nan	unknown	nan	246.1321	0.1547	1.1529	0.0000	5.2315	0	cut	0.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-shots.tsv:1426:1422	3471.4167	3472.6333	1.2167	NOFACE	0	nan	unknown	nan	243.7666	0.1492	1.1543	0.0000	5.1542	0	cut	0.0000							
docs/reference-grammar/deep/baa-baa-black-sheep-lalafun-summary.md:226:| 54:40.00-55:00.00 | 19 | 1.15 |
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:12:8	22.4583	26.4583	4.0000	MCU	0	0.4502	pan_L	119.2586	151.1509	0.5116	1.0961	210.0000	8.3096	1	cut	0.0526	frog (bib "1", climbs ladder)	MCU	starts seated on the log with frog "2" beside it, then climbs up the wooden log
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:22:18	40.6667	43.0000	2.3333	MS	0	0.3425	pan_L	60.7780	134.1508	0.5520	1.1581	30.0000	10.9202	0	cut	0.1818	frog (bib "2")	MS	stands up on the log among the other frogs, gestures with both hands as it sings	group: frogs (b
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:34:30	70.5000	78.4167	7.9167	MCU	0	0.5322	tilt_up	69.0610	174.7676	0.5702	1.1510	80.0000	9.2715	0	cut	0.0263	frog (bib "3")	MCU	mimes eating bugs and licking its lips, then the shot cuts to it balanced tiny atop a tall th
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:43:39	95.5000	97.7917	2.2917	NOFACE	0	nan	complex	59.6966	141.4481	0.5588	1.1041	210.0000	11.1581	1	cut	0.0000	frog (bib "4")	MS	stands up on the log, gesturing with both arms as it begins to sing	group: frogs (2 others, 
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:121:117	308.6250	312.8750	4.2500	ECU	1	0.5927	unknown	nan	158.4374	0.4412	1.1533	0.0000	10.3957	0	cut	1.0000	baby JJ (blonde tuft, green onesie)	ECU	Wide-eyed, then scrunches up and opens his mouth in a crying "wah" expre
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:157:153	429.0833	431.0833	2.0000	CU	1	0.3734	pan_R	35.3586	187.9996	0.2915	1.1545	10.0000	9.1198	1	cut	0.7000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:185:181	520.0417	522.0000	1.9583	MCU	0	0.3522	complex	114.0213	215.1917	0.1914	1.1592	0.0000	8.4678	1	cut	0.1111							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:554:550	1588.9167	1589.9583	1.0417	CU	1	0.5320	pan_L	62.7739	212.0113	0.4107	1.1917	150.0000	11.1504	0	cut	0.8000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:602:598	1666.6667	1670.5000	3.8333	MCU	2	0.6378	static	4.2193	185.1121	0.4341	1.1502	10.0000	3.7094	0	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:628:624	1727.1250	1730.9583	3.8333	MS	1	0.4508	pan_R	36.6515	166.5674	0.4328	1.1502	30.0000	4.6693	1	cut	0.6111							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:668:664	1842.5417	1847.3750	4.8333	WS	2	0.3909	complex	13.7639	147.1248	0.3855	1.1531	350.0000	5.7842	0	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:685:681	1879.0000	1881.3750	2.3750	MS	2	0.4191	complex	50.9016	175.4414	0.5443	1.1589	80.0000	8.5326	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:940:936	2596.4167	2600.1667	3.7500	CU	1	0.5235	complex	84.1658	189.2044	0.3691	1.1568	90.0000	12.2594	1	cut	0.6111							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:1076:1072	3025.1667	3029.7917	4.6250	CU	1	0.4607	static	16.8767	174.8951	0.3688	1.1562	200.0000	8.1673	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:1083:1079	3051.3750	3056.1667	4.7917	ECU	1	0.4899	unknown	nan	199.7079	0.2448	1.1581	10.0000	6.3080	0	cut	0.9130							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:1186:1182	3353.3750	3354.3750	1.0000	CU	0	0.4641	pan_R	157.4238	177.9814	0.5656	1.9696	30.0000	11.1534	1	cut	0.2500							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:1368:1364	3912.5000	3916.0417	3.5417	NOFACE	0	nan	pan_R	18.5318	133.9096	0.5289	1.1590	100.0000	6.2268	0	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:1391:1387	3977.1250	3979.1250	2.0000	NOFACE	0	nan	tilt_up	83.8875	192.6718	0.4091	1.1563	90.0000	24.1255	0	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:1417:1413	4059.5417	4061.3333	1.7917	NOFACE	0	nan	tilt_up	207.8764	184.9023	0.3764	1.1522	140.0000	6.3322	1	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:1561:1557	4425.7500	4427.2500	1.5000	NOFACE	0	nan	static	16.5597	148.5983	0.4161	1.1532	10.0000	2.5789	1	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:1578:1574	4467.2500	4468.4583	1.2083	CU	2	0.7726	complex	41.3348	133.9521	0.3843	1.1586	10.0000	5.4152	0	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:1650:1646	4639.4167	4640.8750	1.4583	NOFACE	0	nan	static	8.1870	208.3065	0.5163	1.1531	350.0000	2.7154	1	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2003:1999	5722.3333	5725.3333	3.0000	MCU	0	0.4282	static	4.5627	69.3555	0.5297	1.1595	110.0000	3.1081	1	cut	0.1429							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2037:2033	5787.3750	5790.8750	3.5000	NOFACE	0	nan	complex	31.1581	120.4364	0.5162	1.3037	0.0000	7.7430	0	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2154:2150	6127.0000	6128.8750	1.8750	NOFACE	0	nan	static	12.3404	212.5160	0.1486	1.1519	40.0000	2.0930	0	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2218:2214	6319.8750	6321.0000	1.1250	MS	0	0.5976	static	7.4180	200.4391	0.4551	1.1521	340.0000	8.1812	1	cut	0.2000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2280:2276	6452.0000	6455.0833	3.0833	MCU	2	0.4614	pan_L	37.4224	194.8115	0.4108	1.1565	350.0000	8.4031	1	cut	0.8000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2414:2410	6737.7083	6741.3333	3.6250	WS	4	0.7117	complex	12.2285	176.5977	0.2368	1.1507	130.0000	1.3006	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2525:2521	7051.5000	7054.5417	3.0417	MCU	0	0.9086	complex	6.2484	158.0425	0.3162	1.1500	60.0000	7.1466	0	cut	0.3571							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2586:2582	7226.2917	7229.7083	3.4167	WS	2	0.5989	tilt_down	26.3721	211.1585	0.4612	0.8620	350.0000	4.2065	0	cut	0.9375							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2620:2616	7292.8750	7295.7500	2.8750	ECU	1	0.5343	unknown	nan	230.6470	0.2585	1.1588	10.0000	2.9878	1	cut	0.7857							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2722:2718	7577.5000	7586.2917	8.7917	MCU	1	0.6384	static	15.7482	148.8123	0.7533	1.1569	90.0000	5.6348	0	cut	0.9302							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2804:2800	7840.2500	7845.6667	5.4167	MS	1	0.5622	complex	11.1557	167.2720	0.5759	2.1309	40.0000	7.2598	1	cut	0.7692							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2834:2830	7921.5000	7923.5000	2.0000	NOFACE	0	nan	pan_R	26.6135	79.4702	0.2429	1.1530	0.0000	3.3638	0	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:2860:2856	7978.2917	7980.2500	1.9583	NOFACE	0	nan	complex	22.0208	125.1718	0.3046	1.1514	350.0000	3.1132	1	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:3063:3059	8614.7083	8617.6667	2.9583	CU	6	0.1354	static	4.6915	170.1208	0.4580	1.1571	10.0000	4.0803	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:3568:3564	9967.1250	9969.9583	2.8333	CU	1	0.6079	complex	20.0911	201.1547	0.2802	1.0323	0.0000	6.8523	0	cut	0.6154							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:3587:3583	10015.4583	10018.5417	3.0833	CU	3	0.7379	static	15.2310	194.1196	0.3112	1.1594	20.0000	3.8245	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:3647:3643	10147.2083	10149.2917	2.0833	MCU	2	0.3943	pan_R	40.3530	145.1167	0.2861	1.1566	180.0000	6.5963	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:3666:3662	10199.4167	10200.5000	1.0833	CU	2	0.7797	static	2.1654	177.2182	0.4104	1.1559	10.0000	2.7048	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:3876:3872	10638.4583	10640.8333	2.3750	MS	2	0.7309	tilt_down	68.2907	176.8205	0.4042	1.1508	80.0000	16.2497	0	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:3884:3880	10656.6667	10658.0417	1.3750	CU	2	0.5550	tilt_down	39.8617	177.6205	0.4249	1.1577	90.0000	14.5567	0	cut	0.8571							
docs/reference-grammar/deep/five-little-speckled-frogs-cocomelon-3hr-shots.tsv:4029:4025	11130.5833	11131.5000	0.9167	CU	1	0.4176	tilt_down	21.9113	218.0392	0.4681	1.1520	10.0000	6.1751	0	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:8:4	9.1667	13.7167	4.5500	MS	0	0.0866	static	3.3054	158.5914	0.5836	0.9725	170.0000	1.1559	0	cut	0.2727	group: five frogs	MS	sit in a row on the log while a golden fish leaps from the pond behind them, ripples spreading	golden 
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:36:32	72.5833	74.1333	1.5500	MCU	2	0.6482	pan_R	71.8960	166.8462	0.6502	1.1579	80.0000	1.6277	0	cut	1.0000	toddler (yellow tee)	MCU	holds up a small blue toy shark, admiring it	brother (blue-teal tee) leans down to look	bright 
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:143:139	319.7833	323.9500	4.1667	WS	3	0.5056	complex	19.3402	146.2321	0.5270	1.5174	50.0000	1.1578	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:146:142	330.7833	332.3667	1.5833	MS	1	0.5873	static	0.1149	161.1598	0.4603	1.0816	80.0000	0.4148	0	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:195:191	436.7833	438.5000	1.7167	MCU	1	0.6317	pan_L	39.2689	204.4751	0.3092	1.1596	40.0000	1.5051	0	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:205:201	459.0000	459.3667	0.3667	NOFACE	0	nan	unknown	nan	221.8462	0.1388	1.1504	50.0000	0.5520	1	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:307:303	708.1667	709.7000	1.5333	EWS	0	0.9575	complex	16.8690	135.0224	0.4264	1.1555	50.0000	3.4581	1	cut	0.0526							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:365:361	863.1667	865.5000	2.3333	MCU	2	0.4026	static	19.9822	207.4630	0.4773	1.1502	100.0000	1.7925	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:466:462	1106.9833	1110.0333	3.0500	MS	1	0.4939	pan_L	26.8614	207.5977	0.4318	1.1549	80.0000	2.0361	0	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:656:652	1671.0667	1673.0667	2.0000	CU	2	0.4975	tilt_down	38.7622	179.3763	0.5359	1.3573	30.0000	1.1553	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:704:700	1849.0667	1851.1500	2.0833	MCU	1	0.7372	pan_R	78.2836	152.1067	0.3071	1.0013	190.0000	1.0071	1	cut	0.9600							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:705:701	1851.1500	1852.5667	1.4167	WS	3	0.2312	static	8.8328	235.6576	0.4725	0.9411	50.0000	0.7568	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:749:745	1952.2333	1953.7000	1.4667	NOFACE	0	nan	complex	17.1590	139.4813	0.3704	1.2824	0.0000	1.1582	1	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:781:777	2017.9833	2018.2333	0.2500	NOFACE	0	nan	unknown	nan	246.1249	0.1547	1.1529	0.0000	5.2498	0	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:809:805	2071.3167	2072.5333	1.2167	NOFACE	0	nan	unknown	nan	243.7643	0.1492	1.1543	0.0000	5.2040	0	cut	0.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:833:829	2115.5333	2121.1500	5.6167	MCU	1	0.5580	unknown	nan	245.3481	0.1736	0.9496	0.0000	2.7166	1	cut	0.9552							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:834:830	2121.1500	2123.2333	2.0833	CU	0	0.5222	unknown	nan	245.4663	0.0819	0.9716	0.0000	1.3657	0	cut	0.0400							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:918:914	2313.9833	2318.9000	4.9167	MS	3	0.3361	static	1.4657	147.3719	0.6390	1.7675	40.0000	1.1565	0	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:952:948	2434.4667	2436.7667	2.3000	CU	2	0.5039	truck_R	31.1900	190.3975	0.3923	1.1867	30.0000	1.1539	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:960:956	2456.7667	2458.4667	1.7000	MS	0	0.9758	complex	17.0584	220.4844	0.2650	1.1570	30.0000	0.7091	1	cut	0.0500							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:963:959	2462.6000	2463.9667	1.3667	MCU	2	0.4671	unknown	nan	194.0569	0.3511	1.1568	30.0000	1.1360	0	cut	0.9375							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:1196:1192	2930.6333	2932.3333	1.7000	EWS	0	0.6364	pan_L	55.6448	168.4494	0.1279	1.1573	20.0000	0.9338	1	cut	0.0500							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:1278:1274	3130.7833	3132.3667	1.5833	MCU	2	0.5895	static	4.9175	193.8395	0.4601	0.9033	180.0000	1.1504	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:1341:1337	3269.2000	3270.7000	1.5000	MCU	1	0.5378	pan_R	23.8563	193.6527	0.3108	1.1544	40.0000	0.8085	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:1344:1340	3280.0333	3281.7833	1.7500	CU	1	0.3751	unknown	nan	213.1929	0.2894	1.1556	40.0000	2.3048	1	cut	0.8571							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:1346:1342	3287.3333	3288.8667	1.5333	MCU	1	0.4587	pan_L	74.6083	182.6651	0.2317	0.9860	130.0000	1.1580	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:1410:1406	3464.5333	3468.0333	3.5000	MS	3	0.7020	static	12.4616	191.1525	0.5103	1.0181	110.0000	1.6892	1	cut	1.0000							
docs/reference-grammar/deep/five-little-speckled-frogs-lalafun-shots.tsv:1459:1455	3554.6167	3557.2833	2.6667	MS	2	0.5514	static	8.4840	173.3928	0.5064	1.0175	30.0000	1.1581	1	cut	1.0000							
docs/reference-grammar/deep/jj-gets-dressed-cocomelon-shots.tsv:40:36	109.5333	114.6667	5.1333	MS	2	0.2253	complex	4.3456	163.8832	0.4901	1.1584	50.0000	6.1932	0	cut	0.9667	group: mom + baby JJ	MS	the trio's raincoat pose holds, then the scene shifts to mom alone by the shelf before revealing JJ pla
docs/reference-grammar/deep/jj-gets-dressed-cocomelon-shots.tsv:49:45	136.3667	140.3333	3.9667	CU	1	0.5742	pan_L	27.9649	174.1542	0.4526	1.1512	180.0000	5.8181	1	cut	0.8696	baby JJ (blonde tuft, green onesie)	CU	grins in his goggles, raises his hands to his face in delight, then turns to embrace his
docs/reference-grammar/deep/jj-gets-dressed-cocomelon-shots.tsv:59:55	174.0333	179.3667	5.3333	MCU	0	0.3806	pan_L	34.6141	185.5023	0.3531	1.1506	170.0000	4.6367	0	cut	0.4062	title card	EWS	static card reads "Yes Yes Save the Earth Song" over an animal-and-watermelon garden background; then cuts to r
docs/reference-grammar/deep/jj-gets-dressed-cocomelon-shots.tsv:72:68	204.9333	206.3333	1.4000	WS	1	0.1027	static	11.5135	160.1015	0.5154	1.1532	350.0000	8.1092	0	cut	1.0000	bear (red, plush)	MCU	reaches one arm toward the light switch on a tiled wall, about to press it	baby JJ (blonde tuft, green o
src/data/animalHeights.ts:49:  cow: { heightM: 1.15, sizeClass: 3 },
src/data/characterCanon.ts:52:    // Minnu, 1.02 m (was 1.15) — still a year older, no longer taller.
src/data/shotGrammar.ts:81: * rays clear a 1.15 m animal 1.5 m behind the prop; the camera pulls back
src/data/shotGrammar.ts:82: * ~0.2 m to hold fill (cameraZ ≥ 0.3). For a 1.15 m cow it is ~25°.
src/data/stageCalibration.ts:186:    cameraHeight: 1.15,
src/engine/__tests__/cameraKeys.test.ts:383:    const cal = { cameraHeight: 1.15, cameraZ: 3.0, cameraFov: 34, backdropOverfill: 1.5, cameraClamp: 'free' as const }
src/engine/__tests__/directorPreflight.test.ts:55:  { ...propsAsAuthored[0], worldX: 1.5, renderHeightM: 1.15 }, // cow 0.5 m further right: its flank was 17 % of Thatha's singles at x 1.0
src/engine/__tests__/directorPreflight.test.ts:123:    expect(frameAreaFraction(insert, 1.0, -1.0, 1.15, 1.0)).toBeGreaterThan(0)
src/engine/__tests__/directorPreflight.test.ts:125:    expect(frameAreaFraction(insert, 1.5, -1.0, 1.15, 1.0)).toBeLessThan(0.03)
src/engine/__tests__/directorPreflight.test.ts:127:    const cow: FramingSubject = { id: 'cow', worldX: 1.5, worldZ: -1.0, heightM: 1.15, eyeHeightM: 0.7, yawDeg: 336, kind: 'prop' }
src/engine/__tests__/directorPreflight.test.ts:128:    expect(frameAreaFraction(insert, 1.5, -1.0, 1.15, 1.0)).toBeLessThan(0.03)
src/engine/__tests__/directorPreflight.test.ts:640:      props: [{ id: 'cow-brown', worldX: 1.5, worldZ: -1.0, heightM: 1.15, spec: { prop: 'cow-brown' } }],
src/engine/__tests__/directorRules.test.ts:22:const cow = { id: 'cow', worldX: 1.0, worldZ: -1.0, heightM: 1.15, renderHeightM: 1.15, spec: { prop: 'cow' } }
src/engine/__tests__/faceRecordLiveliness.test.ts:19:    expect(m.words).toEqual([{ word: 'minmini', startS: 10.1, jawDeg: 1.15, gapMm: 12.16, gapBarMm: 6.06, by: 'gap' }])
src/engine/__tests__/faceRecordLiveliness.test.ts:43:    expect(r.mouthByWord?.[0]).toMatchObject({ by: 'gap', gapMm: 12.16, jawDeg: 1.15 })
src/engine/__tests__/fixtures/faceDrive/poc-song-cues.json:1:{"source":"poc/blender/out/s5/song.json (Rhubarb on the PoC song stem)","duration":151.24,"mouthCues":[{"start":0,"end":2.87,"value":"X"},{"start":2.87,"end":3.23,"value":"B"},{"start":3.23,"end":3.37,"value":"F"},{"start":3.37,"end":3.58,
src/engine/__tests__/framingRules.test.ts:167:const cowV4: FramingSubject = { id: 'cow-brown', worldX: 2.1, worldZ: -1.2, heightM: 1.15, eyeHeightM: 0.69, yawDeg: 336.4, kind: 'prop', lengthM: 1.66 }
src/engine/__tests__/framingRules.test.ts:296:    const cow = propCrownEnvelopeM({ heightM: 1.15, lengthM: 1.66 }, { position: [2.1, 0, -1.2], seed: 101, signature: { kind: 'moo', windows: [{ startSec: 0, endSec: 2.5 }] } }, 2.5, 30)
src/engine/__tests__/framingRules.test.ts:297:    const still = propCrownEnvelopeM({ heightM: 1.15, lengthM: 1.66 }, { position: [2.1, 0, -1.2], seed: 101, bobAmplitude: 0, perkSeconds: 0, squashAmplitude: 0 }, 2.5, 30)
src/engine/__tests__/framingRules.test.ts:358:const cowV5: FramingSubject = { id: 'cow-brown', worldX: 3, worldZ: -1.2, heightM: 1.15, eyeHeightM: 0.69, yawDeg: 336.38, kind: 'prop', lengthM: 1.66 }
src/engine/__tests__/housePreflight.test.ts:5:const farm: HousePreflightCalibration = { cameraHeight: 1.15, cameraZ: 3.0, cameraFov: 34, characterZ: 0, backdropOverfill: 1.5, cameraClamp: 'free' }
src/engine/__tests__/renderGates.test.ts:527:      { name: 'Appa', heightMeters: 1.15 },
src/engine/__tests__/renderGates.test.ts:530:    // 1.15 <= 1.0 * 1.15 = 1.15, so it triggers
src/engine/__tests__/renderGates.test.ts:717:      [{ name: 'Minnu_v46', worldX: 0.4, worldZ: 0.3, heightMeters: 1.15 }],
src/engine/__tests__/shotFraming.test.ts:249:  const cow: FramingSubject = { id: 'cow', worldX: 0, worldZ: -1.2, heightM: 1.15, eyeHeightM: 0.69, yawDeg: 0, kind: 'prop' }
src/engine/__tests__/shotPlanner.test.ts:325:    const cow = { id: 'cow', worldX: -1.75, worldZ: -1.65, heightM: 1.15, renderHeightM: 1.15, lengthM: 1.66, spec: { prop: 'cow', yaw: 0 } }
src/engine/__tests__/shotPlanner.test.ts:336:    const cow = { id: 'cow', worldX: -1.75, worldZ: -1.65, heightM: 1.15, renderHeightM: 1.15, lengthM: 1.66, spec: { prop: 'cow', yaw: 0 } }
src/engine/__tests__/shotPlanner.test.ts:366:    const behind = { id: 'cow', worldX: 0, worldZ: -1.6, heightM: 1.15, eyeHeightM: 0.69, yawDeg: 0, kind: 'prop' as const, lengthM: 1.66 }
src/engine/__tests__/stageCalibration.test.ts:526:    const children = castStagingWidth([1.0, 1.15])
src/engine/__tests__/stageCalibration.test.ts:527:    const mixed = castStagingWidth([1.65, 1.15])
src/engine/__tests__/stageCalibration.test.ts:670:    const family = cameraHeightForCast([1.65, 1.55, 1.15, 1.0])
src/engine/__tests__/stageCalibration.test.ts:671:    const classroom = cameraHeightForCast([1.55, 1.15, 1.0, 1.15, 1.0, 1.0, 1.15])
src/engine/__tests__/stageCalibration.test.ts:682:    expect(castStagingWidth([1.55, 1.15, 1.0, 1.15, 1.0, 1.0, 1.15]))
src/engine/cameraKeys.ts:160: * At the default rig / 1.1 overfill that is ≈ 0.19 m; at 1.6 it is ≈ 1.15 m.
src/engine/renderGates.ts:505:/** 22.1.1: relative check — adults must be > kid × 1.15. */
src/engine/renderGates.ts:506:const ADULT_KID_FACTOR = 1.15
src/engine/renderGates.ts:518: * - 22.1.1: relative — adult ≤ any kid × 1.15
src/engine/renderGates.ts:554:  // 22.1.1: relative check — every adult must be taller than every kid × 1.15
src/remotion/components/colours/Sparkles.tsx:7:  { a: -78, d: 1.0, s: 1.15 },
src/remotion/compositions/Stage3DScene.tsx:314:     * subject 134 is 18 apart; the target is >= 30. Nudging `scale` to ~1.15
src/remotion/compositions/TeacherHandSprite.tsx:529:      scene.add(new THREE.AmbientLight(0xffffff, 1.15))
Binary file tools/anim-clips-authored/Arm_Swing_Sides.glb matches
Binary file tools/anim-clips-authored/Arms_Up_Pick_Me_Up.glb matches
Binary file tools/anim-clips-authored/Arms_Wide_Hold.glb matches
Binary file tools/anim-clips-authored/Bird_Flap.glb matches
Binary file tools/anim-clips-authored/Bird_Peck.glb matches
Binary file tools/anim-clips-authored/Blow_Candles.glb matches
Binary file tools/anim-clips-authored/Brush_Teeth.glb matches
Binary file tools/anim-clips-authored/Bus_Seat_Bounce.glb matches
Binary file tools/anim-clips-authored/Call_Out.glb matches
Binary file tools/anim-clips-authored/Cat_Lap_Milk.glb matches
Binary file tools/anim-clips-authored/Cat_Paw_Lick.glb matches
Binary file tools/anim-clips-authored/Cat_Paw_Swipe.glb matches
Binary file tools/anim-clips-authored/Cat_Whiskers.glb matches
Binary file tools/anim-clips-authored/Cheek_Touch_Adult.glb matches
Binary file tools/anim-clips-authored/Cheek_Touch_Kid.glb matches
Binary file tools/anim-clips-authored/Chicken_Wings.glb matches
Binary file tools/anim-clips-authored/Clap_Big.glb matches
Binary file tools/anim-clips-authored/Clap_Seated.glb matches
Binary file tools/anim-clips-authored/Comb_Hair.glb matches
Binary file tools/anim-clips-authored/Cough_Into_Elbow.glb matches
Binary file tools/anim-clips-authored/Count_Hand_Front.glb matches
Binary file tools/anim-clips-authored/Cover_Face_Scared.glb matches
Binary file tools/anim-clips-authored/Cow_Horns.glb matches
Binary file tools/anim-clips-authored/Cradle_Rock.glb matches
Binary file tools/anim-clips-authored/Dog_Paws_Beg.glb matches
Binary file tools/anim-clips-authored/Dosa_Flip.glb matches
Binary file tools/anim-clips-authored/Dosa_Spread.glb matches
Binary file tools/anim-clips-authored/Drink_Cup_Seated.glb matches
Binary file tools/anim-clips-authored/Duck_Bill.glb matches
Binary file tools/anim-clips-authored/Ears_Hold_Sorry.glb matches
Binary file tools/anim-clips-authored/Eat_By_Hand_Seated.glb matches
Binary file tools/anim-clips-authored/Eat_With_Spoon_Seated.glb matches
Binary file tools/anim-clips-authored/Elephant_Ears.glb matches
Binary file tools/anim-clips-authored/Elephant_Trunk.glb matches
Binary file tools/anim-clips-authored/Feed_By_Hand_Adult.glb matches
Binary file tools/anim-clips-authored/Feed_By_Hand_Kid.glb matches
Binary file tools/anim-clips-authored/Finger_Wag_No.glb matches
Binary file tools/anim-clips-authored/Fish_Swim_Hands.glb matches
Binary file tools/anim-clips-authored/Flex_Muscle.glb matches
Binary file tools/anim-clips-authored/Flex_Muscle_Hold.glb matches
Binary file tools/anim-clips-authored/Flower_In_Hair.glb matches
Binary file tools/anim-clips-authored/Foot_Tap.glb matches
Binary file tools/anim-clips-authored/Frog_Hop.glb matches
Binary file tools/anim-clips-authored/Giggle_Hands_Mouth.glb matches
Binary file tools/anim-clips-authored/Give_Hold.glb matches
Binary file tools/anim-clips-authored/Give_Two_Hands.glb matches
Binary file tools/anim-clips-authored/Hand_Hold_Adult_L.glb matches
Binary file tools/anim-clips-authored/Hand_Hold_Kid_R.glb matches
Binary file tools/anim-clips-authored/Hand_On_Forehead.glb matches
Binary file tools/anim-clips-authored/Hands_On_Head.glb matches
Binary file tools/anim-clips-authored/Hands_On_Hips.glb matches
Binary file tools/anim-clips-authored/Head_Shoulders_Knees_Toes.glb matches
Binary file tools/anim-clips-authored/Head_Wobble.glb matches
Binary file tools/anim-clips-authored/Horn_Press.glb matches
Binary file tools/anim-clips-authored/Horn_Press_Seated.glb matches
Binary file tools/anim-clips-authored/Horse_Ride_Bounce.glb matches
Binary file tools/anim-clips-authored/Hug_Adult.glb matches
Binary file tools/anim-clips-authored/Hug_Adult_Hold.glb matches
Binary file tools/anim-clips-authored/Hug_Kid.glb matches
Binary file tools/anim-clips-authored/Hug_Kid_Hold.glb matches
Binary file tools/anim-clips-authored/Hug_Self_Teddy.glb matches
Binary file tools/anim-clips-authored/Hug_Teddy_Lying.glb matches
Binary file tools/anim-clips-authored/Kid_Look_Up_Hold.glb matches
Binary file tools/anim-clips-authored/Kiss_Forehead_Adult_Kneel.glb matches
Binary file tools/anim-clips-authored/Kiss_Forehead_Kid.glb matches
Binary file tools/anim-clips-authored/Kite_Fly.glb matches
Binary file tools/anim-clips-authored/Knock_Door.glb matches
Binary file tools/anim-clips-authored/Lift_Reach_Adult.glb matches
Binary file tools/anim-clips-authored/Lift_Reach_Kid.glb matches
Binary file tools/anim-clips-authored/March_In_Place.glb matches
Binary file tools/anim-clips-authored/Monkey_Scratch.glb matches
Binary file tools/anim-clips-authored/Nandri_Bow.glb matches
Binary file tools/anim-clips-authored/Nibble_Hands_Mouth.glb matches
Binary file tools/anim-clips-authored/Pat_Dough.glb matches
Binary file tools/anim-clips-authored/Pat_To_Sleep_Adult_Kneel.glb matches
Binary file tools/anim-clips-authored/Peekaboo.glb matches
Binary file tools/anim-clips-authored/Pig_Snout.glb matches
Binary file tools/anim-clips-authored/Point_Eyes.glb matches
Binary file tools/anim-clips-authored/Point_Up_Sky.glb matches
Binary file tools/anim-clips-authored/Point_Up_Sky_Hold.glb matches
Binary file tools/anim-clips-authored/Pottu_Adult.glb matches
Binary file tools/anim-clips-authored/Pottu_Kid.glb matches
Binary file tools/anim-clips-authored/Pout_Arms_Crossed.glb matches
Binary file tools/anim-clips-authored/Rabbit_Ears.glb matches
Binary file tools/anim-clips-authored/Rain_Fingers.glb matches
Binary file tools/anim-clips-authored/Reach_Up_Both.glb matches
Binary file tools/anim-clips-authored/Read_Book.glb matches
Binary file tools/anim-clips-authored/Roar_Claws.glb matches
Binary file tools/anim-clips-authored/Row_Boat_Seated.glb matches
Binary file tools/anim-clips-authored/Rub_Eyes.glb matches
Binary file tools/anim-clips-authored/Salute.glb matches
Binary file tools/anim-clips-authored/Shark_Chomp_Big.glb matches
Binary file tools/anim-clips-authored/Shark_Chomp_Small.glb matches
Binary file tools/anim-clips-authored/Shh_Finger_To_Lips.glb matches
Binary file tools/anim-clips-authored/Shh_Hold.glb matches
Binary file tools/anim-clips-authored/Shiver.glb matches
Binary file tools/anim-clips-authored/Shoo_Away.glb matches
Binary file tools/anim-clips-authored/Shoulder_Ride_Adult.glb matches
Binary file tools/anim-clips-authored/Shoulder_Ride_Kid.glb matches
Binary file tools/anim-clips-authored/Sleep_Beside_Adult_Bed.glb matches
Binary file tools/anim-clips-authored/Sleep_Beside_Adult_Floor.glb matches
Binary file tools/anim-clips-authored/Sleep_Beside_Kid_Bed.glb matches
Binary file tools/anim-clips-authored/Sleep_Beside_Kid_Floor.glb matches
Binary file tools/anim-clips-authored/Sleep_Hands_Cheek.glb matches
Binary file tools/anim-clips-authored/Sleep_Side_Kid_Floor.glb matches
Binary file tools/anim-clips-authored/Smell_Flower.glb matches
Binary file tools/anim-clips-authored/Sneeze.glb matches
Binary file tools/anim-clips-authored/So_Big_So_Small.glb matches
Binary file tools/anim-clips-authored/Sprout_Grow.glb matches
Binary file tools/anim-clips-authored/Squeak_Small.glb matches
Binary file tools/anim-clips-authored/Squeeze_Toy.glb matches
Binary file tools/anim-clips-authored/Steering_Wheel.glb matches
Binary file tools/anim-clips-authored/Steering_Wheel_Seated.glb matches
Binary file tools/anim-clips-authored/Stir_Pot.glb matches
Binary file tools/anim-clips-authored/Storytime_Listen_Seated.glb matches
Binary file tools/anim-clips-authored/Struggle_Trapped.glb matches
Binary file tools/anim-clips-authored/Sun_Circle_Arms.glb matches
Binary file tools/anim-clips-authored/Sweep_Floor.glb matches
Binary file tools/anim-clips-authored/Teapot_Tip.glb matches
Binary file tools/anim-clips-authored/Tiptoe_Reach_Counter.glb matches
Binary file tools/anim-clips-authored/Towel_Dry_Head.glb matches
Binary file tools/anim-clips-authored/Tug_Pull.glb matches
Binary file tools/anim-clips-authored/Tummy_Rub.glb matches
Binary file tools/anim-clips-authored/Twinkle_Fingers.glb matches
Binary file tools/anim-clips-authored/Vanakkam.glb matches
Binary file tools/anim-clips-authored/Vanakkam_Hold.glb matches
Binary file tools/anim-clips-authored/Vanakkam_Seated.glb matches
Binary file tools/anim-clips-authored/Walk_Hand_Hold_Adult_L.glb matches
Binary file tools/anim-clips-authored/Walk_Hand_Hold_Kid_R.glb matches
Binary file tools/anim-clips-authored/Warm_Hands.glb matches
Binary file tools/anim-clips-authored/Wash_Face.glb matches
Binary file tools/anim-clips-authored/Wash_Hands.glb matches
Binary file tools/anim-clips-authored/Wear_Necklace.glb matches
Binary file tools/anim-clips-authored/Wheels_Roll_Arms.glb matches
Binary file tools/anim-clips-authored/Wheels_Roll_Arms_Seated.glb matches
Binary file tools/anim-clips-authored/Wind_Blown.glb matches
Binary file tools/anim-clips-authored/Wings_Open_Close.glb matches
Binary file tools/anim-clips-authored/Wipe_Tears.glb matches
Binary file tools/anim-clips-authored/Wipers_Swish.glb matches
Binary file tools/anim-clips-authored/Wipers_Swish_Seated.glb matches
Binary file tools/anim-clips-authored/_superseded/Cook_Dosa_Flip_proto_v1.glb matches
Binary file tools/anim-clips-authored/_superseded/Cook_Stir_Pot_proto_v1.glb matches
Binary file tools/anim-clips-authored/_superseded/Vanakkam_proto_v1.glb matches
Binary file tools/anim-clips-norm/Acknowledging.glb matches
Binary file tools/anim-clips-norm/Agreeing.glb matches
Binary file tools/anim-clips-norm/Angry_Gesture.glb matches
Binary file tools/anim-clips-norm/Arm_Stretching.glb matches
Binary file tools/anim-clips-norm/Ball_Balance_Foot.glb matches
Binary file tools/anim-clips-norm/Ball_Balance_Foot_1.glb matches
Binary file tools/anim-clips-norm/Ball_Catch.glb matches
Binary file tools/anim-clips-norm/Ball_Catch_High.glb matches
Binary file tools/anim-clips-norm/Ball_Catch_Jump.glb matches
Binary file tools/anim-clips-norm/Ball_Catch_Running.glb matches
Binary file tools/anim-clips-norm/Ball_Catch_Side.glb matches
Binary file tools/anim-clips-norm/Ball_Drop_Kick.glb matches
Binary file tools/anim-clips-norm/Ball_Header.glb matches
Binary file tools/anim-clips-norm/Ball_Juggle_Kickup.glb matches
Binary file tools/anim-clips-norm/Ball_Juggle_Knee.glb matches
Binary file tools/anim-clips-norm/Ball_Juggle_Knee_1.glb matches
Binary file tools/anim-clips-norm/Ball_Kick.glb matches
Binary file tools/anim-clips-norm/Ball_Kick_RunUp.glb matches
Binary file tools/anim-clips-norm/Ball_Kick_Strong.glb matches
Binary file tools/anim-clips-norm/Ball_Miss_Comic.glb matches
Binary file tools/anim-clips-norm/Ball_Receive.glb matches
Binary file tools/anim-clips-norm/Ball_Roll_Underhand.glb matches
Binary file tools/anim-clips-norm/Ball_Throw_Overhand.glb matches
Binary file tools/anim-clips-norm/Ball_Throw_TwoHand.glb matches
Binary file tools/anim-clips-norm/Bored.glb matches
Binary file tools/anim-clips-norm/Breathing_Idle.glb matches
Binary file tools/anim-clips-norm/Briefcase_Idle.glb matches
Binary file tools/anim-clips-norm/Clapping.glb matches
Binary file tools/anim-clips-norm/Climb_Up.glb matches
Binary file tools/anim-clips-norm/Coach_Directing.glb matches
Binary file tools/anim-clips-norm/Come_Out_Of_Hiding.glb matches
Binary file tools/anim-clips-norm/Cow_Milking.glb matches
Binary file tools/anim-clips-norm/Dance_Finish_FistPump.glb matches
Binary file tools/anim-clips-norm/Dance_Finish_Wave.glb matches
Binary file tools/anim-clips-norm/Defeated_Slump.glb matches
Binary file tools/anim-clips-norm/Dig_And_Plant_Seeds.glb matches
Binary file tools/anim-clips-norm/Dizzy_Walk.glb matches
Binary file tools/anim-clips-norm/Fall_Flat_Comic.glb matches
Binary file tools/anim-clips-norm/Fallen_Idle_Comic.glb matches
Binary file tools/anim-clips-norm/Fast_Run.glb matches
Binary file tools/anim-clips-norm/Fishing_Cast.glb matches
Binary file tools/anim-clips-norm/Fishing_Idle.glb matches
Binary file tools/anim-clips-norm/Gangnam_Style.glb matches
Binary file tools/anim-clips-norm/Get_Up_Quick.glb matches
Binary file tools/anim-clips-norm/Ginga_Side.glb matches
Binary file tools/anim-clips-norm/Ginga_Step.glb matches
Binary file tools/anim-clips-norm/Happy_Hand_Gesture.glb matches
Binary file tools/anim-clips-norm/Happy_Idle.glb matches
Binary file tools/anim-clips-norm/Happy_Idle_1.glb matches
Binary file tools/anim-clips-norm/Head_Nod_Yes.glb matches
Binary file tools/anim-clips-norm/Hip_Hop_Bounce.glb matches
Binary file tools/anim-clips-norm/Hip_Hop_Bounce_Gentle.glb matches
Binary file tools/anim-clips-norm/Hip_Hop_Dancing.glb matches
Binary file tools/anim-clips-norm/Hip_Hop_Sidestep.glb matches
Binary file tools/anim-clips-norm/Holding_Walk.glb matches
Binary file tools/anim-clips-norm/House_Dancing.glb matches
Binary file tools/anim-clips-norm/Idle.glb matches
Binary file tools/anim-clips-norm/Jog_Sporty.glb matches
Binary file tools/anim-clips-norm/Joyful_Jump.glb matches
Binary file tools/anim-clips-norm/Jump.glb matches
Binary file tools/anim-clips-norm/Jump_Big.glb matches
Binary file tools/anim-clips-norm/Jump_Down.glb matches
Binary file tools/anim-clips-norm/Jump_Down_1.glb matches
Binary file tools/anim-clips-norm/Jump_Down_2.glb matches
Binary file tools/anim-clips-norm/Jump_Landing_Deep.glb matches
Binary file tools/anim-clips-norm/Jump_Push_Up.glb matches
Binary file tools/anim-clips-norm/Jumping_Up.glb matches
Binary file tools/anim-clips-norm/Kettlebell_Swing.glb matches
Binary file tools/anim-clips-norm/Kiss_Gesture.glb matches
Binary file tools/anim-clips-norm/Kneeling_Idle.glb matches
Binary file tools/anim-clips-norm/Kneeling_Pointing.glb matches
Binary file tools/anim-clips-norm/Laying_Idle.glb matches
Binary file tools/anim-clips-norm/Laying_Sleeping.glb matches
Binary file tools/anim-clips-norm/Left_Turn_90.glb matches
Binary file tools/anim-clips-norm/Lengthy_Head_Nod.glb matches
Binary file tools/anim-clips-norm/Looking_Around.glb matches
Binary file tools/anim-clips-norm/Nervous_Look_Around.glb matches
Binary file tools/anim-clips-norm/Old_Man_Idle.glb matches
Binary file tools/anim-clips-norm/Pain_Gesture.glb matches
Binary file tools/anim-clips-norm/Peek_Around_Left.glb matches
Binary file tools/anim-clips-norm/Peek_Around_Right.glb matches
Binary file tools/anim-clips-norm/Pick_Fruit.glb matches
Binary file tools/anim-clips-norm/Place_Object_Ground.glb matches
Binary file tools/anim-clips-norm/Plant_A_Plant.glb matches
Binary file tools/anim-clips-norm/Playing_Drums.glb matches
Binary file tools/anim-clips-norm/Pointing_Forward.glb matches
Binary file tools/anim-clips-norm/Praying_Kneel.glb matches
Binary file tools/anim-clips-norm/Quick_Hide.glb matches
Binary file tools/anim-clips-norm/Ready_To_Play_Idle.glb matches
Binary file tools/anim-clips-norm/Relay_Test_Run.glb matches
Binary file tools/anim-clips-norm/Relieved_Sigh.glb matches
Binary file tools/anim-clips-norm/Right_Turn_90.glb matches
Binary file tools/anim-clips-norm/Robot_Hip_Hop.glb matches
Binary file tools/anim-clips-norm/Rumba_Dancing.glb matches
Binary file tools/anim-clips-norm/Run_And_Leap.glb matches
Binary file tools/anim-clips-norm/Run_Curve_Left.glb matches
Binary file tools/anim-clips-norm/Run_Forward.glb matches
Binary file tools/anim-clips-norm/Run_Forward_1.glb matches
Binary file tools/anim-clips-norm/Run_To_Dive.glb matches
Binary file tools/anim-clips-norm/Run_To_Stop.glb matches
Binary file tools/anim-clips-norm/Running.glb matches
Binary file tools/anim-clips-norm/Running_Up_Stairs.glb matches
Binary file tools/anim-clips-norm/Sad_Idle.glb matches
Binary file tools/anim-clips-norm/Sad_Idle_1.glb matches
Binary file tools/anim-clips-norm/Samba_Dancing.glb matches
Binary file tools/anim-clips-norm/Scoop_Object_Ground.glb matches
Binary file tools/anim-clips-norm/Seated_Idle.glb matches
Binary file tools/anim-clips-norm/Shaking_Head_No.glb matches
Binary file tools/anim-clips-norm/Shoved_Spin.glb matches
Binary file tools/anim-clips-norm/Silly_Dancing.glb matches
Binary file tools/anim-clips-norm/Sitting.glb matches
Binary file tools/anim-clips-norm/Sitting_1.glb matches
Binary file tools/anim-clips-norm/Sitting_Clap.glb matches
Binary file tools/anim-clips-norm/Sitting_Idle.glb matches
Binary file tools/anim-clips-norm/Sitting_Laughing.glb matches
Binary file tools/anim-clips-norm/Situp_To_Idle.glb matches
Binary file tools/anim-clips-norm/Situps.glb matches
Binary file tools/anim-clips-norm/Skateboarding.glb matches
Binary file tools/anim-clips-norm/Slow_Run.glb matches
Binary file tools/anim-clips-norm/Sneaking_Left.glb matches
Binary file tools/anim-clips-norm/Sneaking_Right.glb matches
Binary file tools/anim-clips-norm/Standard_Idle.glb matches
Binary file tools/anim-clips-norm/Standing_Idle.glb matches
Binary file tools/anim-clips-norm/Standing_Ovation.glb matches
Binary file tools/anim-clips-norm/Standing_Up.glb matches
Binary file tools/anim-clips-norm/Standing_Up_1.glb matches
Binary file tools/anim-clips-norm/Startled_Step_Back.glb matches
Binary file tools/anim-clips-norm/Stop_Walking.glb matches
Binary file tools/anim-clips-norm/Swimming.glb matches
Binary file tools/anim-clips-norm/Swimming_To_Edge.glb matches
Binary file tools/anim-clips-norm/Swing_Dancing.glb matches
Binary file tools/anim-clips-norm/Swing_Drop.glb matches
Binary file tools/anim-clips-norm/Talking_On_Phone.glb matches
Binary file tools/anim-clips-norm/Teeter.glb matches
Binary file tools/anim-clips-norm/Thriller_Dance.glb matches
Binary file tools/anim-clips-norm/Toprock_Step.glb matches
Binary file tools/anim-clips-norm/Toprock_Step_1.glb matches
Binary file tools/anim-clips-norm/Treading_Water.glb matches
Binary file tools/anim-clips-norm/Trip_And_Recover.glb matches
Binary file tools/anim-clips-norm/Twist_Dance.glb matches
Binary file tools/anim-clips-norm/Use_Counter_Machine.glb matches
Binary file tools/anim-clips-norm/Walk_Backward.glb matches
Binary file tools/anim-clips-norm/Walk_Turn_Around.glb matches
Binary file tools/anim-clips-norm/Walking.glb matches
Binary file tools/anim-clips-norm/Walking_Gentle.glb matches
Binary file tools/anim-clips-norm/Watering.glb matches
Binary file tools/anim-clips-norm/Waving_1.glb matches
Binary file tools/anim-clips-norm/Waving_2.glb matches
Binary file tools/anim-clips-norm/Weight_Shift.glb matches
tools/scripts/blink-probe.ts:32:  { name: 'minnu', charFile: 'char-c1b32bdf.glb', variantDir: 'tools/blink-variants/Minnu_v42', heightMeters: 1.15, eyeY: 0.88 },
tools/scripts/check-set-conformance.ts:112:  { label: 'two children (Mintu + Minnu)', heights: [1.0, 1.15] },
tools/scripts/check-set-conformance.ts:116:  { label: 'adult + two children', heights: [1.65, 1.15, 1.0] },
tools/scripts/check-set-conformance.ts:118:  { label: 'TWO ADULTS + TWO CHILDREN (the bar)', heights: [1.65, 1.55, 1.15, 1.0] },
tools/scripts/check-set-conformance.ts:119:  { label: 'classroom: teacher + 6 children', heights: [1.55, 1.15, 1.0, 1.15, 1.0, 1.0, 1.15] },
tools/scripts/check-set-conformance.ts:427:      ? [1.55, 1.15, 1.0, 1.15, 1.0, 1.0, 1.15]
tools/scripts/check-set-conformance.ts:428:      : [1.65, 1.55, 1.15, 1.0]).toFixed(2)} m — frame WIDTH at the staging plane is `
tools/scripts/check_framing.py:30:MIN_LIGHT = 1.15     # ...and it is at least this much brighter than the interior
tools/scripts/framecheck/anchors/anchors-thatha.json:1:{"mixamorigLeftForeArm":{"n":24331,"min":[0.36815714051830534,1.0682589708619747,-0.09966766002681157],"max":[0.5968084125077295,1.1599763720544558,0.004911801204358233]},"mixamorigLeftFoot":{"n":37297,"min":[0.09399331198260512,-0.0000011974286
tools/scripts/framecheck/fc.bundle.js:32193:  var tonemapping_pars_fragment = "#ifndef saturate\n#define saturate( a ) clamp( a, 0.0, 1.0 )\n#endif\nuniform float toneMappingExposure;\nvec3 LinearToneMapping( vec3 color ) {\n	return saturate( toneMappingExposure * color );\n}\nvec3 ReinhardToneMappi
tools/scripts/grade_still.py:7:+ sat 1.15 gave 88 / 174 / 130; the DEFAULT, gamma 1.50 + sat 1.20, gives 80 / 185 / 121 -- the setting Arul picked
tools/scripts/grade_still.py:12:  py tools\\scripts\\grade_still.py in.jpg out.jpg [--gamma 1.35 --sat 1.15] one file (e.g. a thumbnail)
tools/scripts/probe-set-void.mjs:64: *                   1.15 / 1.00 m standing at the cast centre, so the bar can
tools/scripts/probe-set-void.mjs:284:const CAST_HEIGHTS_DEFAULT = [1.78, 1.55, 1.15, 1.0]
tools/scripts/tamil_pace.py:10:`SLEEP-SCRIPT-ANATOMY-2026-09-12.md` §11.2: *"79 wpm and 1.15 : 1.00 : 0.68 are
```

## Step 6 — Chiku / Minmini sizes visible in the repo: `git grep -n -i "chiku\|cartoon mouse\|firefly mascot" -- src tools`

```
src/data/assetManifest.json:849:    "name": "cartoon mouse",
src/data/assetManifest.json:850:    "relPath": "bulk models/cartoon mouse 3d model.glb",
src/data/assetManifest.json:854:    "description": "Chiku regen SUCCESS: strict T-pose, arms straight out, clean warm-brown coat with cream belly, big round ears, no chest-patch artifact. Rig-ready hero mouse.",
src/data/assetManifest.json:858:    "name": "cartoon mouse",
src/data/assetManifest.json:867:    "name": "cartoon mouse(1)",
src/data/assetManifest.json:868:    "relPath": "bulk models/cartoon mouse 3d model (1).glb",
src/data/assetManifest.json:876:    "name": "cartoon mouse(1)",
src/data/assetManifest.json:885:    "name": "cartoon mouse(2)",
src/data/assetManifest.json:890:    "description": "Third mouse: giant-eared Jerry-style, clean texture, cream belly. Arms very short and pressed to the body - NOT rig-friendly; static/background only. The T-pose cartoon mouse remains the Chiku hero.",
src/data/assetManifest.json:1938:    "name": "firefly mascot v3",
src/data/assetManifest.json:1939:    "relPath": "bulk models/firefly mascot v3.glb",
src/data/assetManifest.json:2424:    "name": "Minmini — Firefly Mascot model 1",
src/data/assetManifest.json:2429:    "description": "Minmini TV-firefly mascot CANDIDATE 1: retro TV head (taupe) with face on screen - BLUE iris eyes, dark high-contrast bezel, cyan glow patch; brown antennae, amber wings, green glow abdomen behind. More expressive face; antennae/bezel slightly asymmetric. Static mesh (no rig).",
src/data/assetManifest.json:2433:    "name": "Minmini — Firefly Mascot model 2",
src/data/assetManifest.json:2438:    "description": "Minmini TV-firefly mascot CANDIDATE 2: same TV-firefly design - BLACK button eyes, mid-grey softer bezel, symmetric upright antennae, squarer crisper body panels, deeper green abdomen. Cleaner build, less alive face. Static mesh (no rig).",
src/data/assetManifest.json:4188:    "name": "firefly mascot",
src/data/assetManifest.json:4197:    "name": "firefly mascot v4",
src/data/assetManifest.json:4198:    "relPath": "Non Human characters/firefly mascot v4.glb",
tools/scripts/build-nonhuman-bible-v16.py:10:    "... -> v15 (Kuyil koel) -> v16 (Minmini TV-FIREFLY mascot redesign
tools/scripts/build-nonhuman-bible-v16.py:65:assert '→ v16 (Minmini TV-FIREFLY mascot redesign CANONIZED' in s, \
tools/scripts/build-nonhuman-bible-v16.py:139: 'its changelog ends "… → v15 (Kuyil koel) → v16 (Minmini TV-FIREFLY mascot redesign '
tools/scripts/build-nonhuman-bible-v16.py:227:         '`… → v15 (Kuyil koel) → v16 (Minmini TV-FIREFLY mascot redesign CANONIZED…)` '
```
