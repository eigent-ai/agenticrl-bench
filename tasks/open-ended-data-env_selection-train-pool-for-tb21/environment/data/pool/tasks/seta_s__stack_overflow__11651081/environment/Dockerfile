FROM node:20-alpine@sha256:fb4cd12c85ee03686f6af5362a0b0d56d50c58a04632e6c0fb8363f609372293

RUN apk add --no-cache curl tmux bash

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

WORKDIR /app

COPY package.json /app/package.json
COPY src/ /app/src/
COPY data/ /app/data/
COPY README.txt /app/README.txt

RUN mkdir -p /app/output
