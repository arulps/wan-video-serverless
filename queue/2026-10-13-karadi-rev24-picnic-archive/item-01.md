# item-01 — copy the picnic takes + sidecars + QC sheets into the song folder ($0.00)

1. `mkdir "C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_picnic-version\takes"` (the parent `_picnic-version\` and its
   `README.md` / `_gen\` already exist — Fable wrote them; do not touch them).
2. Copy, from `C:\Projects\opencode\video_image\songs\a12-karadi-w3\`:
   - `out\_rev1x-2026-10-13\*.mp4` and `*.json` (the 14 moved takes + any `-v1-picnic` fallbacks);
   - `out\V1A-seed30313-w3.mp4/.json`, `V2A…`, `V3A…`, `V4A…` (the four verse answers the trek still uses — copies);
   - `out\_qc\*-v1-picnic*` and the rev 1.x QC files CC moved earlier (whatever `out\_qc\_rev1x-2026-10-13\` holds, if that folder exists);
   - `cutplan.json` → `takes\cutplan-rev1.6.json` (the picnic slot plan for this tune).
   Use `copy` with no `/Y`; a prompt or "already exists" means skip and report.
3. Report: the listing of `takes\` with sizes (expect 18 distinct clip IDs across the mp4 files), and total MB.
4. Commit with `[skip ci]` and push: `queue/2026-10-13-karadi-rev24-picnic-archive`, `queue/A12-WATCH-LOG.md`.

**item-01.report.md:** the listing, any skipped files, the commit hash.
