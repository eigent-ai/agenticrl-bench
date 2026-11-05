FROM dart:3.3@sha256:693b65a23ec9addfc5ffef57066ed139128ccd180d5d26694002a5df38386771

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    tmux \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /home/user/env_logger
COPY env_logger/ /home/user/env_logger/
RUN dart pub get
