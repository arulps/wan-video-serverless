ARG PYTORCH_IMAGE=pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime
FROM ${PYTORCH_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive
ENV HF_HOME=/models
ENV HF_HUB_ENABLE_HF_TRANSFER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/opt/wan

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        ffmpeg \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app /opt/wan /models /tmp/wan-input /tmp/wan-output

WORKDIR /opt/wan
# Which Wan codebase this image carries. Both install as the `wan` package:
#   Wan2.2 (default) -> tasks t2v-A14B / i2v-A14B / ti2v-5B   (image tag :latest)
#   Wan2.1           -> task vace-14B, reference-to-video     (image tag :vace)
# app/generator.py builds its task table from whatever `wan` exposes, so one
# handler serves both images; WAN_REPO is also exported so the selftest can say
# which one is running.
ARG WAN_REPO=Wan2.2
ARG WAN_GIT_REF=main
ENV WAN_REPO=${WAN_REPO}
RUN git clone --depth 1 --branch ${WAN_GIT_REF} https://github.com/Wan-Video/${WAN_REPO}.git /opt/wan && \
    grep -v -E '(^|[,; ])(flash_attn|gradio)([,; =<>]|$)' /opt/wan/requirements.txt > /tmp/wan-req.txt && \
    pip install --no-cache-dir -r /tmp/wan-req.txt && \
    python - <<'EOF'
import os, pathlib
p = pathlib.Path("/opt/wan/wan/__init__.py")
if os.environ.get("WAN_REPO", "Wan2.2") == "Wan2.2":
    # Trim Wan2.2's package init to the three pipelines we ship (the others pull
    # in speech/animate dependencies that are not installed here).
    p.write_text(
        "# Copyright 2024-2025 The Alibaba Wan Team Authors. All rights reserved.\n"
        "from . import configs, distributed, modules\n"
        "from .image2video import WanI2V\n"
        "from .text2video import WanT2V\n"
        "from .textimage2video import WanTI2V\n"
    )
    print("patched", p)
else:
    # Wan2.1's init (configs, distributed, modules, FLF2V, I2V, T2V, VACE) is used as is.
    print("kept", p, p.read_text())
EOF

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app
COPY handler.py /app/handler.py

RUN python -c "import einops, safetensors, runpod, huggingface_hub, hf_transfer, boto3, cv2, imageio, torchvision, torchaudio, diffusers, transformers, tokenizers, accelerate, easydict, ftfy, tqdm, numpy; print('deps OK')"

ARG BAKE_TI2V=0
RUN if [ "$BAKE_TI2V" = "1" ]; then \
      python -c "from huggingface_hub import snapshot_download; snapshot_download('Wan-AI/Wan2.2-TI2V-5B', local_dir='/models/ti2v-5B')"; \
    fi

# Wan2.2's VAE decode grows its output with torch.cat per latent frame and needs
# ~2.6 GiB contiguous blocks at 1280x704; without expandable segments the
# caching allocator fragments and OOMs on a 24 GB card with >4 GiB reserved
# but unallocated (job caf3f7b9, 2026-09-21). Kept last so it does not
# invalidate the build layers above.
ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

CMD ["python", "-u", "/app/handler.py"]