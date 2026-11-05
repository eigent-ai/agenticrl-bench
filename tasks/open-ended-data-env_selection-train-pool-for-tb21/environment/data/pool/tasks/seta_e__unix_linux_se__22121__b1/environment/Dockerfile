FROM alpine:3.19@sha256:6baf43584bcb78f2e5847d1de515f23499913ac9f12bdf834811a3145eb11ca1
WORKDIR /app
RUN apk add --no-cache python3 iproute2 curl bash tmux git
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
RUN mkdir -p /opt/net-audit /var/log/net-audit
COPY scan.py /opt/net-audit/scan.py
