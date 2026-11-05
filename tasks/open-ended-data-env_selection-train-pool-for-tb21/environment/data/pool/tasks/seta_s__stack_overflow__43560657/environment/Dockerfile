FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    fish \
    python3 \
    python3-pip \
    python3-passlib \
    tmux \
    ansible \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/provision/vars

COPY provision/site.yml /opt/provision/site.yml
COPY provision/vars/users.yml /opt/provision/vars/users.yml
COPY provision/ansible.cfg /opt/provision/ansible.cfg

RUN grep -v fish /etc/shells > /tmp/shells_clean && mv /tmp/shells_clean /etc/shells

WORKDIR /opt/provision
