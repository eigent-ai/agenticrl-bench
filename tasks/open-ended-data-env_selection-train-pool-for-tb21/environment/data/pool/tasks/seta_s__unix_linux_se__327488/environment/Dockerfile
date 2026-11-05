FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
RUN apt-get update && apt-get install -y python3 bash coreutils tmux curl && \
    rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh && \
    ln -sf /root/.local/bin/uv /usr/local/bin/uv
COPY deploy_konsole.sh /root/deploy_konsole.sh
RUN chmod +x /root/deploy_konsole.sh && /root/deploy_konsole.sh
WORKDIR /root
