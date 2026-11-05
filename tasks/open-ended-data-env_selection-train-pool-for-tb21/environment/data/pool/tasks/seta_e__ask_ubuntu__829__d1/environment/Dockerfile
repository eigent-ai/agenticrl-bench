FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gnupg \
    curl \
    wget \
    ca-certificates \
    lsb-release \
    python3 \
    tmux \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /home/user
COPY service_requirements.txt /home/user/service_requirements.txt

WORKDIR /app
