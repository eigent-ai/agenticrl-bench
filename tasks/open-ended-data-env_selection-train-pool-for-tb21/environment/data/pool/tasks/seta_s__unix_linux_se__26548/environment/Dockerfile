FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

RUN apt-get update && apt-get install -y tmux python3 curl && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/monitor /opt/scripts

COPY tmux.conf /root/.tmux.conf
COPY generate_data.py /opt/scripts/generate_data.py
COPY save_output.sh /opt/monitor/save_output.sh
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /opt/monitor/save_output.sh /entrypoint.sh /opt/scripts/generate_data.py

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]
