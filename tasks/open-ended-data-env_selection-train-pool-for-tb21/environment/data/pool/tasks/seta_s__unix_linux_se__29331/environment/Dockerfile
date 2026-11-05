FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && apt-get install -y \
    xvfb x11-utils python3 tmux curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

RUN mkdir -p /opt/display /var/log/xorg-audit /var/report

COPY launch.sh /opt/display/launch.sh
COPY audit_drivers.py /opt/display/audit_drivers.py
COPY display.log /var/log/xorg-audit/display.log

RUN chmod +x /opt/display/launch.sh /opt/display/audit_drivers.py
