FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app
RUN apt-get update && apt-get install -y procps coreutils bash python3 tmux curl build-essential
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
COPY procfleet/ /opt/procfleet/
RUN chmod +x /opt/procfleet/bin/*.sh /opt/procfleet/workers/*.sh
RUN mkdir -p /opt/procfleet/logs /opt/procfleet/run /opt/procfleet/pipes
