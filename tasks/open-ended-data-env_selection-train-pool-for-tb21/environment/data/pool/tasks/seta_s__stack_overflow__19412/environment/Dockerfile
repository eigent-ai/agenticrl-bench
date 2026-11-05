FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

WORKDIR /opt/sampler

RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 tmux curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/sampler/queries /opt/sampler/output

COPY setup_db.py /tmp/setup_db.py
COPY sample.sh /opt/sampler/sample.sh
COPY create_view.sql /opt/sampler/queries/create_view.sql
COPY select_sample.sql /opt/sampler/queries/select_sample.sql
COPY assign_group.sql /opt/sampler/queries/assign_group.sql

RUN python /tmp/setup_db.py && rm /tmp/setup_db.py
RUN chmod +x /opt/sampler/sample.sh
