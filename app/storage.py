import base64
import os
import subprocess
import tempfile

import boto3
import requests

# Object storage for outputs. Any S3-compatible service works:
#   AWS S3:        S3_BUCKET + AWS_REGION + AWS_ACCESS_KEY_ID/SECRET
#   Cloudflare R2: S3_BUCKET + S3_ENDPOINT_URL=https://<acct>.r2.cloudflarestorage.com
#                  + AWS_ACCESS_KEY_ID/SECRET (R2 API token), AWS_REGION=auto
# Optional S3_PUBLIC_BASE_URL (e.g. an R2 public bucket domain): when set the
# handler returns a plain public URL instead of a presigned one.
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_REGION = os.environ.get("AWS_REGION", "us-east-1")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL") or None
S3_PUBLIC_BASE_URL = (os.environ.get("S3_PUBLIC_BASE_URL") or "").rstrip("/")
S3_PRESIGN_SECONDS = int(os.environ.get("S3_PRESIGN_SECONDS", "86400"))

INPUT_DIR = "/tmp/wan-input"
OUTPUT_DIR = "/tmp/wan-output"
FILE_PART = 1 << 16


def fetch_input(ref: str) -> str:
    os.makedirs(INPUT_DIR, exist_ok=True)
    if ref.startswith("s3://"):
        return _s3_download(ref)
    dest = os.path.join(INPUT_DIR, os.path.basename(ref.split("?")[0]) or "input.bin")
    with requests.get(ref, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=FILE_PART):
                f.write(chunk)
    return dest


def _s3_download(uri: str) -> str:
    bucket, _, key = uri[5:].partition("/")
    dest = os.path.join(INPUT_DIR, os.path.basename(key))
    _s3().download_file(bucket, key, dest)
    return dest


def upload_to_s3(path: str, key: str | None = None, expires: int | None = None) -> str | None:
    if not S3_BUCKET:
        return None
    final_key = key or f"wan-video/{os.path.basename(path)}"
    _s3().upload_file(path, S3_BUCKET, final_key, ExtraArgs={"ContentType": "video/mp4"})
    if S3_PUBLIC_BASE_URL:
        return f"{S3_PUBLIC_BASE_URL}/{final_key}"
    return _s3().generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET, "Key": final_key},
        ExpiresIn=expires or S3_PRESIGN_SECONDS,
    )


def _s3():
    return boto3.client("s3", region_name=S3_REGION, endpoint_url=S3_ENDPOINT_URL)


def write_b64(payload: str) -> str:
    os.makedirs(INPUT_DIR, exist_ok=True)
    dest = os.path.join(INPUT_DIR, "input.png")
    with open(dest, "wb") as f:
        f.write(base64.b64decode(payload))
    return dest


def to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def temp_output_file(ext: str = ".mp4") -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fd, name = tempfile.mkstemp(suffix=ext, dir=OUTPUT_DIR)
    os.close(fd)
    return name


# Review-copy encode quality when no object storage is configured. crf 23 smeared
# fine moving detail (fingers) in the 2026-09-21 ladders at ~470 kbps; 18 is ~3x the
# bitrate and still far under RunPod's 10 MB output cap for a 3-4 s clip.
COMPACT_CRF = int(os.environ.get("COMPACT_CRF", "18"))


def compact_mp4(src: str, crf: int | None = None, preset: str = "medium") -> str:
    """Re-encode Wan's quality=8 libx264 output to a web-sized H.264 (yuv420p,
    faststart). Wan's writer is tuned for fidelity, not size; a 4 s 1280x704 clip
    can be well over RunPod's 10 MB job-output ceiling. Returns the new path.
    Raises on ffmpeg failure so the caller never returns a bogus file."""
    if crf is None:
        crf = COMPACT_CRF
    dst = temp_output_file(".mp4")
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-i", src,
        "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", dst,
    ]
    subprocess.run(cmd, check=True, capture_output=True, timeout=600)
    if not os.path.isfile(dst) or os.path.getsize(dst) == 0:
        raise RuntimeError("ffmpeg produced no output")
    return dst
