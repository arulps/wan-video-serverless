"""Cache resolver + fallback order for app.models (no network)."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import app.models as M  # noqa: E402

root = tempfile.mkdtemp()
assert M.find_cached_snapshot("ti2v-5B", root) is None

snap_bad = os.path.join(root, "models--Wan-AI--Wan2.2-TI2V-5B", "snapshots", "aaaa")
os.makedirs(snap_bad)
open(os.path.join(snap_bad, "Wan2.2_VAE.pth"), "w").close()
assert M.find_cached_snapshot("ti2v-5B", root) is None, "half-staged snapshot must be rejected"

blobs = os.path.join(root, "models--Wan-AI--Wan2.2-TI2V-5B", "blobs")
os.makedirs(blobs)
snap = os.path.join(root, "models--Wan-AI--Wan2.2-TI2V-5B", "snapshots", "bbbb")
os.makedirs(snap)
for f in M.REQUIRED_FILES["ti2v-5B"]:
    open(os.path.join(blobs, "sha_" + f), "w").write("x")
    os.symlink(os.path.join("..", "..", "blobs", "sha_" + f), os.path.join(snap, f))
assert M.find_cached_snapshot("ti2v-5B", root) == snap

M.RUNPOD_MODEL_CACHE = root
M.MODEL_CACHE = tempfile.mkdtemp()
M.snapshot_download = lambda **kw: (_ for _ in ()).throw(AssertionError("must not download"))
assert M.ensure_model("ti2v-5B") == snap

M.RUNPOD_MODEL_CACHE = tempfile.mkdtemp()
calls = []


def fake_dl(repo_id, local_dir):
    calls.append(repo_id)
    for f in M.REQUIRED_FILES["ti2v-5B"]:
        open(os.path.join(local_dir, f), "w").write("x")


M.snapshot_download = fake_dl
assert M.ensure_model("ti2v-5B") == os.path.join(M.MODEL_CACHE, "ti2v-5B")
assert calls == ["Wan-AI/Wan2.2-TI2V-5B"]
M.ensure_model("ti2v-5B")
assert len(calls) == 1, "local copy must be reused"

M.MODEL_CACHE = tempfile.mkdtemp()
M.snapshot_download = lambda repo_id, local_dir: None
try:
    M.ensure_model("ti2v-5B")
    raise SystemExit("incomplete download must raise")
except RuntimeError as exc:
    assert "incomplete" in str(exc)

# ---- vace-14B: cached snapshot under models--Wan-AI--Wan2.1-VACE-14B, index.json required
root = tempfile.mkdtemp()
snap = os.path.join(root, "models--Wan-AI--Wan2.1-VACE-14B", "snapshots", "abc123")
os.makedirs(snap)
for f in ("models_t5_umt5-xxl-enc-bf16.pth", "Wan2.1_VAE.pth"):
    open(os.path.join(snap, f), "w").write("x")
assert M.find_cached_snapshot("vace-14B", root) is None, "no DiT shards index -> not a usable snapshot"
open(os.path.join(snap, "diffusion_pytorch_model.safetensors.index.json"), "w").write("{}")
assert M.find_cached_snapshot("vace-14B", root) == snap
assert M.repo_for("vace-14B") == "Wan-AI/Wan2.1-VACE-14B"
assert M.weights_status("vace-14B")["repo"] == "Wan-AI/Wan2.1-VACE-14B"

print("MODELS CHECKS PASSED")
