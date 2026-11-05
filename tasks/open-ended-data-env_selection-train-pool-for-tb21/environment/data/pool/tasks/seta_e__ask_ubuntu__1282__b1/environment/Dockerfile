FROM opensuse/leap:15.6@sha256:79be7751205ea84559990fb76b1bec71e38d6fad41c70a4f6c921b803b58f421

WORKDIR /app

RUN zypper --non-interactive refresh && \
    zypper --non-interactive install -y curl gzip tmux tar

# Pre-install uv so tests/test.sh needs no network at test time
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
