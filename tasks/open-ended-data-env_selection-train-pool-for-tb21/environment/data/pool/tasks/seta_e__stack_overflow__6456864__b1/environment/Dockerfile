FROM python:3.12-slim@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704
RUN apt-get update && apt-get install -y tmux curl && \
    curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY app/ /app/
RUN mkdir -p /app/output
