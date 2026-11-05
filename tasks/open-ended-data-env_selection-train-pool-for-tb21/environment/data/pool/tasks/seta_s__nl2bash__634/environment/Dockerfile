FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app
RUN apt-get update && apt-get install -y \
    coreutils \
    findutils \
    bash \
    python3 \
    tmux \
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
COPY setup.sh /tmp/setup.sh
RUN chmod +x /tmp/setup.sh && /tmp/setup.sh && rm /tmp/setup.sh
COPY docs-ownership.conf /etc/docs-ownership.conf
COPY protected /srv/docs/.protected
