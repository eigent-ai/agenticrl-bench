FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    screen \
    reptyr \
    tmux \
    ncurses-bin \
    procps \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

RUN mkdir -p /opt/monitor
COPY health_check.sh /opt/monitor/health_check.sh
RUN chmod +x /opt/monitor/health_check.sh

COPY screenrc /root/.screenrc

RUN echo 'kernel.yama.ptrace_scope = 0' >> /etc/sysctl.d/99-ptrace.conf || true

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
