FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential git curl tmux \
    monit python3 procps coreutils \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY monitrc /etc/monit/monitrc
RUN chmod 0700 /etc/monit/monitrc

RUN mkdir -p /etc/monit/conf.d
COPY app.conf /etc/monit/conf.d/app.conf
COPY filesystem.conf /etc/monit/conf.d/filesystem.conf

RUN mkdir -p /opt/monitoring
COPY pio.sh /opt/monitoring/pio.sh
RUN chmod +x /opt/monitoring/pio.sh

RUN mkdir -p /opt/app
COPY server.py /opt/app/server.py
COPY start.sh /opt/app/start.sh
COPY stop.sh /opt/app/stop.sh
RUN chmod +x /opt/app/start.sh /opt/app/stop.sh
