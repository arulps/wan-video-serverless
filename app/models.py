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
            snapshot_download(
                repo_id=TASKS[task]["repo"],
                local_dir=ckpt,
                local_dir_use_symlinks=False,
            )
    return ckpt