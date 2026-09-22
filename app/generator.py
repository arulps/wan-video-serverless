import gc
import inspect
import logging
import os
import threading
import time

import torch
import wan
from PIL import Image
from wan.configs import SIZE_CONFIGS, SUPPORTED_SIZES, WAN_CONFIGS

try:  # Wan2.2 name
    from wan.utils.utils import save_video
except ImportError:  # Wan2.1 name (same signature: tensor, save_file, fps, nrow, normalize, value_range)
    from wan.utils.utils import cache_video as save_video
try:  # Wan2.1 has no MAX_AREA_CONFIGS for ti2v; only the 2.2 branches use it
    from wan.configs import MAX_AREA_CONFIGS
except ImportError:
    MAX_AREA_CONFIGS = {}

from . import models

log = logging.getLogger("wan-generator")

_pipes = {}
_pipes_lock = threading.Lock()

# The image is built from ONE Wan codebase (Dockerfile ARG WAN_REPO):
#   Wan2.2 -> WanT2V / WanI2V / WanTI2V   (tasks t2v-A14B, i2v-A14B, ti2v-5B)
#   Wan2.1 -> WanVace                     (task vace-14B: reference-to-video)
# Both repos install as the `wan` package, so the task table is built from what
# this image's `wan` actually exposes AND what its WAN_CONFIGS knows. A task
# that is not in the table is refused by the handler before any GPU time.
_TASK_CLASS_NAMES = {
    "t2v-A14B": "WanT2V",
    "i2v-A14B": "WanI2V",
    "ti2v-5B": "WanTI2V",
    "vace-14B": "WanVace",
}
_PIPE_CLASSES = {
    task: getattr(wan, name)
    for task, name in _TASK_CLASS_NAMES.items()
    if task in WAN_CONFIGS and getattr(wan, name, None) is not None
}
WAN_REPO = os.environ.get("WAN_REPO", "Wan2.2")

# What dtype the DiT parameters ended up in for each loaded pipeline (reported).
DIT_DTYPES = {}

# Filled in by the decode guard for the last job (reported in the result).
DECODE_STATE = {"vae_decode_dtype": None, "vae_decode_retried": False}


def _install_decode_guard(pipe):
    """Wrap pipe.vae.decode so a CUDA OOM in the VAE decode does not lose the
    sampled latents.

    Observed 2026-09-21 (job caf3f7b9, RTX 4090 24 GB, ti2v-5B 1280x704x81f):
    all sampling steps completed, then `vae.decode` died allocating 2.60 GiB
    with 4.17 GiB reserved-but-unallocated. Wan2.2's decoder runs in fp32 with
    160 channels at full resolution (one 4-frame activation ~2.3-2.6 GiB) and
    grows its output with `torch.cat` on every latent frame, which fragments
    the caching allocator. PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
    (set in the Dockerfile and template env) addresses the fragmentation; this
    guard is the second line: it clears the cache first and, on OOM, retries
    the decode with the VAE in bfloat16 (halves activation memory; upstream
    vae2_2.py already carries a bf16 compatibility fix for its upsampler).
    The latents are still referenced here, so the retry costs seconds, not a
    5-minute resample."""
    if getattr(pipe, "_decode_guarded", False):
        return
    vae = pipe.vae
    orig_decode = vae.decode

    def _mem():
        try:
            free, total = torch.cuda.mem_get_info(0)
            return ("free=%.2fGiB total=%.2fGiB allocated=%.2fGiB reserved=%.2fGiB" % (
                free / 2**30, total / 2**30,
                torch.cuda.memory_allocated() / 2**30, torch.cuda.memory_reserved() / 2**30))
        except Exception as exc:  # pragma: no cover
            return "mem stats unavailable: %s" % exc

    def guarded_decode(zs):
        DECODE_STATE["vae_decode_dtype"] = str(getattr(vae, "dtype", "?"))
        DECODE_STATE["vae_decode_retried"] = False
        gc.collect()
        torch.cuda.empty_cache()
        log.info("VAE decode start (%s): %s", getattr(vae, "dtype", "?"), _mem())
        try:
            return orig_decode(zs)
        except torch.cuda.OutOfMemoryError as exc:
            first = str(exc).splitlines()[0][:200]
            log.warning("VAE decode OOM in %s: %s | %s -- retrying in bfloat16",
                        getattr(vae, "dtype", "?"), first, _mem())
            try:
                vae.model.clear_cache()
            except Exception:
                pass
            gc.collect()
            torch.cuda.empty_cache()
            vae.model.to(torch.bfloat16)
            vae.dtype = torch.bfloat16
            DECODE_STATE["vae_decode_dtype"] = str(torch.bfloat16)
            DECODE_STATE["vae_decode_retried"] = True
            log.info("VAE decode retry (bf16): %s", _mem())
            try:
                return orig_decode(zs)
            except Exception as exc2:
                raise RuntimeError(
                    "VAE decode failed twice: fp32 OOM (%s) then bf16 retry raised %s: %s | %s"
                    % (first, type(exc2).__name__, str(exc2).splitlines()[0][:300], _mem())
                ) from exc2
        except Exception as exc:
            # Not an OOM: surface the type and memory state so it can't be mistaken for one.
            raise RuntimeError(
                "VAE decode raised %s (not OOM) in %s: %s | %s"
                % (type(exc).__name__, getattr(vae, "dtype", "?"),
                   str(exc).splitlines()[0][:300], _mem())
            ) from exc

    vae.decode = guarded_decode
    pipe._decode_guarded = True


def valid_frame_num(n):
    return isinstance(n, int) and (n - 1) % 4 == 0 and n > 0


def supported_sizes(task: str):
    return tuple(SUPPORTED_SIZES.get(task, ()))


def _force_bf16_from_pretrained(dtype):
    """Wan2.1 has no `convert_model_dtype`: `WanVace.__init__` calls
    `VaceWanModel.from_pretrained(checkpoint_dir)` with no dtype and then moves
    the model to the GPU. The VACE-14B shards are ~63 GB (mostly fp32), so that
    path puts a 63 GB fp32 DiT on the card before anything can cast it -- too
    much for an 80 GB GPU once T5 and activations arrive. Wan2.2 solves this
    with `model.to(param_dtype)` before device placement (text2video.py
    _configure_model); for Wan2.1 the same effect is obtained by passing
    `torch_dtype=bf16` into diffusers' from_pretrained, which loads the shards
    straight into bf16 (~34 GB) with accelerate's low-CPU-memory path.
    Inference runs under autocast(bf16) either way, so numerics are unchanged."""
    try:
        from wan.modules import vace_model as vm
    except Exception:
        return False
    cls = vm.VaceWanModel
    if getattr(cls, "_bf16_from_pretrained_installed", False):
        return True
    orig = cls.from_pretrained  # bound classmethod

    def from_pretrained_bf16(*args, **kwargs):
        kwargs.setdefault("torch_dtype", dtype)
        return orig(*args, **kwargs)

    cls.from_pretrained = staticmethod(from_pretrained_bf16)
    cls._bf16_from_pretrained_installed = True
    log.info("VaceWanModel.from_pretrained now loads weights as %s", dtype)
    return True


def _get_pipe(task: str, ckpt_dir: str):
    with _pipes_lock:
        if task not in _pipes:
            cfg = WAN_CONFIGS[task]
            cls = _PIPE_CLASSES[task]
            low_vram = "5B" in task or os.environ.get("T5_CPU", "0") == "1"
            kwargs = dict(config=cfg, checkpoint_dir=ckpt_dir, device_id=0, rank=0, t5_cpu=low_vram)
            params = inspect.signature(cls.__init__).parameters
            if "convert_model_dtype" in params:          # Wan2.2 classes
                kwargs["convert_model_dtype"] = True
            elif task.startswith("vace"):                 # Wan2.1 WanVace
                _force_bf16_from_pretrained(cfg.param_dtype)
            t0 = time.time()
            pipe = cls(**kwargs)
            try:
                dit_dtype = str(next(pipe.model.parameters()).dtype)
            except Exception:
                dit_dtype = "?"
            DIT_DTYPES[task] = dit_dtype
            log.info("pipeline %s loaded from %s in %.1fs (dit dtype %s)", task, ckpt_dir, time.time() - t0, dit_dtype)
            _install_decode_guard(pipe)
            _pipes[task] = pipe
        return _pipes[task]


def _flatten_reference(path: str) -> str:
    """VACE's prepare_source does `Image.open(p).convert('RGB')` and pads onto a
    WHITE canvas; a transparent turnaround PNG converted that way gets black
    where it was transparent. Composite onto white first (no-op for RGB)."""
    img = Image.open(path)
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        rgba = img.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        out = Image.alpha_composite(bg, rgba).convert("RGB")
        dest = os.path.splitext(path)[0] + "-flat.png"
        out.save(dest)
        return dest
    return path


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
    ref_image_paths: list | None = None,
    context_scale: float = 1.0,
):
    """Run one generation. Returns (mp4_path, info) where info records the
    effective parameters (what actually ran, after defaults) and timings.

    `ref_image_paths` (vace-* only): 1..N subject reference images. The character
    identity comes from these; the scene, blocking and camera come from the
    prompt. `image_path` is the START FRAME for the i2v/ti2v tasks and is ignored
    by vace."""
    if not prompt:
        raise ValueError("prompt is required")
    if not valid_frame_num(frame_num):
        raise ValueError("frame_num must be a positive 4n+1 value, e.g. 81, 97, 121")
    if task not in models.TASKS:
        raise ValueError(f"unknown task '{task}'; choose from {models.list_tasks()}")
    if task not in _PIPE_CLASSES:
        raise ValueError(
            f"task '{task}' is not available in this image (built from {WAN_REPO}); "
            f"available: {sorted(_PIPE_CLASSES)}")
    is_vace = task.startswith("vace")
    if is_vace and image_path:
        raise ValueError("vace takes 'ref_images' (subject references), not 'image' (a start frame)")
    if not is_vace and ref_image_paths:
        raise ValueError(f"'ref_images' is only supported by the vace task, not {task}")
    ref_image_paths = [p for p in (ref_image_paths or []) if p]
    if is_vace and not ref_image_paths:
        raise ValueError("vace-14B needs at least one reference image in 'ref_images'")

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

    # Wan2.1 configs carry no sample_steps; upstream generate.py uses 50 for
    # t2v/vace and 40 for i2v.
    default_steps = 50 if is_vace else 40
    steps = int(steps) if steps is not None else int(getattr(cfg, "sample_steps", default_steps))
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

    try:
        gpu_name = torch.cuda.get_device_name(0)
    except Exception:
        gpu_name = None
    info = {
        "task": task, "size": size, "width": w, "height": h, "gpu": gpu_name,
        "frame_num": frame_num, "fps": fps, "duration_s": round(frame_num / fps, 3),
        "steps": steps, "shift": shift,
        "guide_scale": list(guide_scale) if isinstance(guide_scale, tuple) else guide_scale,
        "seed": seed, "solver": solver, "offload": bool(offload),
        "checkpoint_dir": ckpt_dir, "wan_repo": WAN_REPO, "dit_dtype": DIT_DTYPES.get(task),
        "t_weights_s": round(t_weights, 1), "t_load_s": round(t_load, 1),
    }
    if is_vace:
        info["ref_images"] = len(ref_image_paths)
        info["context_scale"] = float(context_scale)
    log.info("generate: %s", info)

    if progress:
        progress(f"sampling {steps} steps x {frame_num} frames @ {size}")
    t0 = time.time()
    if is_vace:
        # Reference-to-video: no source video, no mask -> prepare_source builds a
        # zero video + all-ones mask of the target size and pads each reference
        # onto a white canvas of that size (wan/vace.py). Refs must be flattened
        # first (transparent PNGs would go black in its convert("RGB")).
        flat_refs = [_flatten_reference(p) for p in ref_image_paths]
        src_video, src_mask, src_refs = pipe.prepare_source(
            [None], [None], [flat_refs], frame_num, (w, h), pipe.device)
        video = pipe.generate(
            prompt,
            src_video,
            src_mask,
            src_refs,
            size=(w, h),
            frame_num=frame_num,
            context_scale=float(context_scale),
            shift=shift,
            sample_solver=solver,
            sampling_steps=steps,
            guide_scale=guide_scale,
            n_prompt=n_prompt,
            seed=seed,
            offload_model=offload,
        )
        del src_video, src_mask, src_refs
    elif task == "t2v-A14B":
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
    info.update(DECODE_STATE)
    info["alloc_conf"] = os.environ.get("PYTORCH_CUDA_ALLOC_CONF")

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
