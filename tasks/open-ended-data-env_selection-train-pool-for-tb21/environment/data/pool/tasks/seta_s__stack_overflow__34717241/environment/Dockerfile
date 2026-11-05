FROM python:3.11-slim@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377
WORKDIR /app
RUN apt-get update && apt-get install -y tmux curl && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
RUN . $HOME/.local/bin/env && uv pip install --system pandas
COPY app/run_experiment.py /app/run_experiment.py
COPY app/pipeline/ /app/pipeline/
COPY app/configs/ /app/configs/
COPY app/data/ /app/data/
COPY app/scripts/ /app/scripts/
