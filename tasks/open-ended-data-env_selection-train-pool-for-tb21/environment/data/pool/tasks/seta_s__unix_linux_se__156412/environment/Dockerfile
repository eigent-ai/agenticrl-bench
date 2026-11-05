FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get clean && rm -rf /var/lib/apt/lists/* && \
    apt-get update --allow-insecure-repositories && \
    apt-get install -y --no-install-recommends --allow-unauthenticated \
    ca-certificates \
    curl \
    tmux \
    python3 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /etc/vmon /etc/X11/xorg.conf.d

COPY monitors.conf /etc/vmon/monitors.conf
COPY vmon-helpers.sh /usr/local/bin/vmon-helpers.sh
COPY vmon-setup /usr/local/bin/vmon-setup
COPY cvt /usr/local/bin/cvt

RUN chmod +x /usr/local/bin/vmon-setup /usr/local/bin/vmon-helpers.sh /usr/local/bin/cvt
