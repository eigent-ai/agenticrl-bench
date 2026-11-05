FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    openssh-server \
    openssh-client \
    tmux \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN ssh-keygen -A && mkdir -p /run/sshd

RUN mkdir -p /opt/deploy/keys && \
    ssh-keygen -t ed25519 -f /opt/deploy/keys/ci_key -N "" && \
    useradd -m -s /bin/bash deployuser && \
    mkdir -p /home/deployuser/.ssh && \
    cp /opt/deploy/keys/ci_key.pub /home/deployuser/.ssh/authorized_keys && \
    chown -R deployuser:deployuser /home/deployuser/.ssh && \
    chmod 700 /home/deployuser/.ssh && \
    chmod 600 /home/deployuser/.ssh/authorized_keys

RUN chmod 644 /opt/deploy/keys/ci_key

RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

COPY agent_init.sh /opt/deploy/agent_init.sh
COPY run_deploy.sh /opt/deploy/run_deploy.sh
RUN chmod +x /opt/deploy/agent_init.sh /opt/deploy/run_deploy.sh

CMD ["/bin/bash", "-c", "/usr/sbin/sshd && sleep infinity"]
