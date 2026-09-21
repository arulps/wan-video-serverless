import logging
import os
import sys
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
    log.info("BOOT: torch.cuda.current_device shimmed (returns 0 when unavailable)")
    _force_sdpa_attention()


def _force_sdpa_attention():
    """Force Wan's attention dispatch to the non-flash scaled-dot-product path.

    The built image strips flash_attn from requirements (the CUDA kernel can't be
    compiled on a CPU-only build host), so `FLASH_ATTN_2_AVAILABLE` /
    `FLASH_ATTN_3_AVAILABLE` are False at import.

    Wan2.2's `wan/modules/model.py` does `from .attention import flash_attention`
    at module scope, so by the time this shim runs that module already holds its
    OWN reference to the original function.  Rebinding the attribute on
    `wan.modules.attention` alone never reaches that reference -- which is why
    the previous version of this shim did not prevent
    `assert FLASH_ATTN_2_AVAILABLE` at /opt/wan/wan/modules/attention.py:112.

    Correct approach: import the whole `wan` package first (pulling in every
    submodule that could have from-imported the originals), capture the original
    function objects, then sweep every loaded `wan.*` module and replace any
    attribute that IS one of those originals.  Matching on identity means we
    only touch genuine re-exports and never clobber an unrelated attribute that
    happens to share a name.
    """
    try:
        import torch
        import torch.nn.functional as F
        import wan  # noqa: F401 - force full package import before the sweep
        import wan.modules.attention as wa
    except Exception as exc:
        log.warning("BOOT: attention fallback NOT installed: %s", exc)
        return

    wa.FLASH_ATTN_2_AVAILABLE = False
    wa.FLASH_ATTN_3_AVAILABLE = False

    # Capture the originals BEFORE replacing anything.
    originals = set()
    for attr in ("flash_attention", "attention"):
        fn = getattr(wa, attr, None)
        if callable(fn):
            originals.add(id(fn))

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

    patched = []
    for mod_name, mod in list(sys.modules.items()):
        if mod is None:
            continue
        if mod_name != "wan" and not mod_name.startswith("wan."):
            continue
        try:
            members = list(vars(mod).items())
        except Exception:
            continue
        for attr, value in members:
            if id(value) in originals:
                try:
                    setattr(mod, attr, _sdpa)
                    patched.append("%s.%s" % (mod_name, attr))
                except Exception:
                    pass

    # Belt and braces: guarantee the canonical names regardless of the sweep.
    wa.flash_attention = _sdpa
    wa.attention = _sdpa

    log.info(
        "BOOT: wan attention forced to scaled_dot_product_attention; "
        "patched %d binding(s): %s",
        len(patched), ", ".join(sorted(patched)) or "(none found by sweep)",
    )
    if not any(p.startswith("wan.modules.model.") for p in patched):
        log.warning(
            "BOOT: no flash_attention binding found on wan.modules.model - "
            "either this fork does not from-import it, or that module was not "
            "loaded. If the flash-attn assert reappears, inspect "
            "wan.modules.model.flash_attention at runtime."
        )


def report_failure(source):
    exc_info = sys.exc_info()
    if exc_info[0] is not None:
        tb_text = "".join(traceback.format_exception(*exc_info))
    else:
        tb_text = "(no traceback)"
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
            datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S"),
        )
        client.put_object(Bucket=bucket, Key=key, Body=tb_text)
        log.error("traceback uploaded to s3://%s/%s", bucket, key)
    except Exception as exc:
        log.error("could not upload traceback: %s", exc)
    return tb_text
