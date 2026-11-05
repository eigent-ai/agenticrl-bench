FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    jq \
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN pip3 install --break-system-packages \
    requests==2.31.0 \
    flask==2.3.0

COPY requirements.txt /app/requirements.txt
