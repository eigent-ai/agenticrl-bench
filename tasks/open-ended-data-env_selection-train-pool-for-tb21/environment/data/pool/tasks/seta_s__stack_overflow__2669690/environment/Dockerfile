FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

WORKDIR /opt/aggregator

RUN apt-get update && apt-get install -y --no-install-recommends tmux curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/aggregator/lib /opt/aggregator/responses /opt/aggregator/output

COPY aggregate.py /opt/aggregator/aggregate.py
COPY config.json /opt/aggregator/config.json
COPY __init__.py /opt/aggregator/lib/__init__.py
COPY sanitizer.py /opt/aggregator/lib/sanitizer.py
COPY calendar.json /opt/aggregator/responses/calendar.json
COPY social.json /opt/aggregator/responses/social.json
COPY docs.json /opt/aggregator/responses/docs.json
COPY feed.json /opt/aggregator/responses/feed.json
COPY analytics.json /opt/aggregator/responses/analytics.json
