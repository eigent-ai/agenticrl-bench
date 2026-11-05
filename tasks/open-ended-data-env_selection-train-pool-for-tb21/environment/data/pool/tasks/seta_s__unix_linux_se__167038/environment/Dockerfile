FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

WORKDIR /opt/hwaudit

RUN apt-get update && apt-get install -y --no-install-recommends \
    tmux \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY config.ini /opt/hwaudit/config.ini
COPY run_inventory.sh /opt/hwaudit/run_inventory.sh
COPY inventory.py /opt/hwaudit/inventory.py
COPY data/ /opt/hwaudit/data/

RUN chmod +x /opt/hwaudit/run_inventory.sh
