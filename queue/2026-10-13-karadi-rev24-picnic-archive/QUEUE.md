# CC QUEUE — 2026-10-13 "Karadi rev 2.4 picnic archive": copy the picnic-version takes into the song folder (no API spend)

**Repo:** `C:\Projects\opencode\video_image` · **Machine:** Beast · **Executor:** CC (Sonnet is fine) · **Manager:** Fable.
Arul (13 Oct 23:55) will reuse the picnic clips for a picnic version of the song with a different tune, months from now. The repo's
`out\` is git-ignored, so the rev 1.x takes exist on Beast only. This queue **copies** them (never moves) into
`C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_picnic-version\takes\`, next to the README and plan files Fable wrote there.
**API spend: $0.00.**

## Hard limits
- No API calls, no render. Never print `.env` values, keys, the workspace id or any URL.
- **Copy only** (`copy`, never `move`/`del`). Never overwrite: if a destination file exists, skip it and say so.
- Write only into `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_picnic-version\takes\`. Nothing else in the song folder or the repo changes.
- Commit only this queue folder and `queue\A12-WATCH-LOG.md`, with `[skip ci]`.

## Protocol (markers in `queue\2026-10-13-karadi-rev24-picnic-archive\`)
As before. After item-01: `QUEUE END <time> est $0.00`, tell Arul "Karadi picnic archive done — Fable will review".
