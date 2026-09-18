import base64
import os
import tempfile

import boto3
import requests

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_REGION = os.environ.get("AWS_REGION", "us-east-1")
INPUT_DIR = "/tmp/wan-input"
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


def upload_to_s3(path: str, key: str | None = None, expires: int = 3600) -> str | None:
    if not S3_BUCKET:
        return None
    final_key = key or f"wan-video/{os.path.basename(path)}"
    _s3().upload_file(path, S3_BUCKET, final_key)
    return _s3().generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET, "Key": final_key},
        ExpiresIn=expires,
    )


def _s3():
    return boto3.client("s3", region_name=S3_REGION)


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
    os.makedirs("/tmp/wan-output", exist_ok=True)
    fd, name = tempfile.mkstemp(suffix=ext, dir="/tmp/wan-output")
    os.close(fd)
    return name