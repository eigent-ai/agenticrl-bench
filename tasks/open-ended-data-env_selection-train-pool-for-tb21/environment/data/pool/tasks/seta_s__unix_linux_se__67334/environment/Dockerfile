FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /root

RUN apt-get update && apt-get install -y \
    openssh-server \
    tmux \
    python3-pip \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

RUN ssh-keygen -A

RUN groupadd sftponly && \
    useradd -m -g sftponly -s /bin/false sftpuser && \
    chown root:root /home/sftpuser && \
    chmod 755 /home/sftpuser

RUN mkdir -p /run/sshd

COPY sshd_config /etc/ssh/sshd_config

CMD ["sleep", "infinity"]
