import logging
import os
import traceback

log = logging.getLogger("wan-boot")

_shimmed = False


def apply_cuda_shim():
    global _shimmed
    if _shimmed:
        return
    _shimmed = True
    try:
        import torch
    except Exception:
        return
    current_device = getattr(torch.cuda, "current_device", None)
    if current_device is None:
        return

    def safe_current_device(*args, **kwargs):
        try:
            return current_device(*args, **kwargs)
        except Exception:
            return 0

    torch.cuda.current_device = safe_current_device
    log.debug("torch.cuda.current_device shimmed (returns 0 when unavailable)")


def report_failure(source):
    tb_text = "".join(traceback.format_exception(
        *(__import__("sys").exc_info()))) if __import__("sys").exc_info()[0] else "(no traceback)"
    log.error("[%s] FAILURE\n%s", source, tb_text)
    try:
        import datetime
        import boto3
        bucket = os.environ.get("S3_BUCKET")
        if not bucket:
            return tb_text
        client = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-east-1"))
        key = "wan/errors/%s-%s.txt" % (
            source,
            datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S"),
        )
        client.put_object(Bucket=bucket, Key=key, Body=tb_text)
        log.error("traceback uploaded to s3://%s/%s", bucket, key)
    except Exception as exc:
        log.error("could not upload traceback: %s", exc)
    return tb_text