FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    tmux \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN /root/.local/bin/uv venv /app/.venv && \
    /root/.local/bin/uv pip install --python /app/.venv flask==3.1.0

COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
