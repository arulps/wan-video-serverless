"""Handler behaviour with the generator stubbed: selftest op, key aliases,
inline delivery via real ffmpeg compaction, the size ceiling, the S3 branch,
seed reporting and temp-file cleanup. No GPU, no network."""
import base64
import importlib
import os
import subprocess
import sys
import tempfile
import types

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

# ---- stubs -----------------------------------------------------------------
runpod = types.ModuleType("runpod")
runpod.serverless = types.SimpleNamespace(
    start=lambda cfg: None,
    progress_update=lambda job, msg: progress_log.append(msg),
)
progress_log = []
sys.modules["runpod"] = runpod

# fake wan + a fake app.generator so importing the handler never touches the real model
wan = types.ModuleType("wan")
wan.modules = types.SimpleNamespace(attention=types.SimpleNamespace(flash_attention=None, attention=None))
sys.modules["wan"] = wan

gen = types.ModuleType("app.generator")
gen._PIPE_CLASSES = {"ti2v-5B": object, "t2v-A14B": object, "i2v-A14B": object}
gen.supported_sizes = lambda task: ("704*1280", "1280*704") if task == "ti2v-5B" else ()
CALLS = []


def _make_mp4(path, seconds=1, size="320x176"):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    f"testsrc=size={size}:rate=24", "-t", str(seconds), "-c:v", "libx264",
                    "-crf", "1", "-pix_fmt", "yuv444p", path], check=True)


def fake_generate(**kw):
    CALLS.append(kw)
    if kw.get("progress"):
        kw["progress"]("sampling")
    from app.storage import temp_output_file
    out = temp_output_file(".mp4")
    _make_mp4(out, seconds=fake_generate.seconds)
    info = {"task": kw["task"], "size": kw["size"], "frame_num": kw["frame_num"], "fps": 24,
            "steps": kw["steps"] if kw["steps"] is not None else 50, "seed": kw["seed"],
            "raw_bytes": os.path.getsize(out)}
    return out, info


fake_generate.seconds = 1
gen.generate = fake_generate
sys.modules["app.generator"] = gen

os.environ["S3_BUCKET"] = ""
os.environ["MAX_OUTPUT_MB"] = "9"

import app.boot as boot  # noqa: E402

boot.SHIM_REPORT.update({"sdpa_installed": True, "model_binding_patched": True,
                         "patched": ["wan.modules.model.flash_attention"]})
import handler as H  # noqa: E402

# ---- 1. selftest op --------------------------------------------------------
r = H.handler({"id": "t1", "input": {"op": "selftest"}})
assert r["op"] == "selftest"
assert r["shim"]["model_binding_patched"] is True
assert r["ffmpeg"], "ffmpeg must be found"
assert "weights" in r and r["weights"]["repo"] == "Wan-AI/Wan2.2-TI2V-5B"
# on this CPU box CUDA is absent -> selftest must report error, not pretend ok
assert r["ok"] is False and r["status"] == "error" and "CUDA" in r["error"]
print("selftest:", {k: r[k] for k in ("huggingface_hub", "torch", "cuda_available", "ffmpeg", "ok")})

# ---- 2. shim-not-patched guard ---------------------------------------------
boot.SHIM_REPORT["model_binding_patched"] = False
r = H.handler({"id": "t2", "input": {"prompt": "x"}})
assert r["status"] == "error" and "SDPA patch did not reach" in r["error"]
boot.SHIM_REPORT["model_binding_patched"] = True

# ---- 3. aliases + inline delivery + seed -----------------------------------
CALLS.clear()
r = H.handler({"id": "t3", "input": {
    "prompt": "a duck", "task": "ti2v-5B",
    "num_frames": 81, "sample_steps": 20, "cfg_scale": 4.5, "sample_shift": 5.0,
    "negative_prompt": "blurry", "resolution": "1280*704", "seed": -1}})
assert r["status"] == "complete", r
kw = CALLS[-1]
assert kw["frame_num"] == 81 and kw["steps"] == 20 and kw["guide_scale"] == 4.5
assert kw["shift"] == 5.0 and kw["n_prompt"] == "blurry" and kw["size"] == "1280*704"
assert kw["seed"] >= 0 and r["seed"] == kw["seed"], "seed must be drawn and reported"
assert r["delivery"] == "inline" and r["encoded"].startswith("libx264 crf18")
vid = base64.b64decode(r["video_b64"])
assert vid[4:8] == b"ftyp", "must be an mp4"
assert r["video_bytes"] == len(vid)
assert "sampling" in progress_log and "compacting" in progress_log
# temp files cleaned
assert not os.listdir("/tmp/wan-output"), os.listdir("/tmp/wan-output")
print("inline ok: raw", r["raw_bytes"], "-> compact", r["video_bytes"], "bytes")

# ---- 4. size ceiling -> explicit error, never a silent None ----------------
os.environ["MAX_OUTPUT_MB"] = "0.001"
importlib.reload(H)
r = H.handler({"id": "t4", "input": {"prompt": "a duck"}})
assert r["status"] == "error" and "over the 0.001 MB inline limit" in r["error"], r["error"][-200:]
assert "video_b64" not in r and "video" not in r
os.environ["MAX_OUTPUT_MB"] = "9"
importlib.reload(H)

# ---- 5. S3 branch ----------------------------------------------------------
import app.storage as storage  # noqa: E402

storage.S3_BUCKET = "bkt"
storage.upload_to_s3 = lambda path, key=None, expires=None: f"https://x/{key or 'auto'}"
r = H.handler({"id": "t5", "input": {"prompt": "a duck", "output_key": "wan/d1.mp4"}})
assert r["status"] == "complete" and r["video"] == "https://x/wan/d1.mp4" and r["delivery"] == "s3"
assert "video_b64" not in r
storage.S3_BUCKET = None
r = H.handler({"id": "t5b", "input": {"prompt": "a duck", "output_key": "wan/d1.mp4"}})
assert r["status"] == "complete" and r["delivery"] == "inline" and "warning" in r

# ---- 6. bad size for task -> error from validation path (stub passes through) -
r = H.handler({"id": "t6", "input": {"prompt": "a duck", "task": "nope"}})
assert r["status"] == "error" and "unsupported task" in r["error"]

print("HANDLER CHECKS PASSED")
