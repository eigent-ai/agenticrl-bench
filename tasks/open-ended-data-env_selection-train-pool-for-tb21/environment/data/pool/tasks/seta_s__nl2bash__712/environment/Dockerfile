FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y \
    diffutils \
    coreutils \
    findutils \
    gawk \
    python3 \
    jq \
    tmux \
    file \
    patch \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY setup_env.py /tmp/setup_env.py
RUN python3 /tmp/setup_env.py && rm /tmp/setup_env.py

COPY config.ini /srv/audit/config.ini
