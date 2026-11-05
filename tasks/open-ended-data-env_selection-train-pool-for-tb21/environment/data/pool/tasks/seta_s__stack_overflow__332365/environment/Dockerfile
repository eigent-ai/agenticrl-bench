FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

WORKDIR /opt/school_app

RUN apt-get update && apt-get install -y --no-install-recommends \
    tmux \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN pip install --no-cache-dir flask

COPY setup_db.py /tmp/setup_db.py
RUN python /tmp/setup_db.py && rm /tmp/setup_db.py

COPY app.py /opt/school_app/app.py
COPY routes/ /opt/school_app/routes/
COPY 001_initial.sql /opt/school_app/migrations/001_initial.sql
COPY access.log /opt/school_app/logs/access.log
