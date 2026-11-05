FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux zip unzip && rm -rf /var/lib/apt/lists/*

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Create config directory structure and files
COPY setup_configs.sh /tmp/setup_configs.sh
RUN chmod +x /tmp/setup_configs.sh && /tmp/setup_configs.sh && rm /tmp/setup_configs.sh

WORKDIR /app
