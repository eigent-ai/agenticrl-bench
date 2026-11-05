FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y python3 tmux curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /setup /opt/pkg-audit /var/log/pkg-audit

COPY create_logs.py       /setup/create_logs.py
COPY generate_report.py   /opt/pkg-audit/generate_report.py
COPY report_schema.json   /opt/pkg-audit/report_schema.json

RUN python3 /setup/create_logs.py
