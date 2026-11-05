FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962
WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    curl \
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

RUN pip install --no-cache-dir \
    plotnine \
    matplotlib \
    pandas \
    pyarrow

COPY visualize.py /workspace/visualize.py
