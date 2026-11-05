FROM python:3.11-slim@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377

WORKDIR /opt/neural_pipeline

RUN apt-get update && apt-get install -y build-essential git curl tmux && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN pip install --no-cache-dir numpy scipy

COPY generate_data.py /opt/neural_pipeline/generate_data.py
COPY config.json /opt/neural_pipeline/config.json
COPY pipeline.py /opt/neural_pipeline/pipeline.py

RUN python3 generate_data.py
