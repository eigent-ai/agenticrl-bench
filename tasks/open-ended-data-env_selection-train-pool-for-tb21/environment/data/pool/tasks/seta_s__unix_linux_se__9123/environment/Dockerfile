FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    tmux \
    curl \
    coreutils \
    python3-minimal \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.local/bin:/root/.cargo/bin:$PATH"

RUN mkdir -p /root/bin /root/projects

COPY new_project.sh /root/bin/new_project.sh
RUN chmod +x /root/bin/new_project.sh

# Replace the default Ubuntu .bashrc with a minimal version that works in
# both interactive and non-interactive mode (Ubuntu's default has an early
# return for non-interactive shells that would prevent function loading).
COPY bashrc /root/.bashrc
