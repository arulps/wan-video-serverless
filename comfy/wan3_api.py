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

Network (13 Oct 2026, A12 Gate A lost two renders to dropped TLS connections): polls and downloads retry on connection-level
errors (SSL, reset, timeout, remote disconnect) with a backoff — a dropped poll must never lose a paid task. A submit (POST) is
retried ONCE and only when the connection could not be opened at all (refused, DNS) — then nothing reached the service. A drop
during or after the upload (SSL, reset, timeout) is NOT retried: the service may have accepted the task, and a resubmit would pay
twice (CC, 13 Oct). That row fails and is reported; re-render it on a fresh queue. A finished task can be fetched by id without paying again:
  python comfy/wan3_api.py fetch <task_id> <dest.mp4> [--timeout-min 30]     (writes <dest>.json with recovered=true)
"""
import base64
import http.client
import json
import socket
import ssl
import sys
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
RETRY_BACKOFF_S = (5, 15, 30, 60, 60, 60)             # GET / download: up to 6 retries on connection-level errors
SUBMIT_RETRY_S = 20                                    # POST: one retry, connection-level errors only
TRANSIENT = (urllib.error.URLError, ssl.SSLError, socket.timeout, ConnectionError,
             http.client.RemoteDisconnected, http.client.IncompleteRead)


def _transient(e):
    """a connection-level failure (no HTTP response), as opposed to an HTTP error the service sent"""
    if isinstance(e, urllib.error.HTTPError):
        return e.code in (429, 500, 502, 503, 504)
    return isinstance(e, TRANSIENT)


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


def _call_once(method, url, body=None, timeout=120):
    v = _env()
    if not v["DASHSCOPE_API_KEY"]:
        raise RuntimeError("DASHSCOPE_API_KEY is not set (env or .env)")
    headers = {"Authorization": "Bearer " + v["DASHSCOPE_API_KEY"], "Content-Type": "application/json"}
    if method == "POST":
        headers["X-DashScope-Async"] = "enable"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def _http_message(method, url, e):
    try:
        j = json.loads(e.read())
        msg = "%s: %s" % (j.get("code"), j.get("message"))
    except Exception:
        msg = "HTTP %d" % e.code
    return "Wan3 API %s %s -> %s" % (method, url.split(".com", 1)[-1], msg)


def _never_sent(e):
    """True only when the connection was never opened (refused / DNS) — the request cannot have reached the service."""
    r = getattr(e, "reason", e)
    return isinstance(r, (ConnectionRefusedError, socket.gaierror)) or isinstance(e, (ConnectionRefusedError, socket.gaierror))


def _call(method, url, body=None, timeout=120, log=print):
    """GET: retried on connection-level errors (RETRY_BACKOFF_S). POST: one retry, and only if the connection was never
    opened (_never_sent) — any other failure may have reached the service, so it is not resubmitted (no double pay)."""
    waits = RETRY_BACKOFF_S if method == "GET" else (SUBMIT_RETRY_S,)
    for attempt in range(len(waits) + 1):
        try:
            return _call_once(method, url, body, timeout)
        except urllib.error.HTTPError as e:
            if attempt < len(waits) and method == "GET" and _transient(e):
                log("  wan3 %s: HTTP %d, retry %d in %d s" % (method, e.code, attempt + 1, waits[attempt]))
                time.sleep(waits[attempt]); continue
            raise RuntimeError(_http_message(method, url, e))
        except TRANSIENT as e:
            if method == "POST" and not _never_sent(e):
                raise RuntimeError("Wan3 API POST -> connection dropped during/after the upload (%s); NOT resubmitted (the "
                                   "service may have accepted it — check for an orphan task before re-rendering)" % type(e).__name__)
            if attempt < len(waits):
                log("  wan3 %s: connection error (%s), retry %d in %d s" % (method, type(e).__name__, attempt + 1, waits[attempt]))
                time.sleep(waits[attempt]); continue
            raise RuntimeError("Wan3 API %s %s -> connection failed after %d attempts: %s"
                               % (method, url.split(".com", 1)[-1], attempt + 1, e))


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
        j = _call("GET", base_url() + "/api/v1/tasks/" + task_id, log=log)
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


def download(url, dest, log=print):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 WanBatch"})
    for attempt in range(len(RETRY_BACKOFF_S) + 1):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = r.read()
            break
        except TRANSIENT as e:
            if attempt < len(RETRY_BACKOFF_S):
                log("  wan3 download: connection error (%s), retry %d in %d s" % (type(e).__name__, attempt + 1, RETRY_BACKOFF_S[attempt]))
                time.sleep(RETRY_BACKOFF_S[attempt]); continue
            raise RuntimeError("Wan3 download failed after %d attempts: %s" % (attempt + 1, e))
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    open(dest, "wb").write(data)
    return len(data)


def render(body, dest, timeout_min=30, log=print):
    """Submit, poll, download. Returns {"task_id", "wall_s", "bytes", "usage"} (no URLs, no secrets)."""
    t0 = time.time()
    tid = submit(body)
    log("  wan3 submitted task %s" % tid)
    out, usage = wait(tid, timeout_min, log=log)
    n = download(out["video_url"], dest, log=log)
    return {"task_id": tid, "wall_s": round(time.time() - t0, 1), "bytes": n, "usage": usage}


def fetch(task_id, dest, timeout_min=30, log=print):
    """Recover a task that was submitted but lost (dropped poll, crash): wait for it and download, paying nothing new.
    Writes <dest>.json (recovered=true, no URLs, no secrets). Returns the same dict as render()."""
    t0 = time.time()
    out, usage = wait(task_id, timeout_min, log=log)
    n = download(out["video_url"], dest, log=log)
    shot_id = os.path.basename(dest).split("-seed")[0]
    sidecar = {"shot_id": shot_id, "engine": "wan3", "task_id": task_id, "usage": usage, "bytes": n, "recovered": True,
               "recovered_at": time.strftime("%Y-%m-%d %H:%M:%S"), "wall_s": round(time.time() - t0, 1),
               "note": "fetched by task id after the runner lost the connection; the prompt/refs are in shots/ and the runsheet"}
    json.dump(sidecar, open(dest[:-4] + ".json", "w", encoding="utf-8"), indent=1)
    return {"task_id": task_id, "wall_s": sidecar["wall_s"], "bytes": n, "usage": usage}


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "fetch":
        tmin = 30
        if "--timeout-min" in sys.argv:
            tmin = float(sys.argv[sys.argv.index("--timeout-min") + 1])
        r = fetch(sys.argv[2], sys.argv[3], timeout_min=tmin)
        print("fetched task %s -> %s (%d bytes, usage %s)" % (r["task_id"], sys.argv[3], r["bytes"], r["usage"]))
    else:
        sys.exit("usage: python comfy/wan3_api.py fetch <task_id> <dest.mp4> [--timeout-min N]")
