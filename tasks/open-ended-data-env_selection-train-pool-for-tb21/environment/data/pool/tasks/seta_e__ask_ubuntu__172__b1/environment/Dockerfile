FROM rockylinux:9@sha256:d7be1c094cc5845ee815d4632fe377514ee6ebcf8efaed6892889657e5ddaaa6

WORKDIR /app

RUN dnf makecache -q && dnf install -y tmux

COPY requirements.txt /app/requirements.txt

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
