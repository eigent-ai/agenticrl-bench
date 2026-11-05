FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux lm-sensors python3 jq procps

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Create config directory and copy config
RUN mkdir -p /etc/syshealth
COPY config.json /etc/syshealth/config.json

# Copy skeleton template
COPY syshealth-template.py /app/syshealth-template.py
