FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 tmux curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

RUN mkdir -p /opt/cpu_inventory

COPY collect.py /opt/cpu_inventory/collect.py
COPY README.md  /opt/cpu_inventory/README.md
RUN chmod 755 /opt/cpu_inventory/collect.py
