FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux python3 python3-pip
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/provisioner

COPY packages.conf /opt/provisioner/packages.conf
COPY install.sh /opt/provisioner/install.sh
RUN chmod 755 /opt/provisioner/install.sh

RUN rm -f /etc/apt/sources.list.d/ubuntu.sources
COPY sources.list /etc/apt/sources.list
COPY internal-mirror.list /etc/apt/sources.list.d/internal-mirror.list
