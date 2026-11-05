FROM python:3.11-slim@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    matplotlib==3.9.2 \
    numpy==1.26.4 \
    pandas==2.2.2 \
    pyyaml==6.0.2 \
    pytest==8.3.3

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY app/ /app/

RUN mkdir -p /app/output
