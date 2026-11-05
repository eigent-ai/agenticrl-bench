FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv && \
    ln -s /root/.local/bin/uvx /usr/local/bin/uvx
ENV PATH="/root/.local/bin:${PATH}"

RUN chown -R root:root /var/cache/apt/archives/ && \
    chmod -R 755 /var/cache/apt/archives/ && \
    chown -R root:root /var/lib/apt/lists/partial/ && \
    chmod -R 755 /var/lib/apt/lists/partial/
