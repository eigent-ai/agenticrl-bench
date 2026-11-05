FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app
RUN apt-get update && apt-get install -y python3 coreutils procps tmux curl && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
COPY setup_env.sh /app/setup_env.sh
RUN chmod +x /app/setup_env.sh && /app/setup_env.sh
COPY backup_data.py /app/backup_data.py
RUN chmod +x /app/backup_data.py
