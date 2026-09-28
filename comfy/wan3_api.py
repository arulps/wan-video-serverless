"""Wan 3.0 on Alibaba Cloud Model Studio (DashScope), for batch_runner engine=wan3.

API (Wan3.0 Video Generation API Reference, read 2026-09-28):
  POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
       headers: Authorization: Bearer <key>, X-DashScope-Async: enable, Content-Type: application/json
       body: {"model": "wan3.0-video" | "wan3.0-video-prime",
              "input": {"prompt": ..., "media": [{"type": "reference_image"|"first_frame"|"last_frame", "url": <URL or data URI>}]},
              "parameters": {"resolution": "480P"|"720P"|"1080P", "ratio": "16:9"|"9:16"|..., "duration": 2..30,
                             "audio": bool, "seed": int, "prompt_extend": bool, "watermark": bool}}
  GET  https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}
       -> output.task_status PENDING|RUNNING|SUCCEEDED|FAILED|CANCELED|UNKNOWN, output.video_url (valid 24 h)
Rules: first_frame/last_frame are mutually exclusive with reference_image; max 10 reference images; images
PNG/JPEG/WEBP/BMP, 240-8000 px a side, <= 20 MB, may be sent as data URIs; references are named in the prompt
"Image 1", "Image 2" ... in media order; no negative prompt; output mp4 at 30 fps.

Secrets: DASHSCOPE_API_KEY and DASHSCOPE_WORKSPACE_ID come from the environment, or from the repo's .env
(only those keys are read). They are never printed or written to a sidecar.
"""
import base64
import json
import mimetypes
import os
import time
import urllib.error
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_KEYS = ("DASHSCOPE_API_KEY", "DASHSCOPE_WORKSPACE_ID", "DASHSCOPE_REGION", "DASHSCOPE_BASE_URL")
MODELS = {"standard": "wan3.0-video", "prime": "wan3.0-video-prime"}
# list price, USD per output second (Model Studio console, Singapore, 2026-09-28). Standard shows a limited-time
# 30% discount there; Prime (the only Wan 3.0 model offered in the US region) is dearer and undiscounted.
RATE_USD_PER_S = {"standard": {"480P": 0.05, "720P": 0.10, "1080P": 0.20},
                  "prime":    {"480P": 0.068, "720P": 0.14, "1080P": 0.28}}
RATIOS = {"16:9": 16 / 9, "9:16": 9 / 16, "4:3": 4 / 3, "3:4": 3 / 4, "1:1": 1.0, "21:9": 21 / 9}
MAX_REFS = 10
POLL_S = float(os.environ.get("WAN3_POLL_S", "15"))   # API guidance: poll every 15 s


def _env():
    vals = {k: os.environ.get(k, "") for k in ENV_KEYS}
    envfile = os.path.join(REPO_ROOT, ".env")
    if (not vals["DASHSCOPE_API_KEY"] or not vals["DASHSCOPE_WORKSPACE_ID"]) and os.path.exists(envfile):
        for line in open(envfile, encoding="utf-8", errors="replace"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip().replace("export ", "")
            if k in ENV_KEYS and not vals[k]:
                vals[k] = v.strip().strip('"').strip("'")
    return vals


def credentials_present():
    v = _env()
    return bool(v["DASHSCOPE_API_KEY"]) and (bool(v["DASHSCOPE_WORKSPACE_ID"]) or bool(v["DASHSCOPE_BASE_URL"]))


def base_url():
    v = _env()
    if v["DASHSCOPE_BASE_URL"]:
        return v["DASHSCOPE_BASE_URL"].rstrip("/")
    if not v["DASHSCOPE_WORKSPACE_ID"]:
        raise RuntimeError("DASHSCOPE_WORKSPACE_ID is not set (env or .env)")
    return "https://%s.%s.maas.aliyuncs.com" % (v["DASHSCOPE_WORKSPACE_ID"], v["DASHSCOPE_REGION"] or "ap-southeast-1")


def size_to_resolution(width, height):
    short = min(width, height)
    res = {480: "480P", 720: "720P", 1080: "1080P"}.get(short)
    if not res:
        raise RuntimeError("engine=wan3 needs a 480/720/1080 short side, got %dx%d" % (width, height))
    r = width / float(height)
    ratio = min(RATIOS, key=lambda k: abs(RATIOS[k] - r))
    if abs(RATIOS[ratio] - r) > 0.06:
        raise RuntimeError("engine=wan3: %dx%d is not a supported ratio (%s)" % (width, height, ", ".join(RATIOS)))
    return res, ratio


def estimate_usd(resolution, duration_s, mode="standard"):
    return round(RATE_USD_PER_S[mode][resolution] * duration_s, 2)


def data_uri(path):
    size = os.path.getsize(path)
    if size > 20 * 1024 * 1024:
        raise RuntimeError("image over 20 MB (API limit): %s" % path)
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return "data:%s;base64,%s" % (mime, base64.b64encode(open(path, "rb").read()).decode())


def build_request(prompt, refs=(), first_frame=None, last_frame=None, resolution="720P", ratio="16:9",
                  duration=5, seed=None, mode="standard", prompt_extend=False, audio=False):
    """refs: reference image paths (Image 1..n). first_frame/last_frame: paths. Returns the JSON body (dict)."""
    refs = list(refs or [])
    if refs and (first_frame or last_frame):
        raise RuntimeError("engine=wan3: reference images and first/last frames cannot be combined (API rule)")
    if len(refs) > MAX_REFS:
        raise RuntimeError("engine=wan3: at most %d reference images, got %d" % (MAX_REFS, len(refs)))
    if not 2 <= int(duration) <= 30:
        raise RuntimeError("engine=wan3: duration must be 2-30 s, got %s" % duration)
    media = [{"type": "reference_image", "url": data_uri(p)} for p in refs]
    if first_frame:
        media.append({"type": "first_frame", "url": data_uri(first_frame)})
    if last_frame:
        media.append({"type": "last_frame", "url": data_uri(last_frame)})
    params = {"resolution": resolution, "duration": int(duration), "audio": bool(audio),
              "prompt_extend": bool(prompt_extend), "watermark": False}
    # with a first frame the output ratio follows the image; otherwise pin it
    params["ratio"] = "adaptive" if first_frame else ratio
    if seed is not None:
        params["seed"] = int(seed) % 2147483648
    body = {"model": MODELS[mode], "input": {"prompt": prompt}, "parameters": params}
    if media:
        body["input"]["media"] = media
    return body


def _call(method, url, body=None, timeout=120):
    v = _env()
    if not v["DASHSCOPE_API_KEY"]:
        raise RuntimeError("DASHSCOPE_API_KEY is not set (env or .env)")
    headers = {"Authorization": "Bearer " + v["DASHSCOPE_API_KEY"], "Content-Type": "application/json"}
    if method == "POST":
        headers["X-DashScope-Async"] = "enable"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            j = json.loads(e.read())
            msg = "%s: %s" % (j.get("code"), j.get("message"))
        except Exception:
            msg = "HTTP %d" % e.code
        raise RuntimeError("Wan3 API %s %s -> %s" % (method, url.split(".com", 1)[-1], msg))


def submit(body):
    j = _call("POST", base_url() + "/api/v1/services/aigc/video-generation/video-synthesis", body)
    tid = (j.get("output") or {}).get("task_id")
    if not tid:
        raise RuntimeError("Wan3 API: no task_id in response (%s)" % {k: j.get(k) for k in ("code", "message")})
    return tid


def wait(task_id, timeout_min=30, stop=None, log=print):
    deadline = time.time() + timeout_min * 60
    last = ""
    while time.time() < deadline:
        j = _call("GET", base_url() + "/api/v1/tasks/" + task_id)
        out = j.get("output") or {}
        st = out.get("task_status", "")
        if st != last:
            log("  wan3 task %s: %s" % (task_id, st)); last = st
        if st == "SUCCEEDED":
            return out, j.get("usage") or {}
        if st in ("FAILED", "CANCELED", "UNKNOWN"):
            raise RuntimeError("Wan3 task %s %s: %s %s" % (task_id, st, out.get("code", ""), out.get("message", "")))
        time.sleep(POLL_S)
    raise TimeoutError("Wan3 task %s not done after %d min (still billable; check the console)" % (task_id, timeout_min))


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 WanBatch"})
    with urllib.request.urlopen(req, timeout=600) as r:
        data = r.read()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "wb").write(data)
    return len(data)


def render(body, dest, timeout_min=30, log=print):
    """Submit, poll, download. Returns {"task_id", "wall_s", "bytes", "usage"} (no URLs, no secrets)."""
    t0 = time.time()
    tid = submit(body)
    log("  wan3 submitted task %s" % tid)
    out, usage = wait(tid, timeout_min, log=log)
    n = download(out["video_url"], dest)
    return {"task_id": tid, "wall_s": round(time.time() - t0, 1), "bytes": n, "usage": usage}
