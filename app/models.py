import glob
import logging
import os
import threading

from huggingface_hub import snapshot_download

log = logging.getLogger("wan-models")

# Where weights are downloaded when no pre-staged copy exists (container disk).
MODEL_CACHE = os.environ.get("MODEL_CACHE", "/models")

# RunPod "cached models": the endpoint's Model field (or `runpodctl serverless
# update --model-reference`) makes RunPod pre-stage a Hugging Face repo on the
# host, unbilled, and expose it in HF hub-cache layout at
#   /runpod-volume/huggingface-cache/hub/models--{org}--{name}/snapshots/{hash}/
# The docs say custom workers must resolve that path themselves, so we do.
RUNPOD_MODEL_CACHE = os.environ.get(
    "RUNPOD_MODEL_CACHE", "/runpod-volume/huggingface-cache/hub")

TASKS = {
    "t2v-A14B": {"repo": "Wan-AI/Wan2.2-T2V-A14B"},
    "i2v-A14B": {"repo": "Wan-AI/Wan2.2-I2V-A14B"},
    "ti2v-5B": {"repo": "Wan-AI/Wan2.2-TI2V-5B"},
    # Reference-to-video (subject reference images + text, no start frame).
    # Wan2.1 codebase (image built with WAN_REPO=Wan2.1); ~75 GB on disk, so it
    # MUST come from the RunPod cached-model slot -- the selftest reports whether
    # a snapshot is present and the client scripts refuse to run without one.
    "vace-14B": {"repo": "Wan-AI/Wan2.1-VACE-14B"},
}

# A snapshot is only usable if these exist (guards against a half-staged dir).
# Wan2.2 config names: config.t5_checkpoint / config.vae_checkpoint.
REQUIRED_FILES = {
    "t2v-A14B": ("models_t5_umt5-xxl-enc-bf16.pth", "Wan2.1_VAE.pth"),
    "i2v-A14B": ("models_t5_umt5-xxl-enc-bf16.pth", "Wan2.1_VAE.pth"),
    "ti2v-5B": ("models_t5_umt5-xxl-enc-bf16.pth", "Wan2.2_VAE.pth"),
    "vace-14B": ("models_t5_umt5-xxl-enc-bf16.pth", "Wan2.1_VAE.pth",
                 "diffusion_pytorch_model.safetensors.index.json"),
}

_locks = {}


def list_tasks():
    return sorted(TASKS)


def repo_for(task: str) -> str:
    return TASKS[task]["repo"]


def _complete(path: str, task: str) -> bool:
    return all(os.path.isfile(os.path.join(path, f)) for f in REQUIRED_FILES[task])


def find_cached_snapshot(task: str, cache_root: str = None) -> str | None:
    """Return the RunPod-staged snapshot dir for the task's repo, or None."""
    root = cache_root or RUNPOD_MODEL_CACHE
    repo = TASKS[task]["repo"]
    base = os.path.join(root, "models--" + repo.replace("/", "--"), "snapshots")
    candidates = sorted(glob.glob(os.path.join(base, "*")), key=os.path.getmtime, reverse=True)
    for cand in candidates:
        if os.path.isdir(cand) and _complete(cand, task):
            return cand
    if candidates:
        log.warning("model cache has %s but no complete snapshot (checked %d)", base, len(candidates))
    return None


def ensure_model(task: str) -> str:
    """Return a checkpoint dir for `task`, preferring RunPod's pre-staged cache.

    Order:
      1. RunPod cached model (host-side, unbilled) -- see RUNPOD_MODEL_CACHE.
      2. Already-downloaded copy under MODEL_CACHE/<task> on this worker.
      3. Download from Hugging Face into MODEL_CACHE/<task> (billed worker time,
         ~34 GB for TI2V-5B; this is the path to avoid in production).
    """
    if task not in TASKS:
        raise ValueError(f"unknown task '{task}'; choose from {list_tasks()}")

    lock = _locks.setdefault(task, threading.Lock())
    with lock:
        cached = find_cached_snapshot(task)
        if cached:
            log.info("weights for %s: RunPod cached model at %s", task, cached)
            return cached

        ckpt = os.path.join(MODEL_CACHE, task)
        if os.path.isdir(ckpt) and _complete(ckpt, task):
            log.info("weights for %s: local copy at %s", task, ckpt)
            return ckpt

        log.warning(
            "weights for %s: no cached model found under %s; downloading %s to %s "
            "(billed). Attach the model to the endpoint (RunPod 'Model' field / "
            "--model-reference) to avoid this.",
            task, RUNPOD_MODEL_CACHE, TASKS[task]["repo"], ckpt,
        )
        os.makedirs(ckpt, exist_ok=True)
        # NOTE: `local_dir_use_symlinks` was deprecated in huggingface_hub 0.23
        # and REMOVED in 1.0; a plain `local_dir` writes real files on both.
        snapshot_download(repo_id=TASKS[task]["repo"], local_dir=ckpt)
        if not _complete(ckpt, task):
            raise RuntimeError(f"download of {TASKS[task]['repo']} to {ckpt} is incomplete")
        return ckpt


def weights_status(task: str) -> dict:
    """Cheap, no-download report for the selftest op."""
    ckpt = os.path.join(MODEL_CACHE, task)
    return {
        "task": task,
        "repo": TASKS[task]["repo"],
        "runpod_cache_root": RUNPOD_MODEL_CACHE,
        "runpod_cache_root_exists": os.path.isdir(RUNPOD_MODEL_CACHE),
        "runpod_cached_snapshot": find_cached_snapshot(task),
        "local_copy": ckpt if (os.path.isdir(ckpt) and _complete(ckpt, task)) else None,
    }
