FROM python:3.11-slim@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377

WORKDIR /app

RUN apt-get update && apt-get install -y tmux curl && rm -rf /var/lib/apt/lists/*

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Install Python dependencies
RUN pip install --no-cache-dir pandas

# Create data directory
RUN mkdir -p /data

# Copy pre-seeded files
COPY device_logs.csv /data/device_logs.csv
COPY process_logs.py /app/process_logs.py

# Set broad permissions so the agent can read, write, and modify freely
RUN chmod -R 777 /data /app
