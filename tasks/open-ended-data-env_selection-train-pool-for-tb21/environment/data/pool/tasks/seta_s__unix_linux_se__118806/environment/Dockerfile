FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential git curl tmux vim \
    ncurses-bin ncurses-base bash coreutils \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Place config files
COPY tmux.conf /root/.tmux.conf
COPY bashrc /root/.bashrc
COPY vimrc /root/.vimrc
COPY color-check.sh /usr/local/bin/color-check.sh
RUN chmod +x /usr/local/bin/color-check.sh

# Remove the screen-256color terminfo entry from all possible locations
RUN find / -path "*/terminfo/s/screen-256color*" -delete 2>/dev/null; \
    (apt-get update && apt-get remove -y ncurses-term && rm -rf /var/lib/apt/lists/*) 2>/dev/null; \
    true

WORKDIR /root
