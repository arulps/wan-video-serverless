import os
import threading

import torch
import wan
from PIL import Image
from wan.configs import WAN_CONFIGS, MAX_AREA_CONFIGS, SIZE_CONFIGS
from wan.utils.utils import save_video

from . import models

_pipes = {}
_pipes_lock = threading.Lock()

_PIPE_CLASSES = {
    "t2v-A14B": wan.WanT2V,
    "i2v-A14B": wan.WanI2V,
    "ti2v-5B": wan.WanTI2V,
}

SUPPORTED_SIZES = sorted(SIZE_CONFIGS.keys())
valid_frame_num = lambda n: isinstance(n, int) and (n - 1) % 4 == 0 and n > 0


def _get_pipe(task: str, ckpt_dir: str):
    with _pipes_lock:
        if task not in _pipes:
            cfg = WAN_CONFIGS[task]
            low_vram = "5B" in task or os.environ.get("T5_CPU", "0") == "1"
            _pipes[task] = _PIPE_CLASSES[task](
                config=cfg,
                checkpoint_dir=ckpt_dir,
                device_id=0,
                rank=0,
                t5_cpu=low_vram,
                convert_model_dtype=True,
            )
        return _pipes[task]


def _to_size(size: str, task: str):
    if size not in SIZE_CONFIGS:
        raise ValueError(f"unknown size '{size}'; choose from {SUPPORTED_SIZES}")
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
) -> str:
    if not prompt:
        raise ValueError("prompt is required")
    if not valid_frame_num(frame_num):
        raise ValueError("frame_num must be a positive 4n+1 value, e.g. 81, 97, 121")

    if task not in models.TASKS:
        raise ValueError(f"unknown task '{task}'; choose from {models.list_tasks()}")

    cfg = WAN_CONFIGS[task]
    ckpt_dir = models.ensure_model(task)
    pipe = _get_pipe(task, ckpt_dir)

    steps = int(steps) if steps is not None else int(getattr(cfg, "sample_steps", 40))
    shift = float(shift) if shift is not None else float(getattr(cfg, "sample_shift", 5.0))
    if guide_scale is None:
        guide_scale = getattr(cfg, "sample_guide_scale", 5.0)
    if isinstance(guide_scale, list):
        guide_scale = tuple(guide_scale)
    seed = int(seed)

    img = None
    if image_path:
        img = Image.open(image_path).convert("RGB")

    if task == "t2v-A14B":
        video = pipe.generate(
            input_prompt=prompt,
            size=_to_size(size, task),
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
        w, h = _to_size(size, task)
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
            seed=seed,
            offload_model=offload,
        )
    else:
        w, h = _to_size(size, task)
        video = pipe.generate(
            input_prompt=prompt,
            img=img,
            max_area=MAX_AREA_CONFIGS.get(size, w * h),
            frame_num=frame_num,
            shift=shift,
            sample_solver=solver,
            sampling_steps=steps,
            guide_scale=guide_scale,
            seed=seed,
            offload_model=offload,
        )

    from .storage import temp_output_file

    out = temp_output_file(".mp4")
    fps = int(getattr(cfg, "sample_fps", 16))
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
    return out