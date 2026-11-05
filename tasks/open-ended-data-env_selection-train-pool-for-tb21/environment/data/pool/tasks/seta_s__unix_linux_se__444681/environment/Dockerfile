FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    dconf-cli \
    dbus \
    tmux \
    python3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /etc/dconf/db/local.d \
             /etc/dconf/db/site.d \
             /etc/dconf/profile

COPY dconf_profile_user /etc/dconf/profile/user
COPY dconf_local_00_gnome_audio /etc/dconf/db/local.d/00-gnome-audio

RUN mkdir -p /etc/pulse
COPY default.pa /etc/pulse/default.pa

COPY deployment-notes.txt /root/deployment-notes.txt

WORKDIR /app
