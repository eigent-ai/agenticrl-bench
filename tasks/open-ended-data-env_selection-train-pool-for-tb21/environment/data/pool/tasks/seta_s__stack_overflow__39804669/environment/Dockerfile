FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

RUN apt-get update && apt-get install -y tmux curl && \
    curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY generate_report.py /app/generate_report.py
COPY config.json /app/config.json

RUN chmod +x /app/generate_report.py
