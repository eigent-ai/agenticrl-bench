FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

WORKDIR /opt/dataproc

RUN apt-get update && apt-get install -y --no-install-recommends \
    tmux \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /var/log/dataproc /opt/dataproc/data /opt/dataproc/output

COPY config.ini /opt/dataproc/config.ini
COPY main.py /opt/dataproc/main.py
COPY debug_utils.py /opt/dataproc/debug_utils.py
COPY formatter.py /opt/dataproc/formatter.py
COPY data_loader.py /opt/dataproc/data_loader.py
COPY inventory.csv /opt/dataproc/data/inventory.csv
