"""app.generator against a fake Wan2.1-shaped `wan` package (mirrors upstream
wan/vace.py + wan/configs as read on 2026-09-21): task table built from what the
package exposes, VaceWanModel.from_pretrained forced to bf16, references
flattened onto white, prepare_source/generate called the way generate.py's vace
branch calls them, and the input guards. No GPU, no network."""
import os
import sys
import tempfile
import textwrap
import types

import torch
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

tmp = tempfile.mkdtemp()
pkg = os.path.join(tmp, "wan")
for d in ("modules", "configs", "utils", "distributed"):
    os.makedirs(os.path.join(pkg, d))

CALLS = {}
files = {
    "__init__.py": "from . import configs, distributed, modules\nfrom .text2video import WanT2V\nfrom .vace import WanVace\n",
    "distributed/__init__.py": "",
    "configs/__init__.py": textwrap.dedent('''
        import torch
        class EasyDict(dict):  # real easydict raises AttributeError for missing keys
            def __getattr__(self, k):
                try:
                    return self[k]
                except KeyError:
                    raise AttributeError(k)
        t2v_14B = EasyDict(param_dtype=torch.bfloat16, sample_fps=16, sample_neg_prompt="NEG-DEFAULT")
        WAN_CONFIGS = {"t2v-14B": t2v_14B, "vace-14B": t2v_14B}
        SIZE_CONFIGS = {"1280*720": (1280, 720), "720*1280": (720, 1280), "832*480": (832, 480)}
        MAX_AREA_CONFIGS = {"1280*720": 1280 * 720}
        SUPPORTED_SIZES = {"t2v-14B": ("1280*720",), "vace-14B": ("720*1280", "1280*720", "832*480")}
    '''),
    "utils/__init__.py": "",
    "utils/utils.py": textwrap.dedent('''
        import imageio, torch
        def cache_video(tensor, save_file=None, fps=30, suffix=".mp4", nrow=8, normalize=True, value_range=(-1, 1), retry=5):
            # (C, N, H, W) in [-1, 1] -> frames; torchvision-free stand-in for upstream
            t = ((tensor[0].clamp(-1, 1) + 1) / 2 * 255).type(torch.uint8).permute(1, 2, 3, 0).cpu()
            w = imageio.get_writer(save_file, fps=fps, codec="libx264", quality=8)
            for f in t.numpy():
                w.append_data(f)
            w.close()
            return save_file
    '''),
    "modules/__init__.py": "from .attention import flash_attention\nfrom .model import WanModel\nfrom .vace_model import VaceWanModel\n",
    "modules/attention.py": "import torch\nFLASH_ATTN_2_AVAILABLE=False\nFLASH_ATTN_3_AVAILABLE=False\ndef flash_attention(*a, **k):\n    raise AssertionError('flash')\ndef attention(*a, **k):\n    return flash_attention(*a, **k)\n",
    "modules/model.py": "from .attention import flash_attention\nclass WanModel: pass\n",
    "modules/vace_model.py": textwrap.dedent('''
        import torch
        from .model import WanModel
        class VaceWanModel(WanModel):
            LOAD_KW = []
            def __init__(self, dtype):
                self._p = torch.nn.Parameter(torch.zeros(2, dtype=dtype))
            def parameters(self):
                return iter([self._p])
            @classmethod
            def from_pretrained(cls, ckpt, *a, **kw):
                cls.LOAD_KW.append(dict(kw))
                return cls(kw.get("torch_dtype", torch.float32))
            def eval(self): return self
            def requires_grad_(self, *_): return self
            def to(self, *_): return self
    '''),
    "text2video.py": "class WanT2V:\n    def __init__(self, config, checkpoint_dir, device_id=0, rank=0, t5_fsdp=False, dit_fsdp=False, use_usp=False, t5_cpu=False):\n        pass\n",
    "vace.py": textwrap.dedent('''
        import torch
        from PIL import Image
        from .modules.vace_model import VaceWanModel
        from .text2video import WanT2V
        CALLS = {}
        class _VAE:
            def decode(self, zs):
                return zs
        class WanVace(WanT2V):
            def __init__(self, config, checkpoint_dir, device_id=0, rank=0, t5_fsdp=False, dit_fsdp=False, use_usp=False, t5_cpu=False):
                self.device = torch.device("cpu")
                self.config = config
                self.t5_cpu = t5_cpu
                self.model = VaceWanModel.from_pretrained(checkpoint_dir)
                self.model.eval().requires_grad_(False)
                self.model.to(self.device)
                self.vae = _VAE()
                self.sample_neg_prompt = config.sample_neg_prompt
            def prepare_source(self, src_video, src_mask, src_ref_images, num_frames, image_size, device):
                CALLS["prepare_source"] = dict(src_video=list(src_video), src_mask=list(src_mask),
                                               refs=[list(r) if r else r for r in src_ref_images],
                                               num_frames=num_frames, image_size=tuple(image_size))
                # mirror upstream: refs are opened with convert("RGB")
                out = []
                for refs in src_ref_images:
                    out.append([Image.open(p).convert("RGB") for p in refs] if refs else None)
                return src_video, src_mask, out
            def generate(self, input_prompt, input_frames, input_masks, input_ref_images, size=(1280, 720),
                         frame_num=81, context_scale=1.0, shift=5.0, sample_solver="unipc", sampling_steps=50,
                         guide_scale=5.0, n_prompt="", seed=-1, offload_model=True):
                CALLS["generate"] = dict(prompt=input_prompt, refs=input_ref_images, size=size, frame_num=frame_num,
                                         context_scale=context_scale, shift=shift, solver=sample_solver,
                                         steps=sampling_steps, guide_scale=guide_scale, n_prompt=n_prompt,
                                         seed=seed, offload=offload_model)
                # tiny video tensor (C, N, H, W) in [-1, 1]
                return torch.zeros(3, frame_num, 16, 32) - 1
    '''),
}
for rel, body in files.items():
    with open(os.path.join(pkg, rel), "w") as f:
        f.write(body)
sys.path.insert(0, tmp)
os.environ["WAN_REPO"] = "Wan2.1"

# runpod stub not needed: generator does not import runpod
import app.boot as boot  # noqa: E402

boot.apply_cuda_shim()
assert boot.SHIM_REPORT["model_binding_patched"], boot.SHIM_REPORT

import app.models as models  # noqa: E402
from app import generator as G  # noqa: E402

# ---- 1. task table reflects the codebase in the image ------------------------
assert set(G._PIPE_CLASSES) == {"vace-14B"}, G._PIPE_CLASSES  # t2v-A14B etc. absent in Wan2.1 configs
assert G.WAN_REPO == "Wan2.1"
assert G.supported_sizes("vace-14B") == ("720*1280", "1280*720", "832*480")

# fake checkpoint dir satisfying models.REQUIRED_FILES
ckpt = tempfile.mkdtemp()
for f in models.REQUIRED_FILES["vace-14B"]:
    open(os.path.join(ckpt, f), "w").close()
models.ensure_model = lambda task: ckpt

# ---- 2. reference flattening: transparent PNG -> white, RGB untouched -------
refdir = tempfile.mkdtemp()
rgba = os.path.join(refdir, "front.png")
Image.new("RGBA", (10, 10), (0, 0, 0, 0)).save(rgba)          # fully transparent
rgb = os.path.join(refdir, "lawn.jpg")
Image.new("RGB", (10, 10), (10, 200, 10)).save(rgb)
flat = G._flatten_reference(rgba)
assert flat.endswith("-flat.png") and Image.open(flat).convert("RGB").getpixel((5, 5)) == (255, 255, 255)
assert Image.open(rgba).convert("RGB").getpixel((5, 5)) == (0, 0, 0), "control: plain convert would give black"
assert G._flatten_reference(rgb) == rgb

# ---- 3. full vace call: bf16 load, prepare_source + generate wiring --------
import wan.vace as WV  # noqa: E402
from wan.modules.vace_model import VaceWanModel  # noqa: E402

out, info = G.generate(task="vace-14B", prompt="Mintu at the window", size="1280*720", frame_num=81,
                       steps=None, shift=None, guide_scale=None, n_prompt="", seed=7, offload=True,
                       solver="unipc", ref_image_paths=[rgba, rgb], context_scale=0.9)
assert VaceWanModel.LOAD_KW and VaceWanModel.LOAD_KW[-1].get("torch_dtype") == torch.bfloat16, VaceWanModel.LOAD_KW
assert info["dit_dtype"] == str(torch.bfloat16), info
ps = WV.CALLS["prepare_source"]
assert ps["src_video"] == [None] and ps["src_mask"] == [None] and ps["num_frames"] == 81
assert ps["image_size"] == (1280, 720), "prepare_source takes (w, h) like generate.py's SIZE_CONFIGS"
assert len(ps["refs"]) == 1 and len(ps["refs"][0]) == 2 and ps["refs"][0][0].endswith("-flat.png") and ps["refs"][0][1] == rgb
g = WV.CALLS["generate"]
assert g["prompt"] == "Mintu at the window" and len(g["refs"][0]) == 2
assert g["size"] == (1280, 720) and g["frame_num"] == 81 and g["context_scale"] == 0.9
assert g["steps"] == 50, "vace default steps = 50 (upstream generate.py)"
assert g["shift"] == 5.0 and g["guide_scale"] == 5.0 and g["n_prompt"] == "" and g["seed"] == 7 and g["offload"] is True
assert info["fps"] == 16 and info["duration_s"] == round(81 / 16, 3) and info["ref_images"] == 2
assert info["wan_repo"] == "Wan2.1" and info["steps"] == 50
assert os.path.isfile(out) and os.path.getsize(out) > 0
os.remove(out)
# second call reuses the loaded pipeline (no second from_pretrained)
n_loads = len(VaceWanModel.LOAD_KW)
out2, _ = G.generate(task="vace-14B", prompt="again", size="1280*720", ref_image_paths=[rgb], steps=8)
os.remove(out2)  # /tmp/wan-output is shared with test_handler.py, which asserts it is empty
assert len(VaceWanModel.LOAD_KW) == n_loads and WV.CALLS["generate"]["steps"] == 8

# ---- 4. guards --------------------------------------------------------------
def must_fail(msg, **kw):
    try:
        G.generate(**kw)
    except ValueError as exc:
        assert msg in str(exc), (msg, str(exc))
        return
    raise AssertionError("expected ValueError: " + msg)


must_fail("at least one reference image", task="vace-14B", prompt="x", size="1280*720")
must_fail("not 'image'", task="vace-14B", prompt="x", size="1280*720", image_path=rgb, ref_image_paths=[rgb])
must_fail("not available in this image", task="ti2v-5B", prompt="x", size="1280*704", image_path=rgb)
must_fail("unknown size", task="vace-14B", prompt="x", size="1280*704", ref_image_paths=[rgb])
must_fail("4n+1", task="vace-14B", prompt="x", size="1280*720", frame_num=80, ref_image_paths=[rgb])

print("GENERATOR VACE CHECKS PASSED")
