FROM python:3.13@sha256:fa73a7f200473ac67c9d05b7d91b9b6f3b5b945e296406986b307d7f738e0b37
RUN apt-get update && apt-get install -y --no-install-recommends tmux curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir tzdata pytest
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
WORKDIR /app
COPY app/ /app/
