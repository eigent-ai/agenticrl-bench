FROM node:20-slim@sha256:2cf067cfed83d5ea958367df9f966191a942351a2df77d6f0193e162b5febfc0

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY package.json /app/package.json
RUN npm install

COPY events.json /app/events.json
COPY generate-schedule.js /app/generate-schedule.js
COPY README.md /app/README.md
