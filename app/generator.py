import logging
import os
import threading
import time

import torch
import wan
from PIL import Image
from wan.configs import MAX_AREA_CONFIGS, SIZE_CONFIGS, SUPPORTED_SIZES, WAN_CONFIGS
from wan.utils.utils import save_video

from . import models

log = logging.getLogger("wan-generator")

_pipes = {}
_pipes_lock = threading.Lock()

_PIPE_CLASSES = {
    "t2v-A14B": wan.WanT2V,
    "i2v-A14B": wan.WanI2V,
    "ti2v-5B": wan.WanTI2V,
}


def valid_frame_num(n):
    return isinstance(n, int) and (n - 1) % 4 == 0 and n > 0


def supported_sizes(task: str):
    return tuple(SUPPORTED_SIZES.get(task, ()))


def _get_pipe(task: str, ckpt_dir: str):
    with _pipes_lock:
        if task not in _pipes:
            cfg = WAN_CONFIGS[task]
            low_vram = "5B" in task or os.environ.get("T5_CPU", "0") == "1"
            t0 = time.time()
            _pipes[task] = _PIPE_CLASSES[task](
                config=cfg,
                checkpoint_dir=ckpt_dir,
                device_id=0,
                rank=0,
                t5_cpu=low_vram,
                convert_model_dtype=True,
            )
            log.info("pipeline %s loaded from %s in %.1fs", task, ckpt_dir, time.time() - t0)
        return _pipes[task]


def _to_size(size: str, task: str):
    if size not in SIZE_CONFIGS:
        raise ValueError(f"unknown size '{size}'; choose from {sorted(SIZE_CONFIGS)}")
    allowed = supported_sizes(task)
    if allowed and size not in allowed:
        raise ValueError(f"size '{size}' is not supported for {task}; choose from {allowed}")
    return SIZE_CONFIGS[size]


def generate(
    task: str,
    prompt: str,
    image_path: str | None = None,
    size: str = "1280*720",
    frame_num: int = 81,
    steps: int | None = None,
    shift: float | None = None,
    guide_scale=None,
    n_prompt: str = "",
    seed: int = -1,
    offload: bool = True,
    solver: str = "unipc",
    progress=None,
):
    """Run one generation. Returns (mp4_path, info) where info records the
    effective parameters (what actually ran, after defaults) and timings."""
    if not prompt:
        raise ValueError("prompt is required")
    if not valid_frame_num(frame_num):
        raise ValueError("frame_num must be a positive 4n+1 value, e.g. 81, 97, 121")
    if task not in models.TASKS:
        raise ValueError(f"unknown task '{task}'; choose from {models.list_tasks()}")

    cfg = WAN_CONFIGS[task]
    w, h = _to_size(size, task)

    if progress:
        progress("resolving weights")
    t0 = time.time()
    ckpt_dir = models.ensure_model(task)
    t_weights = time.time() - t0

    if progress:
        progress("loading pipeline")
    t0 = time.time()
    pipe = _get_pipe(task, ckpt_dir)
    t_load = time.time() - t0

    steps = int(steps) if steps is not None else int(getattr(cfg, "sample_steps", 40))
    shift = float(shift) if shift is not None else float(getattr(cfg, "sample_shift", 5.0))
    if guide_scale is None:
        guide_scale = getattr(cfg, "sample_guide_scale", 5.0)
    if isinstance(guide_scale, list):
        guide_scale = tuple(guide_scale)
    seed = int(seed)
    fps = int(getattr(cfg, "sample_fps", 16))

    img = None
    if image_path:
        img = Image.open(image_path).convert("RGB")

    info = {
        "task": task, "size": size, "width": w, "height": h,
        "frame_num": frame_num, "fps": fps, "duration_s": round(frame_num / fps, 3),
        "steps": steps, "shift": shift,
        "guide_scale": list(guide_scale) if isinstance(guide_scale, tuple) else guide_scale,
        "seed": seed, "solver": solver, "offload": bool(offload),
        "checkpoint_dir": ckpt_dir,
        "t_weights_s": round(t_weights, 1), "t_load_s": round(t_load, 1),
    }
    log.info("generate: %s", info)

    if progress:
        progress(f"sampling {steps} steps x {frame_num} frames @ {size}")
    t0 = time.time()
    if task == "t2v-A14B":
        video = pipe.generate(
            input_prompt=prompt,
            size=(w, h),
            frame_num=frame_num,
            shift=shift,
            sample_solver=solver,
            sampling_steps=steps,
            guide_scale=guide_scale,
            n_prompt=n_prompt,
            seed=seed,
            offload_model=offload,
        )
    elif task == "ti2v-5B":
        video = pipe.generate(
            input_prompt=prompt,
            img=img,
            size=(w, h),
            max_area=MAX_AREA_CONFIGS.get(size, w * h),
            frame_num=frame_num,
            shift=shift,
            sample_solver=solver,
            sampling_steps=steps,
            guide_scale=guide_scale,
            n_prompt=n_prompt,
            seed=seed,
            offload_model=offload,
        )
    else:
        video = pipe.generate(
            input_prompt=prompt,
            img=img,
            max_area=MAX_AREA_CONFIGS.get(size, w * h),
            frame_num=frame_num,
            shift=shift,
            sample_solver=solver,
            sampling_steps=steps,
            guide_scale=guide_scale,
            n_prompt=n_prompt,
            seed=seed,
            offload_model=offload,
        )
    info["t_sample_s"] = round(time.time() - t0, 1)

    from .storage import temp_output_file

    if progress:
        progress("encoding")
    out = temp_output_file(".mp4")
    # Wan's save_video swallows exceptions (logs at INFO) and leaves no file, so
    # existence and size are checked here rather than trusted.
    save_video(
        tensor=video[None],
        save_file=out,
        fps=fps,
        nrow=1,
        normalize=True,
        value_range=(-1, 1),
    )
    del video
    if offload:
        torch.cuda.empty_cache()
    if not os.path.isfile(out) or os.path.getsize(out) == 0:
        raise RuntimeError("save_video produced no file - imageio/ffmpeg failure; see worker log")
    info["raw_bytes"] = os.path.getsize(out)
    return out, info
