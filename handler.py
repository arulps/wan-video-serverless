import logging
import os

import app.boot as boot

boot.apply_cuda_shim()

import runpod  # noqa: E402

from app import generator, storage  # noqa: E402

log = logging.getLogger("wan-worker")
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())

DEFAULT_TASK = os.environ.get("DEFAULT_TASK", "ti2v-5B")
MAX_B64_MB = int(os.environ.get("MAX_B64_MB", "90"))


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


def handler(job):
    inp = job.get("input") or {}
    task = inp.get("task") or DEFAULT_TASK
    try:
        if task not in generator._PIPE_CLASSES:
            raise ValueError(f"unsupported task '{task}'; choose from {sorted(generator._PIPE_CLASSES)}")

        image_path = _resolve_image(inp.get("image"))
        size = inp.get("size") or ("1280*704" if task == "ti2v-5B" else "1280*720")

        out_path = generator.generate(
            task=task,
            prompt=inp.get("prompt"),
            image_path=image_path,
            size=size,
            frame_num=int(inp.get("frame_num", 81)),
            steps=inp.get("steps"),
            shift=inp.get("shift"),
            guide_scale=inp.get("guide_scale"),
            n_prompt=inp.get("n_prompt", ""),
            seed=int(inp.get("seed", -1)),
            offload=bool(inp.get("offload", True)),
            solver=inp.get("solver", "unipc"),
        )

        result = {"task": task, "size": size, "status": "complete"}

        if inp.get("output_key") or storage.S3_BUCKET:
            url = storage.upload_to_s3(out_path, inp.get("output_key"))
            if url:
                result["video"] = url
            else:
                result["video"] = storage.to_base64(out_path) if _under_limit(out_path) else None

        if "video" not in result:
            if _under_limit(out_path):
                result["video_b64"] = storage.to_base64(out_path)
            else:
                result["video_path"] = out_path
                log.warning("output exceeds %s MB; returning path on worker only", MAX_B64_MB)

        if os.path.exists(out_path) and os.path.getsize(out_path) <= MAX_B64_MB * 1024 * 1024:
            os.remove(out_path)
        if image_path:
            try:
                os.remove(image_path)
            except OSError:
                pass
        return result
    except Exception:
        tb_text = boot.report_failure(f"job-{job.get('id', '?')}-{task}")
        return {
            "task": task,
            "status": "error",
            "error": tb_text,
        }


def _under_limit(path: str) -> bool:
    return os.path.getsize(path) <= MAX_B64_MB * 1024 * 1024


log.info("wan worker starting (task=%s)", DEFAULT_TASK)
runpod.serverless.start({"handler": handler})