FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /opt/configmgr
RUN apt-get update && apt-get install -y \
    coreutils grep gawk sed \
    python3 python3-pip python3-venv \
    tmux curl \
    && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
COPY configmgr/ /opt/configmgr/
RUN chmod +x /opt/configmgr/validate_indices.sh
