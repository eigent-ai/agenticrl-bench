FROM ubuntu:22.04@sha256:0a9887931b0e38af2e3487ed39e29436b0535c4f3f52e57745baaf79d1898956

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    systemd netplan.io iproute2 net-tools \
    dnsutils isc-dhcp-client curl vim tmux \
    && rm -rf /var/lib/apt/lists/*

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Create directories
RUN mkdir -p /etc/netplan /run/systemd/resolve

# Create default netplan config
COPY 00-default.yaml /etc/netplan/00-default.yaml

# Create template netplan config with placeholders
COPY 01-dns-config.yaml /etc/netplan/01-dns-config.yaml

# Create placeholder stub-resolv.conf
COPY stub-resolv.conf /run/systemd/resolve/stub-resolv.conf

WORKDIR /app
