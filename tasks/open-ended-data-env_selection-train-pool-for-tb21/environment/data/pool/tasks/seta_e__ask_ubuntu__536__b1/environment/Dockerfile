FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux jq procps

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN useradd -m -s /bin/bash user

RUN mkdir -p /home/user/pane_manager && chown -R user:user /home/user/pane_manager

COPY setup_tmux.sh /home/user/setup_tmux.sh
RUN chmod +x /home/user/setup_tmux.sh
