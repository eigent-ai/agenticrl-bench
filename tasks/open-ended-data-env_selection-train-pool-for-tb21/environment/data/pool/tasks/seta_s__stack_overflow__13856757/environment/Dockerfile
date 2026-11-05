FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        tmux \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

WORKDIR /app

RUN /root/.local/bin/uv pip install --system flask requests pillow

RUN ffmpeg -y \
    -f lavfi -i testsrc=duration=5:size=320x240:rate=24 \
    -c:v libx264 -pix_fmt yuv420p \
    /app/sample.mp4

RUN mkdir -p /app/output

COPY process.py serve.py client.py /app/
