FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    procps \
    curl \
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

WORKDIR /app

COPY swap-report.sh /usr/local/bin/swap-report.sh
RUN chmod +x /usr/local/bin/swap-report.sh

COPY swap-report.conf /etc/swap-report.conf

COPY 99-memory.conf /etc/sysctl.d/99-memory.conf
