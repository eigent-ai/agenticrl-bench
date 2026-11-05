FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    python3 \
    python3-pip \
    build-essential \
    git \
    curl \
    tmux \
    grep \
    gawk \
    sed \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/lxc-desktop/xorg.conf.d

COPY deploy.sh /opt/lxc-desktop/deploy.sh
COPY container.conf /opt/lxc-desktop/container.conf
COPY setup-devices.sh /opt/lxc-desktop/setup-devices.sh
COPY start-desktop.sh /opt/lxc-desktop/start-desktop.sh
COPY 10-input.conf /opt/lxc-desktop/xorg.conf.d/10-input.conf
COPY 20-display.conf /opt/lxc-desktop/xorg.conf.d/20-display.conf
COPY README /opt/lxc-desktop/README

RUN chmod +x /opt/lxc-desktop/deploy.sh \
    /opt/lxc-desktop/setup-devices.sh \
    /opt/lxc-desktop/start-desktop.sh

WORKDIR /opt/lxc-desktop
