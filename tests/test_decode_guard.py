"""The VAE decode guard: clears cache, retries once in bf16 on CUDA OOM without
losing the latents, reports what it did, and is idempotent."""
import os
import sys
import types

import torch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

# stub wan so app.generator imports on a CPU box
wan = types.ModuleType("wan")
wan.WanT2V = wan.WanI2V = wan.WanTI2V = object
cfgs = types.ModuleType("wan.configs")
cfgs.MAX_AREA_CONFIGS, cfgs.SIZE_CONFIGS, cfgs.SUPPORTED_SIZES, cfgs.WAN_CONFIGS = {}, {}, {}, {}
utils = types.ModuleType("wan.utils"); uu = types.ModuleType("wan.utils.utils"); uu.save_video = None
sys.modules.update({"wan": wan, "wan.configs": cfgs, "wan.utils": utils, "wan.utils.utils": uu})
hub = types.ModuleType("huggingface_hub"); hub.snapshot_download = None; sys.modules["huggingface_hub"] = hub

import app.generator as G  # noqa: E402


class FakeModel:
    def __init__(self):
        self.dtype = torch.float32
        self.cleared = 0
    def to(self, dtype):
        self.dtype = dtype
        return self
    def clear_cache(self):
        self.cleared += 1


class FakeVAE:
    def __init__(self, fail_first):
        self.dtype = torch.float32
        self.model = FakeModel()
        self.fail_first = fail_first
        self.calls = []
    def decode(self, zs):
        self.calls.append((self.dtype, self.model.dtype))
        if self.fail_first and len(self.calls) == 1:
            raise torch.cuda.OutOfMemoryError("CUDA out of memory. Tried to allocate 2.60 GiB")
        return [z * 2 for z in zs]


# 1. OOM once -> retried in bf16, latents intact, state reported
pipe = types.SimpleNamespace(vae=FakeVAE(fail_first=True))
G._install_decode_guard(pipe)
G._install_decode_guard(pipe)  # idempotent: must not double-wrap
zs = [torch.ones(2, 3)]
out = pipe.vae.decode(zs)
assert torch.equal(out[0], torch.ones(2, 3) * 2)
assert pipe.vae.calls == [(torch.float32, torch.float32), (torch.bfloat16, torch.bfloat16)], pipe.vae.calls
assert pipe.vae.model.cleared == 1
assert G.DECODE_STATE == {"vae_decode_dtype": "torch.bfloat16", "vae_decode_retried": True}

# 2. no OOM -> single fp32 decode, state says so
pipe2 = types.SimpleNamespace(vae=FakeVAE(fail_first=False))
G._install_decode_guard(pipe2)
pipe2.vae.decode(zs)
assert pipe2.vae.calls == [(torch.float32, torch.float32)]
assert G.DECODE_STATE == {"vae_decode_dtype": "torch.float32", "vae_decode_retried": False}

# 3. a non-OOM error is not swallowed
class Boom(FakeVAE):
    def decode(self, zs):
        raise RuntimeError("something else")
pipe3 = types.SimpleNamespace(vae=Boom(False))
G._install_decode_guard(pipe3)
try:
    pipe3.vae.decode(zs); raise SystemExit("should have raised")
except RuntimeError as e:
    assert "something else" in str(e)

print("DECODE GUARD CHECKS PASSED")
