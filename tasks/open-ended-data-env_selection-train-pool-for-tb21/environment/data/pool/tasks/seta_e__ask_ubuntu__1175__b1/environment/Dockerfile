FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

RUN apt-get update && apt-get install -y python3 tmux curl
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /app/scripts /app/data/reports

COPY process_metrics.py /app/scripts/process_metrics.py
COPY metrics_input.json /app/data/metrics_input.json

RUN chmod +x /app/scripts/process_metrics.py
RUN touch /app/data/processing_manifest.txt
