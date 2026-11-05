FROM rockylinux:9@sha256:d7be1c094cc5845ee815d4632fe377514ee6ebcf8efaed6892889657e5ddaaa6

RUN dnf install -y --allowerasing curl wget git vim-enhanced python3 tree jq tmux && \
    dnf remove -y nano || true && \
    dnf remove -y telnet-server || true && \
    dnf clean all

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN useradd -m user || true

COPY packages.txt /home/user/packages.txt

RUN chown user:user /home/user/packages.txt

WORKDIR /home/user
