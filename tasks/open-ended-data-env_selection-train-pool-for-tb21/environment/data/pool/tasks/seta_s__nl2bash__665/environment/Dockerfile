FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /opt/workspace-manager

RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    findutils \
    jq \
    python3 \
    python3-pip \
    python3-venv \
    tmux \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Copy project structure
COPY bin/ /opt/workspace-manager/bin/
COPY config/ /opt/workspace-manager/config/
COPY hooks/ /opt/workspace-manager/hooks/
COPY templates/ /opt/workspace-manager/templates/
COPY README.md /opt/workspace-manager/README.md
COPY setup_workspaces.sh /tmp/setup_workspaces.sh

# Make scripts executable
RUN chmod +x bin/*.sh hooks/*.sh

# Set up pre-existing workspaces
RUN bash /tmp/setup_workspaces.sh && rm /tmp/setup_workspaces.sh
