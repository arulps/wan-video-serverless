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
    _force_sdpa_attention()


def _force_sdpa_attention():
    """Force Wan's attention dispatch to the non-flash scaled-dot-product path.

    The built image strips flash_attn from requirements (the CUDA kernel can't be
    compiled on a CPU-only build host), so `FLASH_ATTN_2_AVAILABLE` /
    `FLASH_ATTN_3_AVAILABLE` are False at import.  Some Wan2.2 forks still route
    self-attention straight into `flash_attention()`, which then hits
    `assert FLASH_ATTN_2_AVAILABLE` at /opt/wan/wan/modules/attention.py:112.

    We patch the availability flags before any attention dispatch is evaluated so
    the dispatcher (which re-reads the flag at call time) always takes the SDPA
    fallback, and we replace `flash_attention()` itself with an SDPA
    implementation so even a fork that calls it directly degrades gracefully.
    """
    try:
        import torch
        import torch.nn.functional as F
        import wan.modules.attention as wa
    except Exception as exc:
        log.debug("attention fallback not installed: %s", exc)
        return

    wa.FLASH_ATTN_2_AVAILABLE = False
    wa.FLASH_ATTN_3_AVAILABLE = False

    def _sdpa(q, k, v, q_lens=None, k_lens=None, dropout_p=0.0,
              softmax_scale=None, q_scale=None, causal=False,
              window_size=(-1, -1), deterministic=False,
              dtype=torch.bfloat16, fa_version=None):
        scale = softmax_scale
        if scale is None and q_scale is not None:
            scale = q_scale * (q.size(-1) ** -0.5)
        if scale is None:
            scale = q.size(-1) ** -0.5
        out = F.scaled_dot_product_attention(
            q, k, v, attn_mask=None,
            dropout_p=dropout_p, is_causal=causal, scale=scale)
        return out

    wa.flash_attention = _sdpa
    wa.attention = _sdpa
    log.debug("wan attention forced to scaled_dot_product_attention (flash-attn unavailable)")


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