FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /opt/datapipe

RUN apt-get update && apt-get install -y bash coreutils python3 tmux curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY config.sh /opt/datapipe/config.sh
COPY ingest.sh /opt/datapipe/ingest.sh
COPY process_file.sh /opt/datapipe/process_file.sh
COPY check_processed.sh /opt/datapipe/check_processed.sh

RUN chmod +x /opt/datapipe/*.sh

RUN mkdir -p /opt/datapipe/data/incoming /opt/datapipe/data/processed /opt/datapipe/logs

COPY data/incoming/ /opt/datapipe/data/incoming/

RUN touch /opt/datapipe/processed.log /opt/datapipe/logs/pipeline.log

RUN bash /opt/datapipe/ingest.sh || true

WORKDIR /opt/datapipe
