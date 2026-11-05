FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /opt/registry
RUN apt-get update && apt-get install -y curl tmux && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
COPY setup_registry.sh /tmp/setup_registry.sh
RUN chmod +x /tmp/setup_registry.sh && bash /tmp/setup_registry.sh && rm /tmp/setup_registry.sh
COPY maintain.sh /opt/registry/maintain.sh
RUN chmod +x /opt/registry/maintain.sh
