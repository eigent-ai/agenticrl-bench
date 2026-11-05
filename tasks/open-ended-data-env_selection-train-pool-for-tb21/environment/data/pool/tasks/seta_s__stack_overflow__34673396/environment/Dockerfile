FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962
WORKDIR /opt/mltrack

RUN apt-get update && apt-get install -y tmux curl && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY run_pipeline.py /opt/mltrack/run_pipeline.py
COPY pipeline/ /opt/mltrack/pipeline/
COPY data/ /opt/mltrack/data/
COPY generate_data.py /opt/mltrack/generate_data.py
RUN python3 /opt/mltrack/generate_data.py && rm /opt/mltrack/generate_data.py
RUN mkdir -p /opt/mltrack/output
