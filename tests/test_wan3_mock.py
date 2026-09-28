"""Mock DashScope test for engine=wan3. No network, no key, no spend.

python tests/test_wan3_mock.py  -> batch_runner against a local fake Model Studio that enforces the documented
API rules (headers, media types, refs vs first/last frame exclusivity, <=10 refs, data-URI images, params)."""
import base64, http.server, json, os, shutil, subprocess, sys, tempfile, threading, uuid

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS, BODIES, POLLS = {}, [], {}


def validate(headers, body):
    assert headers.get("Authorization") == "Bearer sk-test", "auth header"
    assert headers.get("X-DashScope-Async") == "enable", "async header"
    assert body["model"] in ("wan3.0-video", "wan3.0-video-prime")
    media = body["input"].get("media", [])
    types = [m["type"] for m in media]
    refs = types.count("reference_image")
    assert not (refs and ({"first_frame", "last_frame"} & set(types))), "refs mixed with frames"
    assert refs <= 10
    for m in media:
        assert m["url"].startswith("data:image/"), "image must be a data URI"
        base64.b64decode(m["url"].split(",", 1)[1])
    p = body["parameters"]
    assert p["resolution"] in ("480P", "720P", "1080P") and 2 <= p["duration"] <= 30
    assert p["audio"] is False and p["prompt_extend"] is False
    assert p["ratio"] == ("adaptive" if "first_frame" in types else p["ratio"])
    if refs:
        for i in range(refs):
            assert "Image %d is" % (i + 1) in body["input"]["prompt"], "legend missing Image %d" % (i + 1)
    assert "sk-test" not in body["input"]["prompt"]


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, obj, ctype="application/json"):
        data = obj if isinstance(obj, bytes) else json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", ctype); self.end_headers(); self.wfile.write(data)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        try:
            validate(self.headers, body)
        except AssertionError as e:
            return self._send(400, {"code": "InvalidParameter", "message": str(e)})
        tid = uuid.uuid4().hex; TASKS[tid] = body; BODIES.append(body); POLLS[tid] = 0
        self._send(200, {"output": {"task_status": "PENDING", "task_id": tid}, "request_id": "r"})
    def do_GET(self):
        if self.path.startswith("/api/v1/tasks/"):
            assert self.headers.get("Authorization") == "Bearer sk-test"
            tid = self.path.rsplit("/", 1)[-1]; POLLS[tid] += 1
            if POLLS[tid] < 2:
                return self._send(200, {"output": {"task_id": tid, "task_status": "RUNNING"}})
            return self._send(200, {"output": {"task_id": tid, "task_status": "SUCCEEDED",
                                               "video_url": "http://127.0.0.1:%d/v/%s.mp4" % (H.port, tid)},
                                    "usage": {"duration": 5.0, "fps": 30, "SR": 720}})
        if self.path.startswith("/v/"):
            return self._send(200, open(H.mp4, "rb").read(), "video/mp4")
        self._send(404, {})


def main():
    tmp = tempfile.mkdtemp(prefix="wan3-test-")
    H.mp4 = os.path.join(tmp, "fake.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=teal:s=256x144:d=5:r=30", "-pix_fmt", "yuv420p", H.mp4], check=True)
    song = os.path.join(tmp, "song")
    for d in ("shots", "refs", "keyframes"):
        os.makedirs(os.path.join(song, d))
    for n in ("refs/a.png", "refs/b.png", "refs/set.png", "keyframes/k.png"):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=white:s=320x320", "-frames:v", "1", os.path.join(song, n)], check=True)
    open(os.path.join(song, "world.txt"), "w").write("EXTERIOR NIGHT.\n\nA terrace.\n")
    open(os.path.join(song, "characters.txt"), "w").write("Minnu: girl.\nMintu: boy.\n")
    open(os.path.join(song, "shots", "s.txt"), "w").write("SHOT: medium\nMOTION: they wave\nNEGATIVE: open mouth, teeth\n")
    open(os.path.join(song, "shots.csv"), "w").write(
        "shot_id,cast,ref,prompt,duration_s,mode,engine,keyframe,lastframe,ref_labels,seed,size,status\n"
        "R2,Minnu+Mintu,refs/a.png|refs/b.png|refs/set.png,shots/s.txt,5,,wan3,,,,30313,1280x720,\n"
        "LOOP,Minnu,,shots/s.txt,5,prime,wan3,keyframes/k.png,keyframes/k.png,,30313,720x1280,\n"
        "BAD,Minnu,refs/a.png,shots/s.txt,5,,wan3,keyframes/k.png,,,30313,1280x720,\n"
        "CAP,Minnu,refs/a.png,shots/s.txt,5,,wan3,,,,30313,1920x1080,\n")
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); H.port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    env = dict(os.environ, DASHSCOPE_API_KEY="sk-test", DASHSCOPE_BASE_URL="http://127.0.0.1:%d" % H.port, WAN3_POLL_S="0.05")
    runner = [sys.executable, os.path.join(REPO, "comfy", "batch_runner.py"), "--song", song]
    d = subprocess.run(runner + ["--hosts", "api", "--dry-run"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    assert "estimated $" in d.stdout and "Image 1 is Minnu" in d.stdout, d.stdout[-1500:]
    # no --max-usd -> refused before any submission
    n = subprocess.run(runner + ["--hosts", "api"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    assert n.returncode != 0 and "--max-usd is required" in (n.stdout + n.stderr) and not BODIES
    # cap $1.20: R2 (standard 720p $0.50) + LOOP (prime 720p $0.70) fit, CAP (1080p, $1.00) must be refused; BAD fails on the API rule
    r = subprocess.run(runner + ["--hosts", "api,api", "--max-usd", "1.20"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    out = r.stdout + r.stderr
    print(out[-3000:])
    rows = {l.split(",")[0]: l.rsplit(",", 1)[-1] for l in open(os.path.join(song, "shots.csv")).read().splitlines()[1:]}
    assert rows["R2"] == "done" and rows["LOOP"] == "done", rows
    assert rows["BAD"] == "failed" and rows["CAP"] == "failed", rows
    assert "cannot be combined" in out and "would be exceeded" in out
    assert len(BODIES) == 2
    loop = [b for b in BODIES if b["model"] == "wan3.0-video-prime"][0]
    assert [m["type"] for m in loop["input"]["media"]] == ["first_frame", "last_frame"]
    r2 = [b for b in BODIES if b["model"] == "wan3.0-video"][0]
    assert "Image 3 is the set" in r2["input"]["prompt"] and "Avoid: open mouth, teeth." in r2["input"]["prompt"]
    side = json.load(open(os.path.join(song, "out", "R2-seed30313-w3.json")))
    assert "sk-test" not in json.dumps(side) and "video_url" not in json.dumps(side)
    assert os.path.exists(os.path.join(song, "out", "_qc", "R2-strip.png"))
    print("PASS: refs+labels, loop first/last frame (prime), API-rule refusal, --max-usd cap, no secrets/URLs in sidecars")
    shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
