FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

WORKDIR /app

RUN apt-get update && apt-get install -y curl openssl nginx ca-certificates tmux build-essential git

# Pre-install uv
RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

# Generate certificates
COPY generate_certs.sh /tmp/generate_certs.sh
RUN chmod +x /tmp/generate_certs.sh && /tmp/generate_certs.sh && rm /tmp/generate_certs.sh

# Install nginx config
COPY nginx-services.conf /etc/nginx/sites-enabled/services.conf

# Install health check script
COPY health_check.sh /app/health_check.sh
RUN chmod +x /app/health_check.sh

# Install entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["sleep", "infinity"]
