FROM rockylinux:9@sha256:d7be1c094cc5845ee815d4632fe377514ee6ebcf8efaed6892889657e5ddaaa6

WORKDIR /app

RUN dnf install -y --allowerasing curl tmux && dnf clean all

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY requirements.txt /app/requirements.txt

RUN rm -f /etc/yum.repos.d/*.repo

COPY dnf.conf /etc/dnf/dnf.conf
COPY baseos.repo /etc/yum.repos.d/baseos.repo
COPY appstream.repo /etc/yum.repos.d/appstream.repo
COPY extras.repo /etc/yum.repos.d/extras.repo

RUN rm -rf /var/cache/dnf/*
