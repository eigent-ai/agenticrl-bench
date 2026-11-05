FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    tmux curl python3 python3-pip ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/archives /opt/diagnostics

# v2 - force layer cache invalidation for COPY steps below
ARG CACHE_BUST=2

COPY sysping /tmp/sysping-build/sysping-1.0/bin/sysping
RUN chmod +x /tmp/sysping-build/sysping-1.0/bin/sysping && \
    tar czf /opt/archives/sysping-1.0.tar.gz -C /tmp/sysping-build sysping-1.0 && \
    rm -rf /tmp/sysping-build

COPY health_check.sh /opt/diagnostics/health_check.sh
RUN chmod +x /opt/diagnostics/health_check.sh

WORKDIR /root
