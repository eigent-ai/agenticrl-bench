FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Pre-populate bash history
COPY bash_history /root/.bash_history

# Add history settings to bashrc
COPY bashrc_additions /tmp/bashrc_additions
RUN cat /tmp/bashrc_additions >> /root/.bashrc && rm /tmp/bashrc_additions
