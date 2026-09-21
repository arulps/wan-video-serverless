import logging
import os
import random
import shutil
import time

import app.boot as boot

boot.apply_cuda_shim()

import runpod  # noqa: E402

from app import generator, models, storage  # noqa: E402

log = logging.getLogger("wan-worker")
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())

DEFAULT_TASK = os.environ.get("DEFAULT_TASK", "ti2v-5B")

# RunPod caps a job's returned output at 10 MB for /run (20 MB for /runsync).
# This is the cap on the base64 STRING we put in the result, not the file.
MAX_OUTPUT_MB = float(os.environ.get("MAX_OUTPUT_MB", "9"))

# Accept the key spellings that have appeared in this project's runbooks and
# clients, so a mismatch can never again silently fall back to a default.
_ALIASES = {
    "frame_num": ("frame_num", "num_frames", "base_num_frames", "frames"),
    "steps": ("steps", "sample_steps", "num_inference_steps"),
    "guide_scale": ("guide_scale", "cfg_scale", "guidance_scale", "cfg"),
    "shift": ("shift", "sample_shift"),
    "n_prompt": ("n_prompt", "negative_prompt"),
    "solver": ("solver", "sample_solver"),
    "seed": ("seed",),
    "size": ("size", "resolution"),
    "task": ("task",),
    "image": ("image", "image_url", "start_frame"),
    "prompt": ("prompt",),
    "offload": ("offload", "offload_model"),
    "output_key": ("output_key",),
}


def _pick(inp, canonical, default=None):
    for name in _ALIASES[canonical]:
        if name in inp and inp[name] is not None:
            return inp[name]
    return default


def _resolve_image(image):
    if not image:
        return None
    if not isinstance(image, str):
        raise ValueError("image must be a string (http/https URL, s3:// URI, data URI, or base64)")
    if image.startswith("data:"):
        return storage.write_b64(image.split(",", 1)[1])
    if image.startswith("http://") or image.startswith("https://") or image.startswith("s3://"):
        return storage.fetch_input(image)
    try:
        return storage.write_b64(image)
    except Exception:
        return image


def _rm(path):
    if path:
        try:
            os.remove(path)
        except OSError:
            pass


def selftest(task):
    """Prove the worker is usable WITHOUT loading weights: SDPA patch reached
    wan.modules.model, GPU present, weights location, ffmpeg, output config.
    Costs a worker boot only."""
    import torch

    rep = {"op": "selftest", "status": "complete"}
    rep["shim"] = dict(boot.SHIM_REPORT)
    try:
        import huggingface_hub as hfh
        import inspect
        rep["huggingface_hub"] = getattr(hfh, "__version__", "?")
        rep["snapshot_download_has_local_dir_use_symlinks"] = (
            "local_dir_use_symlinks" in inspect.signature(hfh.snapshot_download).parameters)
    except Exception as exc:  # pragma: no cover
        rep["huggingface_hub"] = f"error: {exc}"
    rep["torch"] = torch.__version__
    rep["cuda_available"] = bool(torch.cuda.is_available())
    if rep["cuda_available"]:
        try:
            free, total = torch.cuda.mem_get_info(0)
            rep["gpu"] = torch.cuda.get_device_name(0)
            rep["vram_free_gb"] = round(free / 2**30, 1)
            rep["vram_total_gb"] = round(total / 2**30, 1)
        except Exception as exc:  # pragma: no cover
            rep["gpu"] = f"error: {exc}"
    rep["weights"] = models.weights_status(task)
    for label, path in (("disk_models", models.MODEL_CACHE),
                        ("disk_runpod_volume", "/runpod-volume"),
                        ("disk_tmp", "/tmp")):
        try:
            u = shutil.disk_usage(path)
            rep[label] = {"path": path, "free_gb": round(u.free / 2**30, 1), "total_gb": round(u.total / 2**30, 1)}
        except Exception:
            rep[label] = {"path": path, "free_gb": None}
    rep["ffmpeg"] = shutil.which("ffmpeg")
    rep["output"] = {
        "s3_bucket_set": bool(storage.S3_BUCKET),
        "s3_endpoint_url_set": bool(storage.S3_ENDPOINT_URL),
        "max_output_mb": MAX_OUTPUT_MB,
    }
    rep["supported_sizes"] = generator.supported_sizes(task)
    rep["ok"] = bool(rep["shim"].get("model_binding_patched")) and rep["cuda_available"]
    if not rep["ok"]:
        rep["status"] = "error"
        rep["error"] = "selftest failed: " + (
            "SDPA patch did not reach wan.modules.model" if not rep["shim"].get("model_binding_patched")
            else "CUDA not available")
    return rep


def handler(job):
    inp = job.get("input") or {}
    task = _pick(inp, "task", DEFAULT_TASK)
    out_path = compact_path = image_path = None
    try:
        if task not in generator._PIPE_CLASSES:
            raise ValueError(f"unsupported task '{task}'; choose from {sorted(generator._PIPE_CLASSES)}")

        if inp.get("op") == "selftest":
            return selftest(task)

        # Refuse to spend GPU minutes on a worker whose attention patch is not in
        # place: the flash-attn assert would only fire after weights are loaded.
        if not boot.SHIM_REPORT.get("model_binding_patched"):
            raise RuntimeError(
                "SDPA patch did not reach wan.modules.model on this worker; "
                f"shim report: {boot.SHIM_REPORT}")

        def progress(msg):
            try:
                runpod.serverless.progress_update(job, msg)
            except Exception:
                pass

        image_path = _resolve_image(_pick(inp, "image"))
        size = _pick(inp, "size") or ("1280*704" if task == "ti2v-5B" else "1280*720")
        seed = int(_pick(inp, "seed", -1))
        if seed < 0:
            # Draw it here so the result can report a reproducible seed.
            seed = random.randint(0, 2**31 - 1)

        t_job = time.time()
        out_path, info = generator.generate(
            task=task,
            prompt=_pick(inp, "prompt"),
            image_path=image_path,
            size=size,
            frame_num=int(_pick(inp, "frame_num", 81)),
            steps=_pick(inp, "steps"),
            shift=_pick(inp, "shift"),
            guide_scale=_pick(inp, "guide_scale"),
            n_prompt=_pick(inp, "n_prompt", ""),
            seed=seed,
            offload=bool(_pick(inp, "offload", True)),
            solver=_pick(inp, "solver", "unipc"),
            progress=progress,
        )

        result = {"status": "complete", **info}

        # 1) object storage, if configured
        output_key = _pick(inp, "output_key")
        if storage.S3_BUCKET:
            progress("uploading")
            url = storage.upload_to_s3(out_path, output_key)
            if url:
                result["video"] = url
                result["video_bytes"] = os.path.getsize(out_path)
                result["delivery"] = "s3"
        elif output_key:
            result["warning"] = "output_key given but S3_BUCKET is not configured; returning inline"

        # 2) inline base64, size-checked against RunPod's output limit
        if "video" not in result:
            progress("compacting")
            try:
                compact_path = storage.compact_mp4(out_path)
                inline_src, encoded = compact_path, "libx264 crf23 yuv420p"
            except Exception as exc:
                log.warning("compact re-encode failed (%s); trying the raw file", exc)
                inline_src, encoded = out_path, "wan save_video (quality=8)"
            b64 = storage.to_base64(inline_src)
            limit = int(MAX_OUTPUT_MB * 1024 * 1024)
            result["video_bytes"] = os.path.getsize(inline_src)
            result["encoded"] = encoded
            if len(b64) <= limit:
                result["video_b64"] = b64
                result["delivery"] = "inline"
            else:
                raise RuntimeError(
                    f"video is {result['video_bytes']} bytes ({len(b64)} as base64), over the "
                    f"{MAX_OUTPUT_MB} MB inline limit and no S3_BUCKET is configured. "
                    "Configure object storage or request fewer frames / smaller size.")

        result["t_total_s"] = round(time.time() - t_job, 1)
        return result
    except Exception:
        tb_text = boot.report_failure(f"job-{job.get('id', '?')}-{task}")
        return {"task": task, "status": "error", "error": tb_text}
    finally:
        _rm(out_path)
        _rm(compact_path)
        _rm(image_path)


log.info("wan worker starting (task=%s, shim=%s)", DEFAULT_TASK, boot.SHIM_REPORT)
runpod.serverless.start({"handler": handler})
