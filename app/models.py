import os
import threading

from huggingface_hub import snapshot_download

MODEL_CACHE = os.environ.get("MODEL_CACHE", "/models")

TASKS = {
    "t2v-A14B": {"repo": "Wan-AI/Wan2.2-T2V-A14B"},
    "i2v-A14B": {"repo": "Wan-AI/Wan2.2-I2V-A14B"},
    "ti2v-5B": {"repo": "Wan-AI/Wan2.2-TI2V-5B"},
}

_locks = {}


def list_tasks():
    return sorted(TASKS)


def repo_for(task: str) -> str:
    return TASKS[task]["repo"]


def ensure_model(task: str) -> str:
    if task not in TASKS:
        raise ValueError(f"unknown task '{task}'; choose from {list_tasks()}")
    ckpt = os.path.join(MODEL_CACHE, task)
    lock = _locks.setdefault(task, threading.Lock())
    with lock:
        if not os.path.isdir(ckpt) or not os.listdir(ckpt):
            os.makedirs(ckpt, exist_ok=True)
            # NOTE: `local_dir_use_symlinks` was deprecated in huggingface_hub
            # 0.23 and REMOVED in 1.0.  requirements.txt asks for >=0.24 with no
            # ceiling, so a fresh build resolves to 1.x and passing that kwarg
            # raises TypeError on the very first job -- the worker boots clean,
            # accepts the job, then dies.  Since 0.23 a plain `local_dir` already
            # writes real files rather than symlinks, so dropping it is a no-op
            # on old versions and a fix on new ones.
            snapshot_download(
                repo_id=TASKS[task]["repo"],
                local_dir=ckpt,
            )
    return ckpt