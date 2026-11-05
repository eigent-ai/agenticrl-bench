FROM node:20-slim@sha256:2cf067cfed83d5ea958367df9f966191a942351a2df77d6f0193e162b5febfc0

WORKDIR /home/user/calutil

RUN apt-get update && apt-get install -y tmux curl && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY package.json /home/user/calutil/package.json
COPY cli.js /home/user/calutil/cli.js
COPY src/ /home/user/calutil/src/
COPY test/ /home/user/calutil/test/

RUN npm install
