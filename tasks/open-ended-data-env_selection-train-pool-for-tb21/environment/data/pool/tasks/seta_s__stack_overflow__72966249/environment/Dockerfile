FROM node:20-slim@sha256:2cf067cfed83d5ea958367df9f966191a942351a2df77d6f0193e162b5febfc0
RUN apt-get update && apt-get install -y tmux curl && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
WORKDIR /app
COPY analyze.js /app/analyze.js
COPY package.json /app/package.json
COPY README.md /app/README.md
COPY lib/isometric.js /app/lib/isometric.js
COPY data/session.json /app/data/session.json
