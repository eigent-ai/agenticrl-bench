FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    xvfb x11-utils x11-xserver-utils xdotool xterm \
    imagemagick \
    dbus dbus-x11 \
    xauth \
    procps psmisc \
    build-essential git curl tmux \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN useradd -m -s /bin/bash render && \
    chown root:root /home/render

RUN mkdir -p /opt/render-pipeline/output && \
    chown root:root /opt/render-pipeline/output

COPY env.conf /opt/render-pipeline/env.conf
COPY render.sh /opt/render-pipeline/render.sh
COPY start-display.sh /opt/render-pipeline/start-display.sh
RUN chmod +x /opt/render-pipeline/render.sh /opt/render-pipeline/start-display.sh

WORKDIR /opt/render-pipeline
