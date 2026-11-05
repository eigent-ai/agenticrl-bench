FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    python3 \
    python3-yaml \
    jq \
    curl \
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /etc/docker /opt/stacks/webapp /usr/local/bin

COPY docker-preflight /usr/local/bin/docker-preflight
RUN chmod 0755 /usr/local/bin/docker-preflight

COPY daemon.json /etc/docker/daemon.json

COPY webapp-compose.yaml /opt/stacks/webapp/docker-compose.yaml
