FROM python:3.11-slim@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377

RUN apt-get update && apt-get install -y --no-install-recommends \
        bash curl tmux \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

RUN pip install --no-cache-dir \
        torch==2.2.2+cpu \
        --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir pytest

WORKDIR /app

COPY app/ /app/

RUN chmod +x /app/run_benchmarks.sh
