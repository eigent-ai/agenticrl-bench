FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y openjdk-17-jdk-headless tmux curl python3

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY src/ /app/src/
COPY data/ /app/data/
COPY run.sh /app/run.sh

RUN chmod +x /app/run.sh
RUN mkdir -p /app/output /app/build
