FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

RUN apt-get update && apt-get install -y sqlite3 tmux curl && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN pip install uv

RUN mkdir -p /opt/doctracker/reports

COPY seed.sql /tmp/seed.sql
RUN sqlite3 /opt/doctracker/tracker.db < /tmp/seed.sql

COPY generate_reports.py /opt/doctracker/generate_reports.py
RUN chmod +x /opt/doctracker/generate_reports.py

WORKDIR /opt/doctracker
