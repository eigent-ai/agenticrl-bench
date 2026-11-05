FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

RUN apt-get update && apt-get install -y tmux && rm -rf /var/lib/apt/lists/*
RUN pip install uv

WORKDIR /app
RUN mkdir -p /app/data

COPY generate_data.py /tmp/generate_data.py
RUN python3 /tmp/generate_data.py

COPY import_data.py /app/import_data.py
