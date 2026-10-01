# CC QUEUE — 2026-09-30 "Tamil voice test": C1 red ball with a Tamil voice (2 variants) on Wan 3.0

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine) · **Manager:** Fable (reviews after).
Arul wants to hear a Short with Tamil speech instead of English. Same shot as the published-ready `C1_w3` (Minnu, red ball,
same seed 30313), only the voice lines change, from the runsheet's Tamil recording sheet:
இது என்ன நிறம்? → சிவப்பு! → சிவப்பு பந்து!
- `C1_w3ta`: lines written in Tamil script.
- `C1_w3tr`: the same lines in Latin transliteration (Idhu enna niram? / Sivappu! / Sivappu pandhu!) — to see which Wan pronounces better.
Dry-run by Fable: 2 rows, $1.00.

## Hard limits
- **API spend ≤ $1.20 at list price.** No pod, no GPU, no upscale. Only these 2 rows; no extra seeds; failures reported, not re-run.
- Never print, echo or log `.env` values, the API key, the workspace id or any video URL.
- Never touch RunPod. Never restore a `shots.csv`. Commits carry `[skip ci]`.
- Do not touch `C1-metadata.md`, `USE-CLIPS.md` or existing clips in `renders-learning\C1\`; only add files.

## Protocol (markers in `queue\2026-09-30-tamil-voice-test\`)
As in `queue\2026-09-28-shorts-retakes1`: LOG.md start/done lines, `item-N.report.md`, `item-N.done`, `item-N.blocked` + stop.
After item-02: `QUEUE END <time> est $<x>`, tell Arul "Tamil voice test done — ask Fable to review queue\2026-09-30-tamil-voice-test".
