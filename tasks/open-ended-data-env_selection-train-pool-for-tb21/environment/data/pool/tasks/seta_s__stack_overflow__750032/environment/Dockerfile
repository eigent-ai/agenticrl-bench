FROM node:20-bookworm-slim@sha256:2cf067cfed83d5ea958367df9f966191a942351a2df77d6f0193e162b5febfc0
WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip curl tmux && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY process_files.js /app/process_files.js
COPY package.json /app/package.json
COPY data/ /app/data/
