FROM python:3.10-slim-bookworm@sha256:5be5aaecb962a41567bc8041f1e9e3432cb085b037fe057f9a562630b2e4b370

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN pip install --no-cache-dir \
    torch==2.2.2+cpu --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    pandas==2.2.1 \
    Pillow==10.2.0 \
    PyYAML==6.0.1

WORKDIR /app

COPY src/ /app/src/
COPY config.yaml /app/config.yaml
COPY run_pipeline.py /app/run_pipeline.py
COPY validate_output.py /app/validate_output.py
COPY generate_data.py /tmp/generate_data.py

RUN cd /app && python /tmp/generate_data.py && rm /tmp/generate_data.py
