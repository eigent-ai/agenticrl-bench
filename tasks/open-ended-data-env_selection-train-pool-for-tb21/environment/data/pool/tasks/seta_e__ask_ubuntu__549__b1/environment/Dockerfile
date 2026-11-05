FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y sudo build-essential git curl tmux

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN useradd -m -s /bin/bash developer && \
    echo "developer:password" | chpasswd && \
    mkdir -p /opt/developer/bin

COPY cshrc_distractor /home/developer/.cshrc

RUN chown -R developer:developer /home/developer
