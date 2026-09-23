#!/usr/bin/env python3
"""Drive a ComfyUI server headlessly: upload the reference image, patch the
API-format workflow (comfy/vace_ref2v_api.json), queue it, wait, download the
mp4, print timing. No UI clicks needed.

    python comfy/run_comfy.py --host http://127.0.0.1:8188 \
        --ref outputs/vace/refs/minnu-4view-16x9.png \
        --prompt-file prompts/mazhai/V2c-minnu-impatience-v3.txt \
        --negative-file prompts/mazhai/NEGATIVE.txt \
        --label v2c-a1 --steps 4 --cfg 1.0 --shift 5.0 --sampler lcm \
        --out outputs/vace/pod

Control run (no LoRA):  --no-lora --steps 30 --cfg 5.0 --sampler uni_pc --scheduler simple
Schema check:           --schema SaveVideo   (prints /object_info for a node and exits)

Only the standard library is used so it runs on the pod or the laptop as is.

`build_workflow()` and `submit_and_wait()` below are reusable pieces factored
out for comfy/batch_runner.py; this file's own CLI behaviour is unchanged.
"""
import argparse
import copy
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))

# RunPod's proxy 403s the stdlib's default urllib User-Agent -- always send a
# browser-like one. Found in production (phase4d).
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) WanComfyDriver/1.0"

DEFAULT_LORA = "Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank64.safetensors"


def http(method, url, data=None, headers=None, timeout=600):
    h = {"User-Agent": USER_AGENT}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def interrupt(host):
    """POST /interrupt -- best-effort, never raises."""
    try:
        http("POST", host + "/interrupt", b"")
    except Exception:
        pass


def upload_image(host, path):
    """POST /upload/image (multipart). Returns the server-side filename."""
    boundary = "----wan" + uuid.uuid4().hex
    name = os.path.basename(path)
    ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    body = b""
    body += ("--%s\r\nContent-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\n"
             "Content-Type: %s\r\n\r\n" % (boundary, name, ctype)).encode()
    body += open(path, "rb").read() + b"\r\n"
    body += ("--%s\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n" % boundary).encode()
    body += ("--%s--\r\n" % boundary).encode()
    out = http("POST", host + "/upload/image", body, {"Content-Type": "multipart/form-data; boundary=" + boundary})
    j = json.loads(out)
    return (j.get("subfolder") + "/" if j.get("subfolder") else "") + j["name"]


# Node 9 is the conditioning node; which input carries the reference image(s)
# depends on its class. Multi-reference needs a node that encodes every image of
# the batch on its own: core WanVaceToVideo uses only reference_image[:1]
# (verified in comfy_extras/nodes_wan.py), so >1 refs switch it to our
# comfy/custom_nodes/wan_vace_multiref.py node; WanPhantomSubjectToVideo
# already loops over the batch.
REF_INPUT_KEY = {"WanVaceToVideo": "reference_image", "WanVaceToVideoMultiRef": "reference_image",
                 "WanPhantomSubjectToVideo": "images"}
MULTIREF_CLASS = {"WanVaceToVideo": "WanVaceToVideoMultiRef"}
# LoadImage / ImageBatch node ids used for the 2nd.. references (15/16 are the keyframe nodes)
EXTRA_REF_NODE_BASE = 20


def build_workflow(wf, prompt, negative, ref_name, width, height, length, seed, steps, cfg,
                    sampler, scheduler, shift, lora, lora_strength, no_lora, prefix):
    """Patch a loaded vace_ref2v_api.json / phantom_s2v_api.json workflow dict
    with the shot's parameters. Returns a fresh deep copy -- the input `wf` is
    never mutated, so the same base dict can be reused across shots.
    `ref_name` is None (no reference), one uploaded filename (one sheet), or a
    list of uploaded filenames (SEPARATE references, one per character tile:
    they are batched with ImageBatch and node 9 is switched to a class that
    encodes each image on its own)."""
    wf = copy.deepcopy(wf)
    wf["6"]["inputs"]["text"] = prompt
    wf["7"]["inputs"]["text"] = negative
    cond_class = wf["9"]["class_type"]
    ref_key = REF_INPUT_KEY.get(cond_class)
    if ref_key is None:
        raise RuntimeError("node 9 is %r; expected one of %s" % (cond_class, ", ".join(REF_INPUT_KEY)))
    refs = [ref_name] if isinstance(ref_name, str) else list(ref_name or [])
    if not refs:
        # No reference (e.g. an empty-room establishing shot): the reference
        # input is optional upstream, so drop the LoadImage node and the link;
        # the shot becomes plain text-to-video.
        wf.pop("8", None)
        wf["9"]["inputs"].pop(ref_key, None)
    else:
        wf["8"]["inputs"]["image"] = refs[0]
        last = ["8", 0]
        for i, name in enumerate(refs[1:]):
            load_id = str(EXTRA_REF_NODE_BASE + 2 * i)
            batch_id = str(EXTRA_REF_NODE_BASE + 2 * i + 1)
            wf[load_id] = {"class_type": "LoadImage", "inputs": {"image": name}}
            wf[batch_id] = {"class_type": "ImageBatch", "inputs": {"image1": last, "image2": [load_id, 0]}}
            last = [batch_id, 0]
        wf["9"]["inputs"][ref_key] = last
        if len(refs) > 1 and cond_class in MULTIREF_CLASS:
            wf["9"]["class_type"] = MULTIREF_CLASS[cond_class]
    wf["9"]["inputs"].update({"width": width, "height": height, "length": length})
    wf["10"]["inputs"].update({"seed": seed, "steps": steps, "cfg": cfg,
                               "sampler_name": sampler, "scheduler": scheduler})
    wf["5"]["inputs"]["shift"] = shift
    if no_lora:
        wf["5"]["inputs"]["model"] = ["1", 0]      # ModelSamplingSD3 takes the raw UNET
        if "4" in wf:
            del wf["4"]
    else:
        wf["4"]["inputs"].update({"lora_name": lora, "strength_model": lora_strength})
    wf["14"]["inputs"]["filename_prefix"] = "video/" + prefix
    return wf


def add_first_frame_keyframe(wf, keyframe_name, width, height):
    """Pin frame 0 of the clip to an uploaded image (VACE first-frame-to-video).
    Verified against ComfyUI's WanVaceToVideo (comfy_extras/nodes_wan.py):
    a control_video shorter than `length` is padded with 0.5 (neutral) and a
    control_masks batch shorter than `length` is padded with 1.0 (= generate),
    so ONE keyframe image + ONE all-zero mask frame pins exactly frame 0 and
    leaves every other frame free. The reference sheet stays on
    `reference_image` for identity. Node ids 15/16 are free in
    vace_ref2v_api.json."""
    wf["15"] = {"class_type": "LoadImage", "inputs": {"image": keyframe_name}}
    wf["16"] = {"class_type": "SolidMask", "inputs": {"value": 0.0, "width": width, "height": height}}
    wf["9"]["inputs"]["control_video"] = ["15", 0]
    wf["9"]["inputs"]["control_masks"] = ["16", 0]
    return wf


def submit_and_wait(host, wf, prefix, out_dir, timeout_min):
    """Queue `wf` on `host`, poll until it finishes, download the video to
    `out_dir/<prefix>.mp4`. Returns {"dest", "wall_s", "bytes", "server_file",
    "prompt_id"}. Raises RuntimeError on a rejected prompt or execution error
    (message prefixed "PROMPT REJECTED" or "EXECUTION ERROR" respectively),
    or TimeoutError after `timeout_min` minutes."""
    client = uuid.uuid4().hex
    try:
        r = http("POST", host + "/prompt", json.dumps({"prompt": wf, "client_id": client}).encode(),
                 {"Content-Type": "application/json"})
    except urllib.error.HTTPError as e:
        raise RuntimeError("PROMPT REJECTED (fix the named node input and rerun):\n" + e.read().decode()[:3000])
    pid = json.loads(r)["prompt_id"]
    print("queued", pid, "prefix", prefix, flush=True)

    t0 = time.time(); deadline = t0 + timeout_min * 60; last = ""
    while time.time() < deadline:
        h = json.loads(http("GET", host + "/history/" + pid))
        if pid in h:
            item = h[pid]
            st = item.get("status", {})
            if st.get("status_str") == "error":
                raise RuntimeError("EXECUTION ERROR:\n" + json.dumps(st.get("messages"), indent=1)[:3000])
            outs = item.get("outputs", {})
            vids = []
            for node_out in outs.values():
                for key in ("videos", "gifs", "images"):
                    for f in node_out.get(key, []) or []:
                        if f.get("filename", "").lower().endswith((".mp4", ".webm", ".mkv")):
                            vids.append(f)
            if vids:
                wall = time.time() - t0
                f = vids[0]
                q = urllib.parse.urlencode({"filename": f["filename"], "subfolder": f.get("subfolder", ""), "type": f.get("type", "output")})
                data = http("GET", host + "/view?" + q)
                os.makedirs(out_dir, exist_ok=True)
                dest = os.path.join(out_dir, prefix + ".mp4")
                open(dest, "wb").write(data)
                return {"dest": dest, "wall_s": round(wall, 1), "bytes": len(data),
                        "server_file": f, "prompt_id": pid}
        try:
            qd = json.loads(http("GET", host + "/queue"))
            line = "running=%d pending=%d %.0fs" % (len(qd.get("queue_running", [])), len(qd.get("queue_pending", [])), time.time() - t0)
        except Exception:
            line = "%.0fs" % (time.time() - t0)
        if line != last:
            print(line, flush=True); last = line
        time.sleep(10)
    raise TimeoutError("TIMED OUT after %d min" % timeout_min)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="http://127.0.0.1:8188")
    ap.add_argument("--workflow", default=os.path.join(HERE, "vace_ref2v_api.json"))
    ap.add_argument("--ref", action="append", help="reference image (16:9 sheet); uploaded to ComfyUI/input. "
                    "Repeat for SEPARATE references (one tile per character; needs the multi-ref custom node)")
    ap.add_argument("--prompt-file"); ap.add_argument("--prompt", default="")
    ap.add_argument("--negative-file"); ap.add_argument("--negative", default="")
    ap.add_argument("--label", default="vace")
    ap.add_argument("--steps", type=int, default=4)
    ap.add_argument("--cfg", type=float, default=1.0)
    ap.add_argument("--shift", type=float, default=5.0)
    ap.add_argument("--sampler", default="lcm")
    ap.add_argument("--scheduler", default="simple")
    ap.add_argument("--seed", type=int, default=30313)
    ap.add_argument("--width", type=int, default=1280); ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--length", type=int, default=81)
    ap.add_argument("--lora", default=DEFAULT_LORA)
    ap.add_argument("--lora-strength", type=float, default=1.0)
    ap.add_argument("--no-lora", action="store_true", help="bypass the LoRA node (control run)")
    ap.add_argument("--out", default="outputs/vace/pod")
    ap.add_argument("--timeout-min", type=int, default=60)
    ap.add_argument("--schema", help="print /object_info/<Node> and exit")
    a = ap.parse_args()

    if a.schema:
        print(http("GET", a.host + "/object_info/" + a.schema).decode()[:4000]); return

    wf = json.load(open(a.workflow, encoding="utf-8"))
    pos = open(a.prompt_file, encoding="utf-8").read().strip() if a.prompt_file else a.prompt
    neg = open(a.negative_file, encoding="utf-8").read().strip() if a.negative_file else a.negative
    if not pos: sys.exit("prompt required (--prompt or --prompt-file)")
    if not a.ref: sys.exit("--ref required")
    if (a.length - 1) % 4: sys.exit("length must be 4n+1")

    ref_names = [upload_image(a.host, r) for r in a.ref]
    print("uploaded ref(s) ->", ", ".join(ref_names), flush=True)
    ref_name = ref_names if len(ref_names) > 1 else ref_names[0]

    stamp = time.strftime("%Y%m%d-%H%M")
    prefix = "%s-%s-s%d-cfg%g-%dx%d" % (stamp, a.label, a.steps, a.cfg, a.width, a.height)

    wf = build_workflow(wf, prompt=pos, negative=neg, ref_name=ref_name, width=a.width, height=a.height,
                         length=a.length, seed=a.seed, steps=a.steps, cfg=a.cfg, sampler=a.sampler,
                         scheduler=a.scheduler, shift=a.shift, lora=a.lora, lora_strength=a.lora_strength,
                         no_lora=a.no_lora, prefix=prefix)

    try:
        result = submit_and_wait(a.host, wf, prefix, a.out, a.timeout_min)
    except RuntimeError as e:
        msg = str(e)
        print(msg)
        sys.exit(2 if msg.startswith("PROMPT REJECTED") else 3)
    except TimeoutError as e:
        print(str(e) + "; /interrupt the server if needed"); sys.exit(4)

    meta = {"prompt_id": result["prompt_id"], "wall_s": result["wall_s"], "steps": a.steps, "cfg": a.cfg,
            "shift": a.shift, "sampler": a.sampler, "scheduler": a.scheduler, "seed": a.seed,
            "size": [a.width, a.height], "length": a.length, "lora": None if a.no_lora else a.lora,
            "lora_strength": a.lora_strength, "ref": a.ref, "bytes": result["bytes"],
            "server_file": result["server_file"]}
    json.dump(meta, open(result["dest"][:-4] + ".json", "w"), indent=1)
    print("SAVED", result["dest"], "(%d B) wall %.1fs" % (result["bytes"], result["wall_s"]), flush=True)


if __name__ == "__main__":
    main()
