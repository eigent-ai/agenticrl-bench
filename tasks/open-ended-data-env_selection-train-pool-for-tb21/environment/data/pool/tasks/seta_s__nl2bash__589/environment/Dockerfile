FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux python3 jq

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Copy build assets
COPY search_patterns.conf /tmp/build/search_patterns.conf
COPY setup_env.sh /tmp/build/setup_env.sh
RUN chmod +x /tmp/build/setup_env.sh && /tmp/build/setup_env.sh && rm -rf /tmp/build
