FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

RUN apt-get update && apt-get install -y \
    xvfb \
    twm \
    x11-utils \
    x11-apps \
    xdotool \
    xauth \
    procps \
    curl \
    tmux \
    xfonts-base \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/xci

COPY twmrc /root/.twmrc

COPY run_test.sh /opt/xci/run_test.sh
COPY setup_display.sh /opt/xci/setup_display.sh
COPY start_session.sh /opt/xci/start_session.sh
COPY query_window.sh /opt/xci/query_window.sh
COPY teardown.sh /opt/xci/teardown.sh

RUN chmod +x /opt/xci/run_test.sh \
              /opt/xci/setup_display.sh \
              /opt/xci/start_session.sh \
              /opt/xci/query_window.sh \
              /opt/xci/teardown.sh
