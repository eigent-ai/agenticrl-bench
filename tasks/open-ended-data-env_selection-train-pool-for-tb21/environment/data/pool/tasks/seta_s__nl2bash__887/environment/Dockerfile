FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    tmux \
    python3 \
    python3-pip \
    python3-yaml \
    coreutils \
    findutils \
    && rm -rf /var/lib/apt/lists/*

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Set up artifact storage structure
RUN mkdir -p /opt/artifacts

COPY system.conf /opt/artifacts/system.conf
COPY audit.log /opt/artifacts/audit.log
COPY setup_artifacts.sh /tmp/setup_artifacts.sh

RUN chmod +x /tmp/setup_artifacts.sh && /tmp/setup_artifacts.sh && rm /tmp/setup_artifacts.sh

WORKDIR /opt/artifacts
