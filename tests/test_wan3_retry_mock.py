"""Mock test for wan3_api retries + fetch (no network, no secrets). Fable, 13 Oct 2026.
Scenarios: (1) a poll that drops twice then succeeds -> the task is not lost; (2) a submit that drops once -> retried once;
(3) a submit that drops twice -> fails (never a third POST); (4) an HTTP 400 on submit -> no retry; (5) download drops then
succeeds; (6) fetch(task_id) writes the file + a recovered sidecar; (7) a failed task raises."""
import io, json, os, ssl, sys, tempfile, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "comfy"))
os.environ["DASHSCOPE_API_KEY"] = "test"; os.environ["DASHSCOPE_WORKSPACE_ID"] = "ws"
import wan3_api as W
W.RETRY_BACKOFF_S = (0, 0, 0, 0, 0, 0); W.SUBMIT_RETRY_S = 0; W.POLL_S = 0
calls = []
class R:
    def __init__(self, payload): self.payload = payload
    def __enter__(self): return self
    def __exit__(self, *a): pass
    def read(self): return self.payload
def fake_urlopen(script):
    it = iter(script)
    def urlopen(req, timeout=0):
        url = req.full_url if hasattr(req, "full_url") else req
        calls.append((getattr(req, "method", "GET"), url.split(".com", 1)[-1] if ".com" in url else url))
        step = next(it)
        if isinstance(step, Exception): raise step
        return R(step if isinstance(step, bytes) else json.dumps(step).encode())
    return urlopen
def http_err(code):
    return urllib.error.HTTPError("u", code, "m", {}, io.BytesIO(json.dumps({"code": "Bad", "message": "x"}).encode()))
ok_running = {"output": {"task_status": "RUNNING"}}
ok_done = {"output": {"task_status": "SUCCEEDED", "video_url": "https://x.com/v.mp4"}, "usage": {"s": 7}}
n = 0
def check(name, cond):
    global n; n += 1; assert cond, name; print("  ok", n, name)
# 1 poll drops twice then succeeds; download fine
W.urllib.request.urlopen = fake_urlopen([ssl.SSLError("drop"), ConnectionResetError(), ok_running, ok_done, b"MP4DATA"])
d = tempfile.mkdtemp(); dest = os.path.join(d, "O1-seed1-w3.mp4")
out, usage = W.wait("t1", log=lambda *a: None); nb = W.download(out["video_url"], dest, log=lambda *a: None)
check("poll survives two drops", out["task_status"] == "SUCCEEDED" and nb == 7)
# 2 submit drops once -> retried once -> ok
calls.clear(); W.urllib.request.urlopen = fake_urlopen([ssl.SSLError("drop"), {"output": {"task_id": "t2"}}])
check("submit retried once", W.submit({"x": 1}) == "t2" and len(calls) == 2)
# 3 submit drops twice -> fails, exactly 2 POSTs
calls.clear(); W.urllib.request.urlopen = fake_urlopen([ssl.SSLError("drop"), ConnectionResetError(), {"output": {"task_id": "t3"}}])
try: W.submit({"x": 1}); check("submit never a third POST", False)
except RuntimeError as e: check("submit never a third POST", len(calls) == 2 and "connection failed after 2 attempts" in str(e))
# 4 HTTP 400 on submit -> no retry
calls.clear(); W.urllib.request.urlopen = fake_urlopen([http_err(400), {"output": {"task_id": "t4"}}])
try: W.submit({"x": 1}); check("400 not retried", False)
except RuntimeError as e: check("400 not retried", len(calls) == 1 and "Bad: x" in str(e))
# 5 download drops then succeeds
W.urllib.request.urlopen = fake_urlopen([ssl.SSLError("drop"), b"ABC"])
check("download retried", W.download("https://x.com/v.mp4", dest, log=lambda *a: None) == 3)
# 6 fetch by id writes file + sidecar
W.urllib.request.urlopen = fake_urlopen([ok_running, ok_done, b"MP4DATA"])
r = W.fetch("t6", dest, log=lambda *a: None); sc = json.load(open(dest[:-4] + ".json"))
check("fetch writes sidecar", r["bytes"] == 7 and sc["recovered"] is True and sc["shot_id"] == "O1" and sc["task_id"] == "t6"
      and "url" not in json.dumps(sc).lower())
# 7 failed task raises
W.urllib.request.urlopen = fake_urlopen([{"output": {"task_status": "FAILED", "code": "E", "message": "boom"}}])
try: W.wait("t7", log=lambda *a: None); check("failed task raises", False)
except RuntimeError as e: check("failed task raises", "FAILED" in str(e))
# 8 GET 503 is retried, 404 is not
calls.clear(); W.urllib.request.urlopen = fake_urlopen([http_err(503), ok_done])
check("503 retried", W._call("GET", "https://a.com/t", log=lambda *a: None)["output"]["task_status"] == "SUCCEEDED" and len(calls) == 2)
calls.clear(); W.urllib.request.urlopen = fake_urlopen([http_err(404), ok_done])
try: W._call("GET", "https://a.com/t", log=lambda *a: None); check("404 not retried", False)
except RuntimeError: check("404 not retried", len(calls) == 1)
print("PASS test_wan3_retry_mock: %d checks" % n)
