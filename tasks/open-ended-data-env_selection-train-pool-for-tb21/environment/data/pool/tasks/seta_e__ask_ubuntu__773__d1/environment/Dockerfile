FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y ufw sudo build-essential git curl tmux

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Create a non-root user 'user' with sudo access
RUN useradd -m -s /bin/bash user && \
    echo "user:password" | chpasswd && \
    usermod -aG sudo user && \
    echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Copy UFW rules files
COPY user.rules /lib/ufw/user.rules
COPY user6.rules /lib/ufw/user6.rules

# Create home directory for user
RUN mkdir -p /home/user && chown -R user:user /home/user

WORKDIR /app
