import logging
import os
import sys
import traceback

log = logging.getLogger("wan-boot")

_shimmed = False

# Populated by _force_sdpa_attention(); read by the handler's selftest op so a
# cheap job can prove the patch reached wan.modules.model before any weights
# are loaded.
SHIM_REPORT = {
    "sdpa_installed": False,
    "patched": [],
    "model_binding_patched": False,
    "error": None,
}


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
    _log_hf_hub()


def _log_hf_hub():
    """Answer the open dispatch question (huggingface_hub version) from the boot log."""
    try:
        import inspect

        import huggingface_hub as hfh

        has_kwarg = "local_dir_use_symlinks" in inspect.signature(hfh.snapshot_download).parameters
        log.info(
            "BOOT: huggingface_hub %s; snapshot_download has local_dir_use_symlinks=%s",
            getattr(hfh, "__version__", "?"), has_kwarg,
        )
    except Exception as exc:
        log.warning("BOOT: could not inspect huggingface_hub: %s", exc)


def make_sdpa_flash_attention(torch, F):
    """Build a drop-in replacement for wan.modules.attention.flash_attention that
    runs on torch's scaled_dot_product_attention.

    Contract of the original (see Wan2.2 wan/modules/attention.py):
      q: [B, Lq, Nq, C1]  k: [B, Lk, Nk, C1]  v: [B, Lk, Nk, C2]   (heads AFTER sequence)
      returns [B, Lq, Nq, C2] in q's original dtype.

    torch SDPA wants [B, N, L, C] (heads BEFORE sequence), so the tensors must be
    transposed in and back out -- exactly what upstream's own non-flash
    `attention()` fallback does. Passing Wan's layout straight through does not
    crash: SDPA silently attends across the 24 heads *within* each token instead
    of across tokens, and the job completes with a noise video.

    Semantics reproduced from the flash path:
      * q_scale multiplies q before attention.
      * softmax_scale None -> 1/sqrt(C1) (flash default == SDPA default).
      * k_lens (true key lengths per batch row) -> boolean key-padding mask.
        Wan calls self-attention with k_lens=seq_lens (== Lk at batch 1) and
        cross-attention with k_lens=None, so at batch 1 this is a no-op; it is
        implemented anyway so batch>1 stays correct rather than silently wrong.
      * q_lens: flash treats rows past q_lens as absent. Their outputs are
        never read by Wan (it unpads by seq_lens), so they are left as-is.
      * window_size / deterministic: Wan uses (-1, -1) and False; not supported
        here and ignored (a non-default window_size raises so it cannot go
        unnoticed).
      * Both the original's `version=` and attention()'s `fa_version=` kwargs
        are accepted so either call path works.
    """

    def sdpa_flash_attention(q, k, v, q_lens=None, k_lens=None, dropout_p=0.0,
                             softmax_scale=None, q_scale=None, causal=False,
                             window_size=(-1, -1), deterministic=False,
                             dtype=torch.bfloat16, version=None, fa_version=None):
        if tuple(window_size) != (-1, -1):
            raise NotImplementedError(
                "sliding-window attention is not available on the SDPA fallback")

        out_dtype = q.dtype
        b, lq, lk = q.size(0), q.size(1), k.size(1)

        half_dtypes = (torch.float16, torch.bfloat16)
        if q.dtype not in half_dtypes:
            q = q.to(dtype)
        if k.dtype not in half_dtypes:
            k = k.to(dtype)
        if v.dtype not in half_dtypes:
            v = v.to(dtype)
        q = q.to(v.dtype)
        k = k.to(v.dtype)

        if q_scale is not None:
            q = q * q_scale

        attn_mask = None
        if k_lens is not None:
            k_lens_t = torch.as_tensor(k_lens, device=k.device)
            if bool((k_lens_t < lk).any()):
                # True = attend. Shape [B, 1, 1, Lk] broadcasts over heads and queries.
                attn_mask = (torch.arange(lk, device=k.device)[None, :]
                             < k_lens_t[:, None])[:, None, None, :]

        # [B, L, N, C] -> [B, N, L, C]
        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)

        out = F.scaled_dot_product_attention(
            q, k, v,
            attn_mask=attn_mask,
            dropout_p=dropout_p,
            is_causal=causal,
            scale=softmax_scale,
        )

        # [B, N, L, C] -> [B, L, N, C]
        return out.transpose(1, 2).contiguous().type(out_dtype)

    return sdpa_flash_attention


def _force_sdpa_attention():
    """Force Wan's attention dispatch to the non-flash scaled-dot-product path.

    The built image strips flash_attn from requirements (the CUDA kernel can't be
    compiled on a CPU-only build host), so `FLASH_ATTN_2_AVAILABLE` /
    `FLASH_ATTN_3_AVAILABLE` are False at import and `flash_attention()` asserts.

    Wan2.2's `wan/modules/model.py` does `from .attention import flash_attention`
    at module scope (so does `wan/modules/__init__.py`), so by the time this shim
    runs those modules already hold their OWN references to the original
    function. Rebinding the attribute on `wan.modules.attention` alone never
    reaches them.

    Approach: import the whole `wan` package first (pulling in every submodule
    that could have from-imported the originals), capture the original function
    objects, then sweep every loaded `wan.*` module and replace any attribute
    that IS one of those originals. Matching on identity means only genuine
    re-exports are touched.
    """
    try:
        import torch
        import torch.nn.functional as F
        import wan  # noqa: F401 - force full package import before the sweep
        import wan.modules.attention as wa
    except Exception as exc:
        SHIM_REPORT["error"] = repr(exc)
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

    _sdpa = make_sdpa_flash_attention(torch, F)

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

    model_ok = any(p.startswith("wan.modules.model.") for p in patched)
    SHIM_REPORT.update({
        "sdpa_installed": True,
        "patched": sorted(patched),
        "model_binding_patched": model_ok,
    })

    log.info(
        "BOOT: wan attention forced to scaled_dot_product_attention; "
        "patched %d binding(s): %s",
        len(patched), ", ".join(sorted(patched)) or "(none found by sweep)",
    )
    if not model_ok:
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

        bucket = os.environ.get("S3_BUCKET")
        if not bucket:
            return tb_text
        from . import storage  # lazy: keeps boot importable before deps load
        key = "wan/errors/%s-%s.txt" % (
            source,
            datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S"),
        )
        storage._s3().put_object(Bucket=bucket, Key=key, Body=tb_text)
        log.error("traceback uploaded to s3://%s/%s", bucket, key)
    except Exception as exc:
        log.error("could not upload traceback: %s", exc)
    return tb_text
