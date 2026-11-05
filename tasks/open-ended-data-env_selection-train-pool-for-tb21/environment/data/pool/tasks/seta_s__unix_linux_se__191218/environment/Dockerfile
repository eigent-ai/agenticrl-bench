FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /opt/imagebuilder

RUN apt-get update && apt-get install -y \
    grub-pc-bin \
    grub-common \
    grub2-common \
    parted \
    kpartx \
    e2fsprogs \
    dosfstools \
    file \
    curl \
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/imagebuilder/output /opt/imagebuilder/templates /mnt/image

COPY build-image.sh /opt/imagebuilder/build-image.sh
COPY ifcfg-eth0.tpl /opt/imagebuilder/templates/ifcfg-eth0.tpl

RUN chmod +x /opt/imagebuilder/build-image.sh

WORKDIR /app
