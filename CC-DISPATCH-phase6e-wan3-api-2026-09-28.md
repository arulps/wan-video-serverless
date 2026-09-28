# CC-DISPATCH — Phase 6e: Wan 3.0 through Alibaba Model Studio (engine=wan3) + first test (2026-09-28)

**Repo:** `C:\Projects\opencode\video_image` · **Executor:** CC (Sonnet is fine). Parts A → E in one go.
**Budget: API spend ≤ $2.10 at list price** (3 Twinkle rows $1.50 + L01 $0.50; the console shows a 30% launch discount,
so expect ~$1.40). No pod. Standing rules: never print, echo or log `.env` values or the API key; edit `shots.csv`
cells, never restore it; report **full Windows paths**.
**Phase 6d (Wan 2.2 on a pod) is ON HOLD** — Wan 3.0 does first/last frames too. Its code is committed here unrun.

## 0 · Why (Arul, 2026-09-28)
OpenArt's quality comes from Wan 3.0, Alibaba's closed model (no weights, so not on our pods). Called directly from
Alibaba Model Studio it is $0.10/s at 720p list ($0.50 per 5 s clip; console shows 30% off now) vs OpenArt $0.60 and
our Phantom pod ~$0.39 average per shot at 720p. The runner keeps everything else (shot lists, refs, sidecars, strips,
laptop upscale); only the render step moves to the API.

## 1 · On disk (Fable; mock-tested; not committed)
| file | what |
|---|---|
| `comfy/wan3_api.py` | **new**. Model Studio client: builds the documented request (`wan3.0-video` / `-prime`, media `reference_image` or `first_frame`/`last_frame` as data URIs, `resolution`, `ratio`, `duration`, `seed`, `audio:false`, `prompt_extend:false`, `watermark:false`), submits with `X-DashScope-Async: enable`, polls every 15 s, downloads the mp4. Endpoint `https://{WorkspaceId}.{region}.maas.aliyuncs.com` (region from `DASHSCOPE_REGION`, here `ap-southeast-1` = Singapore, also the default). Reads `DASHSCOPE_API_KEY`, `DASHSCOPE_WORKSPACE_ID` (+ optional `DASHSCOPE_REGION`) from env or `.env` — only those keys; never printed; no key or video URL in sidecars. |
| `comfy/batch_runner.py` | `engine=wan3`: `ref` = up to 10 images named "Image 1..n" in a legend prepended to the prompt (labels from new column `ref_labels`, else cast names + "the set"); OR `keyframe`/`lastframe` as first/last frame (blank lastframe = none; the API forbids mixing refs and frames — refused before any call). `mode` = `standard` / `prime`. Shot `NEGATIVE:` becomes an "Avoid:" sentence (the API has no negative prompt). No 512-token limit for these rows. `--max-usd` is **required** for wan3 rows: each row reserves its list-price estimate before submitting and is refused if the cap would be exceeded. `--hosts api,api,api` = 3 tasks in parallel. `--wan3-prompt-extend` opts into Alibaba's prompt rewriting (off by default). Dry-run prints the model/resolution/ratio/estimate and the total. |
| `tests/test_wan3_mock.py` | **new**: fake Model Studio enforcing the documented rules (headers, data-URI images, refs vs frames, ≤10 refs, params, legend present); checks the refusal paths and that sidecars hold no secret/URL. PASS. |
| `songs/_ab7-2026-09-28-wan3/` | **new**: T04_w3 (Minnu + set), T08_w3 (Minmini front + side + set, explicit labels), T07_w3 (Minnu + Mintu + set) — the same shots, refs, seed and set plate as `_ab6` (Phantom 480p) and `_ab5` (Phantom 720p), at 1280x720, 5 s. |
| `songs/shorts-loops/shots.csv` | + columns `lastframe`, `ref_labels` (blank for old rows); + row `L01_w3` (720x1280, first = last = `keyframes/L01-start.png`). |
| everything listed in `CC-DISPATCH-phase6d-flf2v-L01-2026-09-28.md` §1 | flf2v engine, PULL_SKIP, x3 upscale — committed here, run later if needed. |

## Part A — prerequisites ($0)
1. **Credentials (Arul).** `.env` must contain `DASHSCOPE_API_KEY=`, `DASHSCOPE_WORKSPACE_ID=` and
   `DASHSCOPE_REGION=ap-southeast-1` (Singapore: the only region with standard `wan3.0-video` and its 30% launch
   discount; US (Virginia) offers only Prime at $0.14/s for 720p. Key, workspace and model must all be in Singapore). The workspace id is in the console's workspace settings. Check **without printing values**:
   `python -c "import sys; sys.path.insert(0,'comfy'); import wan3_api; print('credentials present:', wan3_api.credentials_present())"`
   If False: stop and tell Arul which of the two names is missing.
2. L01 keyframe: if `C:\Channel Contents\MinMiniKids\YT Shorts\keyframes\L01-start.png` (or .jpg) exists, fit it exactly
   as in 6d Part A1 into `songs\shorts-loops\keyframes\L01-start.png`. If not, L01_w3 is skipped (say so); the rest runs.

## Part B — tests + commit ($0)
```
python tests\test_wan3_mock.py            -> PASS
python tests\test_flf2v_mock.py           -> PASS
python -m py_compile comfy\wan3_api.py comfy\run_comfy.py comfy\batch_runner.py scripts\upscale_video.py
bash -n scripts/pod_bootstrap.sh
python comfy\batch_runner.py --song songs\_ab7-2026-09-28-wan3 --hosts api --dry-run      -> 3 rows, est $1.50, no MISSING
python comfy\batch_runner.py --song songs\shorts-loops --hosts api --dry-run --only L01_w3 -> est $0.50
git status   -- confirm NO .env, logs.txt, nil, out/, outputs/ in the add set
git add comfy/wan3_api.py tests/test_wan3_mock.py songs/_ab7-2026-09-28-wan3 CC-DISPATCH-phase6e-wan3-api-2026-09-28.md ^
        comfy/wan22_flf2v_api.json comfy/run_comfy.py comfy/batch_runner.py tests/test_flf2v_mock.py scripts/pod_bootstrap.sh scripts/upscale_video.py docs/SHOT-LIST-SPEC.md ^
        songs/shorts-loops/shots.csv songs/shorts-loops/shots/L01-flf.txt songs/shorts-loops/REVIEW-L01-2026-09-28.md songs/_ab6-2026-09-27-setplate/REVIEW-2026-09-27.md ^
        CC-REPORT-phase6c.md CC-DISPATCH-phase6d-flf2v-L01-2026-09-28.md
(+ songs/shorts-loops/keyframes/L01-start.png if A2 made it)
git commit -m "wan3 engine: Wan 3.0 via Alibaba Model Studio (refs or first/last frame, --max-usd cap); flf2v engine (Wan2.2, on hold); PULL_SKIP; x3 upscale [skip ci]"
git push
gh run list --workflow deploy.yml -L 1      -> no run for this commit
```

## Part C — render through the API (≤ $2.10 list)
```
python comfy\batch_runner.py --song songs\_ab7-2026-09-28-wan3 --hosts api,api,api --max-usd 1.60 --timeout-min 30 2>&1 | tee songs\_ab7-2026-09-28-wan3\batch_6e.log
python comfy\batch_runner.py --song songs\shorts-loops --only L01_w3 --hosts api --max-usd 0.55 --timeout-min 30 2>&1 | tee songs\shorts-loops\batch_6e.log
```
(The second only if A2 made the keyframe.) If the first task fails with an auth/region/model error: stop, report the
`code: message` line (it never contains the key) and do not retry by hand. Record each sidecar's `usage` block and
wall time. Arul checks the actual charge in the console (Usage & Billing) — note the time window of the run for him.

## Part D — upscale + comparison ($0, laptop)
Wan 3.0 outputs 30 fps, so no interpolation — upscale only (720p → x3):
```
cd songs\_ab7-2026-09-28-wan3\out ; mkdir 4K ; mkdir _qc
foreach ($c in "T04_w3-seed30313-w3","T08_w3-seed30313-w3","T07_w3-seed30313-w3") { powershell -ExecutionPolicy Bypass -File ..\..\..\scripts\upscale.ps1 "$c.mp4" -Dst "4K\$c-4K.mp4" -Height 2160 }
```
L01_w3 (if rendered): same with `-Height 3840`, in `songs\shorts-loops\out\4K\`, plus the loop checks from 6d Part C
(`-stream_loop 2` preview and first/last frame PNG — last frame index = frame count − 1, read it with ffprobe).
Comparison stills at t = 2.5 s (frame rates differ, so use time, not frame numbers), each pair side by side at 720 high:
```
ffmpeg -y -ss 2.5 -i T07_w3-seed30313-w3.mp4 -ss 2.5 -i ..\..\_ab6-2026-09-27-setplate\out\T07_set-seed30313-s30.mp4 -filter_complex "[0]scale=-2:720[a];[1]scale=-2:720[b];[a][b]hstack" -frames:v 1 _qc\T07-wan3-vs-phantom480.png
ffmpeg -y -ss 2.5 -i T04_w3-seed30313-w3.mp4 -ss 2.5 -i ..\..\_ab5-2026-09-23-phantom720\out\T04_ph720-seed30313-s6.mp4 -filter_complex "[0]scale=-2:720[a];[1]scale=-2:720[b];[a][b]hstack" -frames:v 1 _qc\T04-wan3-vs-phantom720.png
ffmpeg -y -ss 2.5 -i T08_w3-seed30313-w3.mp4 -ss 2.5 -i ..\..\_ab5-2026-09-23-phantom720\out\T08_ph720-seed30313-s30.mp4 -filter_complex "[0]scale=-2:720[a];[1]scale=-2:720[b];[a][b]hstack" -frames:v 1 _qc\T08-wan3-vs-phantom720.png
```
Copy the 4K files and the three comparison PNGs to `C:\Channel Contents\MinMiniKids\songs\Twinkle Twinkle\wan3-test\`
(and L01's to `C:\Channel Contents\MinMiniKids\YT Shorts\renders\L01\wan3\`).

## Part E — report (`CC-REPORT-phase6e.md`) + commit statuses
Commit `songs/_ab7-2026-09-28-wan3/shots.csv`, `songs/shorts-loops/shots.csv` (statuses) and the report with `[skip ci]`.
Report: A1 result (True/False only), A2, test outputs, commit hashes, per-row task id / wall s / `usage` / list-price
estimate, total estimate, the run's time window (for the console bill), upscale sidecar values, all full Windows paths.
**Do not judge the clips** — Fable checks: same house as the plate; Minnu/Mintu/Minmini on-model vs refs; two distinct
children; mouths; framing size; L01 loop closes; and Wan 3.0 vs Phantom side by side.
