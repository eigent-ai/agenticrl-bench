FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y \
    sudo \
    procps \
    coreutils \
    util-linux \
    build-essential \
    git \
    curl \
    tmux \
    python3 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN groupadd monitors && \
    useradd -m -s /bin/bash appuser && \
    useradd -r -m -s /bin/bash sandbox && \
    useradd -m -s /bin/bash -G monitors monitor

RUN mkdir -p /opt/sandbox/output && \
    mkdir -p "/opt/sandbox/build output"

COPY subuid /etc/subuid
COPY subgid /etc/subgid
COPY monitors_sudoers /etc/sudoers.d/monitors
RUN chmod 0440 /etc/sudoers.d/monitors

COPY 99-userns.conf /etc/sysctl.d/99-userns.conf

COPY manage.sh /opt/sandbox/manage.sh
COPY config.env /opt/sandbox/config.env
COPY demo.sh /opt/sandbox/demo.sh

RUN chmod +x /opt/sandbox/manage.sh /opt/sandbox/demo.sh && \
    chown -R appuser:appuser /opt/sandbox && \
    chmod 777 /opt/sandbox/output && \
    chmod 777 "/opt/sandbox/build output"
