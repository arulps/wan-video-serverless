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
ARG WAN_GIT_REF=main
RUN git clone --depth 1 --branch ${WAN_GIT_REF} https://github.com/Wan-Video/Wan2.2.git /opt/wan && \
    grep -v -E '(^|[,; ])flash_attn([,; ]|$)' /opt/wan/requirements.txt > /tmp/wan-req.txt && \
    pip install --no-cache-dir -r /tmp/wan-req.txt

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app
COPY handler.py /app/handler.py

ARG BAKE_TI2V=0
RUN if [ "$BAKE_TI2V" = "1" ]; then \
      python -c "from huggingface_hub import snapshot_download; snapshot_download('Wan-AI/Wan2.2-TI2V-5B', local_dir='/models/ti2v-5B')"; \
    fi

CMD ["python", "-u", "/app/handler.py"]