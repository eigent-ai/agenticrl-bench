FROM node:20-slim@sha256:2cf067cfed83d5ea958367df9f966191a942351a2df77d6f0193e162b5febfc0

RUN apt-get update && apt-get install -y tmux curl && \
    curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/texthub

COPY package.json ./
RUN npm install

COPY server.js ./
COPY static/ ./static/
COPY data/ ./data/
COPY extras/ ./extras/
COPY scripts/ ./scripts/

RUN ln -s ../extras/notes.txt ./data/notes.txt
RUN sed -i 's/$/\r/' ./data/changelog.txt ./data/report.txt
