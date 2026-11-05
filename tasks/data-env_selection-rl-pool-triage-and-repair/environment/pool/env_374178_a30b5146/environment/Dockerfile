FROM ubuntu:24.04

WORKDIR /home/agent

RUN apt-get update && apt-get install -y build-essential git curl tmux systemd procps

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Create service scripts directory
RUN mkdir -p /home/agent/services /var/run /var/log /etc/systemd/system/multi-user.target.wants

# Copy service scripts
COPY data_collector.sh /home/agent/services/data_collector.sh
COPY log_processor.sh /home/agent/services/log_processor.sh
COPY health_reporter.sh /home/agent/services/health_reporter.sh

RUN chmod +x /home/agent/services/data_collector.sh /home/agent/services/log_processor.sh /home/agent/services/health_reporter.sh

# Test runner. Task sandboxes have no network, so the runner and its packages are baked into the image.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tmux curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
ENV PATH=/root/.local/bin:$PATH UV_CACHE_DIR=/opt/uv-cache
# The image builder may point uv at its own package mirror with the cache off; the offline runner needs a pypi.org cache.
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh \
    && env -u UV_NO_CACHE -u UV_INDEX_URL -u PIP_INDEX_URL uvx -p 3.13 -w pytest==8.4.1 -w pytest-json-ctrf==0.3.5 pytest --version
ENV UV_OFFLINE=1
