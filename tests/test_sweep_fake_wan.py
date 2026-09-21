"""End-to-end check of _force_sdpa_attention against a fake `wan` package that
mirrors Wan2.2's real import graph (verified against upstream main 2026-09-21):
  wan/__init__.py            from . import configs, distributed, modules ...
  wan/modules/__init__.py    from .attention import flash_attention   (re-export)
  wan/modules/model.py       from .attention import flash_attention   (call site)
  wan/distributed/ulysses.py from ..modules.attention import flash_attention
The model's forward must (a) not hit the flash assert and (b) compute the
right numbers through the patched binding."""
import math
import os
import sys
import tempfile
import textwrap

import torch

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

tmp = tempfile.mkdtemp()
pkg = os.path.join(tmp, "wan")
os.makedirs(os.path.join(pkg, "modules"))
os.makedirs(os.path.join(pkg, "distributed"))
os.makedirs(os.path.join(pkg, "configs"))

files = {
    "__init__.py": "from . import configs, distributed, modules\nfrom .textimage2video import WanTI2V\n",
    "configs/__init__.py": "",
    "distributed/__init__.py": "",
    "distributed/ulysses.py": "from ..modules.attention import flash_attention\n",
    "distributed/sequence_parallel.py": "from .ulysses import flash_attention as _fa\n",
    "distributed/lazy_only.py": "from ..modules.attention import flash_attention\n",
    "textimage2video.py": "from .distributed.sequence_parallel import _fa\nfrom .modules.model import WanModel\nclass WanTI2V: pass\n",
    "modules/__init__.py": "from .attention import flash_attention\nfrom .model import WanModel\n",
    "modules/attention.py": textwrap.dedent('''
        import torch
        FLASH_ATTN_3_AVAILABLE = False
        FLASH_ATTN_2_AVAILABLE = False
        def flash_attention(q, k, v, q_lens=None, k_lens=None, dropout_p=0., softmax_scale=None,
                            q_scale=None, causal=False, window_size=(-1, -1), deterministic=False,
                            dtype=torch.bfloat16, version=None):
            assert FLASH_ATTN_2_AVAILABLE
            raise RuntimeError("unreachable")
        def attention(q, k, v, **kw):
            return flash_attention(q, k, v, **kw)
    '''),
    "modules/model.py": textwrap.dedent('''
        import torch
        from .attention import flash_attention
        class WanModel:
            window_size = (-1, -1)
            def self_attn(self, q, k, v, seq_lens):
                return flash_attention(q=q, k=k, v=v, k_lens=seq_lens, window_size=self.window_size)
            def cross_attn(self, q, k, v, context_lens):
                return flash_attention(q, k, v, k_lens=context_lens)
    '''),
}
for rel, body in files.items():
    if body is None:
        continue
    with open(os.path.join(pkg, rel), "w") as f:
        f.write(body)

sys.path.insert(0, tmp)
for m in [m for m in sys.modules if m == "wan" or m.startswith("wan.")]:
    del sys.modules[m]

import app.boot as boot  # noqa: E402

# --- control: before the patch, the model call reproduces the production assert
import wan  # noqa: E402
m = wan.modules.model.WanModel()
q = torch.randn(1, 10, 4, 8)
try:
    m.self_attn(q, q, q, torch.tensor([10]))
    raise SystemExit("control failed: assert did not fire")
except AssertionError:
    print("control: AssertionError (FLASH_ATTN_2_AVAILABLE) reproduced before patch")

# --- patch
boot._force_sdpa_attention()
rep = boot.SHIM_REPORT
print("patched:", rep["patched"])
assert rep["sdpa_installed"]
assert rep["model_binding_patched"]
assert "wan.modules.model.flash_attention" in rep["patched"]
assert "wan.modules.flash_attention" in rep["patched"]
assert "wan.distributed.ulysses.flash_attention" in rep["patched"]
assert "wan.modules.attention.flash_attention" in rep["patched"]
assert "wan.modules.attention.attention" in rep["patched"]


# --- after: model call must run AND be numerically right
def reference(q, k, v):
    b, lq, n, c = q.shape
    out = torch.empty(b, lq, n, v.shape[-1])
    for bi in range(b):
        for h in range(n):
            s = (q[bi, :, h] @ k[bi, :, h].T) / math.sqrt(c)
            out[bi, :, h] = torch.softmax(s, -1) @ v[bi, :, h]
    return out


torch.manual_seed(1)
q = torch.randn(1, 10, 4, 8)
k = torch.randn(1, 10, 4, 8)
v = torch.randn(1, 10, 4, 8)
got = m.self_attn(q, k, v, torch.tensor([10]))          # bf16 default dtype path
assert got.shape == (1, 10, 4, 8)
assert (got.float() - reference(q, k, v)).abs().max().item() < 0.1

# cross-attention with Lq != Lk (the case the old shim crashed on)
kc = torch.randn(1, 37, 4, 8)
vc = torch.randn(1, 37, 4, 8)
got = m.cross_attn(q, kc, vc, None)
assert got.shape == (1, 10, 4, 8)
assert (got.float() - reference(q, kc, vc)).abs().max().item() < 0.1

# aliased re-export ("import ... as _fa") is caught by identity, not name
assert "wan.distributed.sequence_parallel._fa" in rep["patched"]

# a module imported only AFTER the sweep must still receive the patched function,
# because the canonical name on wan.modules.attention was rebound too
import wan.distributed.lazy_only as lazy  # noqa: E402
assert lazy.flash_attention is wan.modules.attention.flash_attention
assert lazy.flash_attention.__name__ == "sdpa_flash_attention"

# idempotent second call must not re-patch / break
boot._force_sdpa_attention()
print("SWEEP + END-TO-END CHECKS PASSED")
