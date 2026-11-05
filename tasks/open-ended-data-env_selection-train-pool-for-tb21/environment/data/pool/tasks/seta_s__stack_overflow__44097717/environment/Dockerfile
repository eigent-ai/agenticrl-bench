FROM ruby:3.2-slim@sha256:84184c9e2c368885a1d0c93ad1953c33d81081058d274b87b4aa6f3e209e5d16

RUN apt-get update && apt-get install -y \
    python3 python3-pip tmux curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY app/ /app/
RUN mkdir -p /app/output

CMD ["bash"]
