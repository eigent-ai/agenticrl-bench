FROM python:3.12-slim@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends tmux curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY requirements.txt /app/requirements.txt
RUN /root/.local/bin/uv pip install --system -r /app/requirements.txt

COPY generate_data.py /app/generate_data.py
COPY visualize.py /app/visualize.py

RUN python /app/generate_data.py
RUN python /app/visualize.py
