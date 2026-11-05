FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y \
    iproute2 \
    net-tools \
    kmod \
    python3 \
    curl \
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

RUN mkdir -p /opt/labnet

COPY setup_network.sh /opt/labnet/setup_network.sh
COPY server.py /opt/labnet/server.py

RUN chmod 755 /opt/labnet/setup_network.sh /opt/labnet/server.py

CMD ["sleep", "infinity"]
