FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

# Install system packages. Do NOT clean apt lists — apt-cache policy needs them.
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    openssh-client \
    less \
    ca-certificates \
    python3 \
    python3-pip \
    aptitude \
    tmux

# Install uv for test runner
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Pre-warm aptitude package cache so first search does not stall
RUN aptitude show curl > /dev/null 2>&1 || true

# Plant the audit tool files
RUN mkdir -p /opt/audit
COPY packages.txt /opt/audit/packages.txt
COPY README.md /opt/audit/README.md
COPY audit.py /opt/audit/audit.py
