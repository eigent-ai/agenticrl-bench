FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    php-cli \
    python3 \
    tmux \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

COPY opt/data-processor /opt/data-processor

RUN chmod -R 755 /opt/data-processor
