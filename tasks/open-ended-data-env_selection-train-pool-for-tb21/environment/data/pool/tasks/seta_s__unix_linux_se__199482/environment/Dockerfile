FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /opt/memmon
RUN apt-get update && apt-get install -y python3 procps tmux curl && \
    rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
COPY memmon.py /opt/memmon/memmon.py
COPY config.json /opt/memmon/config.json
RUN chmod +x /opt/memmon/memmon.py
WORKDIR /app
