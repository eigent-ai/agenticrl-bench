FROM python:3.11-slim@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN pip install --no-cache-dir \
    pandas==2.1.4 \
    numpy==1.26.2 \
    scikit-learn==1.3.2 \
    lightgbm==4.2.0 \
    statsmodels==0.14.1 \
    matplotlib==3.8.2

COPY datasets/ /data/datasets/

RUN mkdir -p /data/results
