FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962
WORKDIR /app

RUN apt-get update && apt-get install -y tmux curl && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY score_tracker.py /app/score_tracker.py
COPY quiz_runner.py /app/quiz_runner.py
COPY report_gen.py /app/report_gen.py
