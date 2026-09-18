import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

API_BASE = os.environ.get("RUNPOD_API_BASE", "https://api.runpod.ai/v2")
POLL_INTERVAL = float(os.environ.get("POLL_INTERVAL", "3"))


def load_env(path=None):
    path = path or os.environ.get("WAN_ENV_PATH") or os.path.join(os.getcwd(), ".env")
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def _request(url, method="GET", payload=None, api_key=None):
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def main():
    load_env()
    ap = argparse.ArgumentParser(description="Generate a video via the Wan serverless endpoint")
    ap.add_argument("--endpoint", default=os.environ.get("WAN_ENDPOINT_ID"),
                    help="serverless endpoint id (defaults to WAN_ENDPOINT_ID from .env)")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--task", default=None, choices=["ti2v-5B", "t2v-A14B", "i2v-A14B"])
    ap.add_argument("--image", default=None, help="http(s) URL, s3:// URI, or base64")
    ap.add_argument("--size", default=None, help="e.g. 1280*704, 1280*720, 832*480")
    ap.add_argument("--frame-num", type=int, default=81)
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--seed", type=int, default=-1)
    ap.add_argument("--output-key", default=None, help="S3 key to write video to")
    ap.add_argument("--out", default="video.mp4", help="local file to save the video")
    ap.add_argument("--sync", action="store_true", help="use /runsync instead of /run + poll")
    args = ap.parse_args()

    api_key = os.environ.get("RUNPOD_API_KEY")
    if not api_key:
        sys.exit("RUNPOD_API_KEY env var is required")

    input_payload = {
        "prompt": args.prompt,
        "frame_num": args.frame_num,
        "seed": args.seed,
        "offload": True,
    }
    for key, val in (("task", args.task), ("image", args.image), ("size", args.size),
                     ("steps", args.steps), ("output_key", args.output_key)):
        if val is not None:
            input_payload[key] = val

    endpoint = args.endpoint
    if not endpoint:
        sys.exit("no endpoint id: pass --endpoint or set WAN_ENDPOINT_ID in .env")
    endpoint = endpoint.lstrip("/")

    if args.sync:
        print("submitting sync job...")
        resp = _request(f"{API_BASE}/{endpoint}/runsync", "POST",
                        {"input": input_payload}, api_key)
        output = resp.get("output")
        if resp.get("status") != "COMPLETED" or output is None:
            sys.exit(f"job failed: {resp}")
    else:
        resp = _request(f"{API_BASE}/{endpoint}/run", "POST",
                        {"input": input_payload}, api_key)
        job_id = resp.get("id")
        if not job_id:
            sys.exit(f"submit failed: {resp}")
        print(f"job {job_id} submitted")
        while True:
            status = _request(f"{API_BASE}/{endpoint}/status/{job_id}", api_key=api_key)
            state = status.get("status")
            print(f"  status: {state}")
            if state == "COMPLETED":
                output = status.get("output")
                break
            if state in ("FAILED", "CANCELLED"):
                sys.exit(f"job {state}: {status}")
            time.sleep(POLL_INTERVAL)

    if not output:
        sys.exit("empty output")
    if output.get("video"):
        url = output["video"]
        print(f"downloading result...")
        with urllib.request.urlopen(url, timeout=300) as r, open(args.out, "wb") as f:
            f.write(r.read())
    elif output.get("video_b64"):
        with open(args.out, "wb") as f:
            f.write(base64.b64decode(output["video_b64"]))
    else:
        sys.exit(f"unexpected output shape: {list(output.keys())}")

    print(f"saved {args.out} ({os.path.getsize(args.out)} bytes)")


if __name__ == "__main__":
    main()