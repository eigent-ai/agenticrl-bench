FROM node:20-slim@sha256:2cf067cfed83d5ea958367df9f966191a942351a2df77d6f0193e162b5febfc0

RUN apt-get update && apt-get install -y tmux curl && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

WORKDIR /app

COPY package.json /app/package.json
RUN npm install

COPY server.js /app/server.js
COPY config.json /app/config.json

COPY file-checker.js /app/lib/file-checker.js
COPY route-check-file.js /app/routes/check-file.js
COPY route-theme-manifest.js /app/routes/theme-manifest.js
COPY route-health.js /app/routes/health.js
COPY route-fallback.js /app/routes/fallback.js

COPY default-style.css /app/assets/themes/default/style.css
COPY default-logo.png /app/assets/themes/default/logo.png
COPY default-app.js /app/assets/themes/default/app.js
COPY ocean-style.css /app/assets/themes/ocean/style.css
COPY ocean-logo.png /app/assets/themes/ocean/logo.png
COPY desert-style.css /app/assets/themes/desert/style.css
COPY fallback-logo.png /app/assets/defaults/fallback-logo.png
