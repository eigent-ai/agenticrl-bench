FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl tmux \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN pip install --no-cache-dir pyyaml beautifulsoup4 lxml

COPY sec_audit.py /app/sec_audit.py
COPY compliance_rules.yaml /app/compliance_rules.yaml

RUN mkdir -p /app/templates /app/report

COPY login.html /app/templates/login.html
COPY register.html /app/templates/register.html
COPY change_password.html /app/templates/change_password.html
COPY admin_login.html /app/templates/admin_login.html
COPY profile_edit.html /app/templates/profile_edit.html
