"""Numerical check: the SDPA replacement must equal flash_attention semantics on
Wan's [B, L, N, C] layout. Reference = explicit per-head softmax attention.
Also demonstrates that the OLD shim (no transpose) is wrong."""
import math
import os
import sys

import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.boot import make_sdpa_flash_attention  # noqa: E402

torch.manual_seed(0)


def reference(q, k, v, k_lens=None, q_scale=None, softmax_scale=None):
    # q,k,v: [B, L, N, C] float32
    b, lq, n, c = q.shape
    lk = k.shape[1]
    if q_scale is not None:
        q = q * q_scale
    scale = softmax_scale if softmax_scale is not None else 1.0 / math.sqrt(c)
    out = torch.empty(b, lq, n, v.shape[-1])
    for bi in range(b):
        for h in range(n):
            s = (q[bi, :, h] @ k[bi, :, h].T) * scale  # [Lq, Lk]
            if k_lens is not None:
                s[:, k_lens[bi]:] = float("-inf")
            p = torch.softmax(s, dim=-1)
            out[bi, :, h] = p @ v[bi, :, h]
    return out


def old_shim(q, k, v, **kw):
    return F.scaled_dot_product_attention(q, k, v, scale=q.size(-1) ** -0.5)


sdpa = make_sdpa_flash_attention(torch, F)

B, LQ, LK, N, C = 2, 37, 53, 4, 16
q = torch.randn(B, LQ, N, C)
k = torch.randn(B, LK, N, C)
v = torch.randn(B, LK, N, C)

# 1. plain (self-attn style, k_lens == full length) in float32 (dtype passthrough for exactness)
ref = reference(q, k, v)
got = sdpa(q, k, v, k_lens=torch.tensor([LK, LK]), dtype=torch.float32)
assert got.shape == ref.shape, (got.shape, ref.shape)
err = (got - ref).abs().max().item()
print("plain max abs err:", err)
assert err < 1e-4

# 2. cross-attn style: k_lens=None
got = sdpa(q, k, v, dtype=torch.float32)
assert (got - ref).abs().max().item() < 1e-4

# 3. q_scale + explicit softmax_scale
ref = reference(q, k, v, q_scale=0.7, softmax_scale=0.11)
got = sdpa(q, k, v, q_scale=0.7, softmax_scale=0.11, dtype=torch.float32)
assert (got - ref).abs().max().item() < 1e-4

# 4. padded keys (batch>1, ragged k_lens) -> mask must apply
k_lens = torch.tensor([LK, 20])
ref = reference(q, k, v, k_lens=k_lens)
got = sdpa(q, k, v, k_lens=k_lens, dtype=torch.float32)
err = (got - ref).abs().max().item()
print("masked max abs err:", err)
assert err < 1e-4

# 5. bf16 in -> bf16 out, values close to float32 reference
qb, kb, vb = q.bfloat16(), k.bfloat16(), v.bfloat16()
got = sdpa(qb, kb, vb, k_lens=torch.tensor([LK, LK]))
assert got.dtype == torch.bfloat16
err = (got.float() - reference(q, k, v)).abs().max().item()
print("bf16 max abs err:", err)
assert err < 0.1

# 6. both kwarg spellings accepted
sdpa(q, k, v, version=None, dtype=torch.float32)
sdpa(q, k, v, fa_version=None, dtype=torch.float32)

# 7. the OLD shim is wrong on this layout (demonstration).
#    (a) cross-attention (Lq != Lk, e.g. video tokens vs 512 text tokens): crashes
try:
    old_shim(q, k, v)
    raise AssertionError("old shim unexpectedly accepted Lq != Lk")
except RuntimeError as exc:
    print("OLD shim, Lq != Lk -> RuntimeError:", str(exc)[:70])
#    (b) self-attention (Lq == Lk): runs, but attends across heads -> garbage
ks, vs = torch.randn(B, LQ, N, C), torch.randn(B, LQ, N, C)
bad = old_shim(q, ks, vs)
ref = reference(q, ks, vs)
print("OLD shim, Lq == Lk -> max abs err vs reference:", (bad - ref).abs().max().item())
assert (bad - ref).abs().max().item() > 0.5

print("ALL SDPA NUMERIC CHECKS PASSED")
