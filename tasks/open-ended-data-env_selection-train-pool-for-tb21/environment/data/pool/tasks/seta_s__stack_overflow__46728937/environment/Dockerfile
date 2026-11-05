FROM python:3.11-slim@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377

RUN apt-get update && apt-get install -y tmux curl && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

WORKDIR /app

COPY requirements.txt .
RUN pip install uv && uv pip install --system -r requirements.txt

COPY setup.py .
RUN python setup.py

COPY extract_activations.py .
