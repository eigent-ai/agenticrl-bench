FROM debian:bookworm@sha256:854dd8ab51d62866dbd8f5431d15ce77b12983a2a4a1e1fe43a2395dc7ef9f61

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-minimal \
    tmux \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

RUN mkdir -p /opt/config

COPY environments.conf /opt/config/environments.conf
COPY extract_config.py /opt/config/extract_config.py
RUN chmod +x /opt/config/extract_config.py

WORKDIR /opt/config
