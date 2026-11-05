FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

WORKDIR /opt/metricspipe

COPY install_deps.py /tmp/install_deps.py
RUN python3 /tmp/install_deps.py && rm /tmp/install_deps.py

COPY config.json /opt/metricspipe/config.json
COPY aggregate.py /opt/metricspipe/aggregate.py
COPY validate.py /opt/metricspipe/validate.py
COPY setup_data.py /tmp/setup_data.py

RUN python3 /tmp/setup_data.py && rm /tmp/setup_data.py

RUN mkdir -p "/opt/metrics pipe_link/output/" && \
    ln -s "/opt/metrics pipe_link/output/" /opt/metricspipe/output
