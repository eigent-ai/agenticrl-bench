FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

WORKDIR /opt/mlpipeline

RUN apt-get update && apt-get install -y --no-install-recommends \
    tmux \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN pip install --no-cache-dir pandas

COPY callbacks.py /opt/mlpipeline/callbacks.py
COPY trainer.py /opt/mlpipeline/trainer.py
COPY analyze_metrics.py /opt/mlpipeline/analyze_metrics.py
COPY config.py /opt/mlpipeline/config.py
COPY run_pipeline.py /opt/mlpipeline/run_pipeline.py

RUN mkdir -p /opt/mlpipeline/output
