FROM alpine:3.21@sha256:ee16d92f96db08d9d2d07da48555a27f3a69d8f0759021dbc601195ed0d2b5bd
WORKDIR /opt/vm-io-manager

RUN apk add --no-cache bash python3 tmux procps curl coreutils grep gawk sed

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Copy the toolkit structure
COPY config/ /opt/vm-io-manager/config/
COPY data/ /opt/vm-io-manager/data/
COPY bin/ /opt/vm-io-manager/bin/

RUN chmod +x /opt/vm-io-manager/bin/*.sh

# Create empty output directory
RUN mkdir -p /opt/vm-io-manager/output
