FROM debian:bookworm@sha256:854dd8ab51d62866dbd8f5431d15ce77b12983a2a4a1e1fe43a2395dc7ef9f61

RUN apt-get update && apt-get install -y \
    gcc \
    make \
    libc6-dev \
    tmux \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /root/project

COPY project/ /root/project/

RUN chmod -R 755 /root/project
