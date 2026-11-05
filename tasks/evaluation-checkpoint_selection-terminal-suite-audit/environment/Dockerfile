FROM python:3.12.12-slim-bookworm@sha256:593bd06efe90efa80dc4eee3948be7c0fde4134606dd40d8dd8dbcade98e669c

ENV DEBIAN_FRONTEND=noninteractive PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends git curl ca-certificates xz-utils procps less ripgrep jq tmux sqlite3 \
        util-linux file tree diffutils patch build-essential openssh-server; \
    rm -rf /var/lib/apt/lists/*

# Tooling for the box; coding-agent CLIs are not baked in (the harness installs its own agent at run time).
RUN set -eux; \
    curl -fsSL https://nodejs.org/dist/v22.20.0/node-v22.20.0-linux-x64.tar.xz -o /tmp/node.tar.xz; \
    echo "00bbd05e306ea68b6e13e17360d0e2f680b493ef95f2fea1c4296ff7437530bc  /tmp/node.tar.xz" | sha256sum -c -; \
    tar -xJf /tmp/node.tar.xz --no-same-owner -C /usr/local --strip-components=1; \
    rm -f /tmp/node.tar.xz; \
    pip install uv==0.8.17; \
    rm -rf /root/.npm /root/.cache

# Harbor (same build the cluster runs) and a few libraries the suite's tests use, for poking at tasks locally.
RUN set -eux; \
    uv venv /opt/harbor --python /usr/local/bin/python3.12; \
    uv pip install --no-cache --python /opt/harbor/bin/python \
        "harbor[modal] @ git+https://github.com/harbor-framework/harbor@3e30cca047a4d0dc1fb209bf5a74ff761b794b90" \
        "litellm==1.103.0"; \
    /opt/harbor/bin/python -I -c "import importlib.metadata as m; assert m.version('litellm') == '1.103.0'"; \
    ln -s /opt/harbor/bin/harbor /usr/local/bin/harbor; \
    pip install pytest==8.4.1 beautifulsoup4==4.14.2 numpy==2.3.4 pandas==2.3.3 requests==2.32.5 pillow==12.0.0; \
    rm -rf /root/.cache; \
    chown -R root:root /usr/local /opt/harbor; chmod -R go-w /usr/local /opt/harbor; harbor --version

COPY app/ /app/

RUN set -eux; \
    find /app -name __pycache__ -type d -prune -exec rm -rf {} +; \
    test -z "$(find /app -name '*.pyc' -o -name '*.orig' -o -name '*.rej' -o -name '.git' | head -1)"; \
    find /app -type d -exec chmod 0755 {} +; \
    chmod -R go-w,a+r /app; \
    find /app/suite -exec touch -h -d "2025-11-04 09:30:00" {} +; \
    find /app/eval -exec touch -h -d "2026-09-29 15:12:00" {} +; \
    useradd -m -u 1000 -s /bin/bash agent; \
    chown -R agent:agent /app; \
    test -z "$(find /app -type f -perm /022)"

WORKDIR /app
