FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-yaml \
    curl \
    tmux \
    procps \
    iproute2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/registry /etc/registry /var/lib/registry

COPY server.py /opt/registry/server.py
COPY entrypoint.sh /opt/registry/entrypoint.sh
COPY config.yml /etc/registry/config.yml

RUN chmod +x /opt/registry/entrypoint.sh
