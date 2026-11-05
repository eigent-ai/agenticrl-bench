FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential git curl tmux \
    xvfb x11-xkb-utils x11-xserver-utils x11-utils \
    python3 python3-pip sudo \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN useradd -m -s /bin/bash devuser

COPY keyboard-setup /usr/local/bin/keyboard-setup
RUN chmod +x /usr/local/bin/keyboard-setup

COPY Xmodmap /home/devuser/.Xmodmap
RUN chown devuser:devuser /home/devuser/.Xmodmap

WORKDIR /root
