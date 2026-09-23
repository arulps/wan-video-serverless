#!/usr/bin/env python3
"""Upscale a finished clip (OpenArt 720p, our 720p keepers, anything) to a
4K master, optionally raising the frame rate, and encode it properly.

    python scripts/upscale_video.py in.mp4 out-4k.mp4                 # 4K (3840x2160), same fps, h264 crf 16
    python scripts/upscale_video.py in.mp4 out.mp4 --fps 30            # + frame interpolation to 30 fps
    python scripts/upscale_video.py in.mp4 out.mp4 --height 1080       # 1080p instead of 4K
    python scripts/upscale_video.py in.mp4 out.mp4 --codec hevc        # HEVC master (smaller, YouTube-fine)
    python scripts/upscale_video.py in.mp4 out.mp4 --frames-dir F      # keep the PNG frames (for a further pass)

Pipeline: ffmpeg decode -> PNG frames -> Real-ESRGAN (realesr-animevideov3,
the model trained for animation video; x4 then a lanczos resize to the exact
target) -> optional RIFE (rife-ncnn-vulkan if on PATH) or ffmpeg minterpolate
-> libx264/libx265 crf 16 -> audio copied from the source untouched.

Self-contained: the network is defined here (SRVGGNetCompact, ~40 lines), so
there is no basicsr/realesrgan package dependency -- those break on current
torchvision. Needs: torch, numpy, Pillow, ffmpeg. GPU strongly recommended
(a 5 s 720p clip is ~120 frames; ~0.3 s/frame on an A100 at 4K, tens of
seconds per frame on a CPU). Weights (16 MB) are downloaded once into
~/.cache/wan-upscale/ from the Real-ESRGAN GitHub release.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

MODELS = {
    # name: (url, num_feat, num_conv, upscale)
    "animevideov3": ("https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth", 64, 16, 4),
}
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "wan-upscale")


def log(*a):
    print(time.strftime("[%H:%M:%S]"), *a, flush=True)


def run(cmd, **kw):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw)
    if r.returncode != 0:
        sys.exit("command failed: %s\n%s" % (" ".join(cmd), r.stdout.decode(errors="replace")[-3000:]))
    return r.stdout.decode(errors="replace")


def probe(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=width,height,r_frame_rate,nb_frames:format=duration", "-of", "json", path])
    j = json.loads(out)
    s = j["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    fps = float(num) / float(den)
    has_audio = "audio" in run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", path])
    return {"w": int(s["width"]), "h": int(s["height"]), "fps": fps,
            "frames": int(s.get("nb_frames") or 0), "dur": float(j["format"]["duration"]), "audio": has_audio}


# ---------------------------------------------------------------- network

def build_model(num_feat, num_conv, upscale):
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    class SRVGGNetCompact(nn.Module):
        """Real-ESRGAN's compact VGG-style SR net (used by realesr-animevideov3)."""
        def __init__(self, num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4):
            super().__init__()
            self.upscale = upscale
            self.body = nn.ModuleList()
            self.body.append(nn.Conv2d(num_in_ch, num_feat, 3, 1, 1))
            self.body.append(nn.PReLU(num_parameters=num_feat))
            for _ in range(num_conv):
                self.body.append(nn.Conv2d(num_feat, num_feat, 3, 1, 1))
                self.body.append(nn.PReLU(num_parameters=num_feat))
            self.body.append(nn.Conv2d(num_feat, num_out_ch * upscale * upscale, 3, 1, 1))
            self.upsampler = nn.PixelShuffle(upscale)

        def forward(self, x):
            out = x
            for m in self.body:
                out = m(out)
            out = self.upsampler(out)
            base = F.interpolate(x, scale_factor=self.upscale, mode="nearest")
            return out + base

    return SRVGGNetCompact(num_feat=num_feat, num_conv=num_conv, upscale=upscale)


def load_weights(name, path_override=None):
    import torch
    url, nf, nc, up = MODELS[name]
    path = path_override or os.path.join(CACHE, os.path.basename(url))
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        log("downloading weights", url)
        urllib.request.urlretrieve(url, path)
    sd = torch.load(path, map_location="cpu", weights_only=False)
    if "params" in sd:
        sd = sd["params"]
    model = build_model(nf, nc, up)
    model.load_state_dict(sd, strict=True)
    model.eval()
    return model, up


def upscale_frame(model, up, img, device, tile=512, pad=16):
    """img: HxWx3 uint8 -> (H*up)x(W*up)x3 uint8, tiled so 4K fits in VRAM."""
    import numpy as np
    import torch
    h, w, _ = img.shape
    x = torch.from_numpy(np.ascontiguousarray(img)).permute(2, 0, 1).float().div_(255.0).unsqueeze(0).to(device)
    out = torch.zeros((1, 3, h * up, w * up), device=device)
    with torch.no_grad():
        for y in range(0, h, tile):
            for x0 in range(0, w, tile):
                y0, y1 = max(0, y - pad), min(h, y + tile + pad)
                x1, x2 = max(0, x0 - pad), min(w, x0 + tile + pad)
                patch = model(x[:, :, y0:y1, x1:x2])
                oy, ox = (y - y0) * up, (x0 - x1) * up
                th, tw = min(tile, h - y) * up, min(tile, w - x0) * up
                out[:, :, y * up:y * up + th, x0 * up:x0 * up + tw] = patch[:, :, oy:oy + th, ox:ox + tw]
    out = out.clamp_(0, 1).mul_(255.0).round_().byte().squeeze(0).permute(1, 2, 0).cpu().numpy()
    return out


# ---------------------------------------------------------------- pipeline

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--height", type=int, default=2160, help="target height (2160 = 4K UHD, 1080)")
    ap.add_argument("--fps", type=float, default=None, help="target fps (frame interpolation); default = keep source fps")
    ap.add_argument("--codec", choices=["h264", "hevc"], default="h264")
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--model", default="animevideov3", choices=list(MODELS))
    ap.add_argument("--weights", default=None, help="local .pth instead of the cached download")
    ap.add_argument("--tile", type=int, default=512)
    ap.add_argument("--frames-dir", default=None, help="keep the upscaled PNG frames here")
    ap.add_argument("--device", default=None, help="cuda | cpu (default: cuda if available)")
    ap.add_argument("--limit", type=int, default=0, help="only the first N frames (smoke test)")
    a = ap.parse_args()

    import numpy as np
    import torch
    from PIL import Image

    device = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    info = probe(a.src)
    target_h = a.height
    target_w = round(info["w"] * target_h / info["h"] / 2) * 2
    log("source %dx%d @ %.3f fps, %.2f s, audio=%s -> target %dx%d @ %s fps on %s" %
        (info["w"], info["h"], info["fps"], info["dur"], info["audio"], target_w, target_h, a.fps or "%.3f" % info["fps"], device))

    model, up = load_weights(a.model, a.weights)
    model = model.to(device)
    if device == "cuda":
        model = model.half()

    work = tempfile.mkdtemp(prefix="upscale-")
    src_frames = os.path.join(work, "src"); os.makedirs(src_frames)
    out_frames = a.frames_dir or os.path.join(work, "up"); os.makedirs(out_frames, exist_ok=True)
    t0 = time.time()
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", a.src]
    if a.limit:
        cmd += ["-frames:v", str(a.limit)]
    run(cmd + [os.path.join(src_frames, "f%06d.png")])
    names = sorted(os.listdir(src_frames))
    log("decoded %d frames in %.1fs" % (len(names), time.time() - t0))

    t1 = time.time()
    for i, n in enumerate(names):
        img = np.asarray(Image.open(os.path.join(src_frames, n)).convert("RGB"))
        if device == "cuda":
            with torch.autocast("cuda", dtype=torch.float16):
                big = upscale_frame(model, up, img, device, a.tile)
        else:
            big = upscale_frame(model, up, img, device, a.tile)
        if big.shape[1] != target_w or big.shape[0] != target_h:
            big = np.asarray(Image.fromarray(big).resize((target_w, target_h), Image.LANCZOS))
        Image.fromarray(big).save(os.path.join(out_frames, n), compress_level=1)
        if i % 20 == 0 or i == len(names) - 1:
            el = time.time() - t1
            log("upscaled %d/%d (%.2fs/frame, eta %.0fs)" % (i + 1, len(names), el / (i + 1), el / (i + 1) * (len(names) - i - 1)))

    # frame interpolation
    fps_in = info["fps"]
    vf = []
    interp_note = "none"
    if a.fps and abs(a.fps - fps_in) > 1e-3:
        if shutil.which("rife-ncnn-vulkan") and abs(a.fps / fps_in - round(a.fps / fps_in)) < 1e-6 and int(round(a.fps / fps_in)) in (2, 4, 8):
            factor = int(round(a.fps / fps_in))
            rife_out = os.path.join(work, "rife"); os.makedirs(rife_out)
            log("RIFE x%d via rife-ncnn-vulkan" % factor)
            run(["rife-ncnn-vulkan", "-i", out_frames, "-o", rife_out, "-n", str(len(names) * factor), "-f", "f%06d.png"])
            out_frames = rife_out
            fps_in = a.fps
            interp_note = "rife-ncnn-vulkan x%d" % factor
        else:
            vf.append("minterpolate=fps=%g:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" % a.fps)
            interp_note = "ffmpeg minterpolate -> %g fps" % a.fps

    # encode: frames + original audio
    t2 = time.time()
    enc = ["ffmpeg", "-v", "error", "-y", "-framerate", "%.6f" % fps_in, "-i", os.path.join(out_frames, "f%06d.png")]
    if info["audio"] and not a.limit:
        enc += ["-i", a.src, "-map", "0:v", "-map", "1:a", "-c:a", "copy"]
    if vf:
        enc += ["-vf", ",".join(vf)]
    if a.codec == "h264":
        enc += ["-c:v", "libx264", "-preset", "slow", "-crf", str(a.crf), "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "5.1"]
    else:
        enc += ["-c:v", "libx265", "-preset", "slow", "-crf", str(a.crf), "-pix_fmt", "yuv420p", "-tag:v", "hvc1"]
    enc += ["-movflags", "+faststart", "-shortest", a.dst]
    run(enc)
    log("encoded in %.1fs" % (time.time() - t2))
    if not a.frames_dir:
        shutil.rmtree(work, ignore_errors=True)
    out = probe(a.dst)
    meta = {"src": a.src, "dst": a.dst, "source": info, "output": out, "model": a.model, "upscale_factor": up,
            "interpolation": interp_note, "codec": a.codec, "crf": a.crf, "device": device,
            "seconds": {"decode": round(t1 - t0, 1), "upscale": round(t2 - t1, 1), "encode": round(time.time() - t2, 1)}}
    json.dump(meta, open(a.dst + ".json", "w"), indent=1)
    log("DONE %s: %dx%d @ %.3f fps, %.2f s, %.1f MB" % (a.dst, out["w"], out["h"], out["fps"], out["dur"], os.path.getsize(a.dst) / 1e6))


if __name__ == "__main__":
    main()
