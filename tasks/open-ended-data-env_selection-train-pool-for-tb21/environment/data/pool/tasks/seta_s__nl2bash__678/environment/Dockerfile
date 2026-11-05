FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /opt/webapp
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    sqlite3 \
    tmux \
    curl \
    file \
    && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
COPY setup_env.sh /tmp/setup_env.sh
RUN bash /tmp/setup_env.sh && rm /tmp/setup_env.sh
