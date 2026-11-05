FROM node:20-slim@sha256:2cf067cfed83d5ea958367df9f966191a942351a2df77d6f0193e162b5febfc0

RUN apt-get update && apt-get install -y tmux python3 python3-pip python3-venv curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

WORKDIR /app

COPY package.json /app/package.json
RUN npm install

COPY config.json /app/config.json
COPY src/ /app/src/
COPY data/ /app/data/

WORKDIR /
