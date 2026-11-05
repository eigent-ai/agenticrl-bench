FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    xvfb \
    mesa-utils \
    x11-utils \
    python3 \
    tmux \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

RUN mkdir -p /opt/ci_gl
COPY ci_gl/ /opt/ci_gl/
RUN chmod +x /opt/ci_gl/*.sh

WORKDIR /app
