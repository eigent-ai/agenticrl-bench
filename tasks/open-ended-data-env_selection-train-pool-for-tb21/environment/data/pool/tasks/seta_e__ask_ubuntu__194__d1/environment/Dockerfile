FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Set up history environment variables
ENV HISTTIMEFORMAT="%F %T "
ENV HISTFILE=/root/.bash_history

# Copy the pre-populated bash history file
COPY bash_history /root/.bash_history
RUN chmod 600 /root/.bash_history
