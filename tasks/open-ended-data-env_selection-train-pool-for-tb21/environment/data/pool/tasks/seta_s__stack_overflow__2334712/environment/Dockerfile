FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-client \
    python3 \
    python3-psycopg2 \
    build-essential \
    git \
    curl \
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY init_db.sql /tmp/init_db.sql
COPY setup_db.sh /tmp/setup_db.sh
RUN chmod +x /tmp/setup_db.sh && /tmp/setup_db.sh

COPY config.ini /opt/datasync/config.ini
COPY run_pipeline.py /opt/datasync/run_pipeline.py
COPY sql/ /opt/datasync/sql/

WORKDIR /opt/datasync
