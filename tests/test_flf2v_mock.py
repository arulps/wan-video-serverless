"""Mock-ComfyUI test for engine=flf2v (Wan2.2 first-last-frame). No GPU, no network.

python tests/test_flf2v_mock.py   -> runs batch_runner against a local fake ComfyUI that checks every
submitted workflow: links resolve, node 13 is WanFirstLastFrameToVideo with both frames, the two
KSamplerAdvanced split one schedule, LoRAs present only in distilled mode. Needs ffmpeg for the fake mp4."""
import http.server, json, os, shutil, subprocess, sys, tempfile, threading, uuid

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBMITTED = []
UPLOADS = []


def check(wf):
    for nid, node in wf.items():
        for k, v in node["inputs"].items():
            if isinstance(v, list) and len(v) == 2 and isinstance(v[0], str):
                assert v[0] in wf, "node %s.%s links to missing node %s" % (nid, k, v[0])
    n13 = wf["13"]
    assert n13["class_type"] == "WanFirstLastFrameToVideo"
    assert n13["inputs"]["start_image"] == ["11", 0] and n13["inputs"]["end_image"] == ["12", 0]
    hi, lo = wf["14"]["inputs"], wf["15"]["inputs"]
    assert hi["add_noise"] == "enable" and lo["add_noise"] == "disable"
    assert hi["end_at_step"] == lo["start_at_step"] == hi["steps"] // 2
    assert lo["latent_image"] == ["14", 0] and hi["latent_image"] == ["13", 2]
    assert hi["noise_seed"] == lo["noise_seed"]
    lora = "5" in wf
    assert lora == ("6" in wf)
    if lora:
        assert wf["7"]["inputs"]["model"] == ["5", 0] and hi["steps"] == 4 and hi["cfg"] == 1.0 and wf["7"]["inputs"]["shift"] == 5.0
    else:
        assert wf["7"]["inputs"]["model"] == ["1", 0] and wf["8"]["inputs"]["model"] == ["2", 0]
        assert hi["steps"] == 20 and hi["cfg"] == 3.5 and wf["7"]["inputs"]["shift"] == 8.0
    for t in ("9", "10"):
        assert "__" not in wf[t]["inputs"]["text"]


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, body, ctype="application/json"):
        self.send_response(code); self.send_header("Content-Type", ctype); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))
        if self.path == "/upload/image":
            name = body.split(b'filename="')[1].split(b'"')[0].decode(); UPLOADS.append(name)
            return self._send(200, json.dumps({"name": name, "subfolder": ""}).encode())
        if self.path == "/prompt":
            wf = json.loads(body)["prompt"]
            try:
                check(wf)
            except AssertionError as e:
                return self._send(400, json.dumps({"error": str(e)}).encode())
            SUBMITTED.append(wf); pid = uuid.uuid4().hex; H.last = pid
            return self._send(200, json.dumps({"prompt_id": pid}).encode())
    def do_GET(self):
        if self.path.startswith("/history/"):
            pid = self.path.split("/")[-1]
            return self._send(200, json.dumps({pid: {"status": {"status_str": "success"},
                "outputs": {"18": {"images": [{"filename": "x.mp4", "subfolder": "video", "type": "output"}]}}}}).encode())
        if self.path.startswith("/view"):
            return self._send(200, open(H.mp4, "rb").read(), "video/mp4")
        if self.path.startswith("/queue"):
            return self._send(200, b'{"queue_running":[],"queue_pending":[]}')
        self._send(404, b"{}")


def main():
    tmp = tempfile.mkdtemp(prefix="flf2v-test-")
    H.mp4 = os.path.join(tmp, "fake.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=teal:s=144x256:d=5.06:r=16", "-pix_fmt", "yuv420p", H.mp4], check=True)
    song = os.path.join(tmp, "song"); os.makedirs(os.path.join(song, "shots")); os.makedirs(os.path.join(song, "keyframes"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=white:s=720x1280", "-frames:v", "1",
                    os.path.join(song, "keyframes", "L01-start.png")], check=True)
    shutil.copy(os.path.join(song, "keyframes", "L01-start.png"), os.path.join(song, "keyframes", "L01-end.png"))
    open(os.path.join(song, "world.txt"), "w").write("INTERIOR DAY.\n\nA living room.\n")
    open(os.path.join(song, "characters.txt"), "w").write("Minnu: girl; keep exactly as in the first frame.\n")
    open(os.path.join(song, "shots", "L01.txt"), "w").write("SHOT: medium\nMOTION: she pops out and hides again\n")
    open(os.path.join(song, "shots.csv"), "w").write(
        "shot_id,cast,ref,prompt,duration_s,mode,engine,keyframe,lastframe,seed,size,status\n"
        "A,Minnu,,shots/L01.txt,5,distilled,flf2v,keyframes/L01-start.png,,30313,720x1280,\n"
        "B,Minnu,,shots/L01.txt,5,full,flf2v,keyframes/L01-start.png,keyframes/L01-end.png,30313,720x1280,\n")
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    host = "http://127.0.0.1:%d" % srv.server_address[1]
    r = subprocess.run([sys.executable, os.path.join(REPO, "comfy", "batch_runner.py"), "--song", song, "--hosts", host],
                       capture_output=True, text=True)
    print(r.stdout[-2500:], r.stderr[-1500:])
    rows = open(os.path.join(song, "shots.csv")).read()
    assert len(SUBMITTED) == 2, "submitted %d" % len(SUBMITTED)
    assert "5" in SUBMITTED[0] and "5" not in SUBMITTED[1]
    assert SUBMITTED[0]["11"]["inputs"]["image"] == SUBMITTED[0]["12"]["inputs"]["image"]          # loop: same frame
    assert SUBMITTED[1]["12"]["inputs"]["image"] == "L01-end.png"
    assert rows.count(",done") == 2, rows
    side = json.load(open(os.path.join(song, "out", "A-seed30313-s4.json")))
    assert side["params"]["engine"] == "flf2v" and side["lastframe"] == side["keyframe"]
    print("PASS: 2 rows, distilled + full, loop and explicit last frame, uploads", UPLOADS)
    shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
