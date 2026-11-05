FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /opt/platform

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    jq \
    tmux \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY registry.json /opt/platform/registry.json
COPY setup_platform.sh /tmp/setup_platform.sh
RUN chmod +x /tmp/setup_platform.sh && /tmp/setup_platform.sh && rm /tmp/setup_platform.sh
