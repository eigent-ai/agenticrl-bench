FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/resmanager/templates /var/shared_resources

COPY broker.py /opt/resmanager/broker.py
COPY worker.py /opt/resmanager/worker.py
COPY resource_manager.py /opt/resmanager/resource_manager.py
COPY run_scenario.py /opt/resmanager/run_scenario.py
RUN chmod +x /opt/resmanager/run_scenario.py
COPY capsule.template /opt/resmanager/templates/capsule.template
COPY cube.template /opt/resmanager/templates/cube.template
COPY sphere.template /opt/resmanager/templates/sphere.template
