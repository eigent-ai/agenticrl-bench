FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /opt/audit
RUN apt-get update && apt-get install -y build-essential git curl tmux perl findutils grep gawk coreutils python3 jq
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
RUN mkdir -p /opt/audit/output /opt/webapp
COPY audit_config.json /opt/audit/audit_config.json
COPY exclusions.conf /opt/audit/exclusions.conf
COPY run_audit.sh /opt/audit/run_audit.sh
RUN chmod +x /opt/audit/run_audit.sh
COPY setup_env.sh /tmp/setup_env.sh
RUN chmod +x /tmp/setup_env.sh && /tmp/setup_env.sh
RUN rm /tmp/setup_env.sh
