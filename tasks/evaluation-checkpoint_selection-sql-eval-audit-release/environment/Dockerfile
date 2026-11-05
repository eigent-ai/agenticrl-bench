# Eval box with one H100: the eval suite, run cards and RL prompt set as before, the six release candidates in /models,
# and the SGLang build they were evaluated with (Miles v0.1.0 image: SGLang cb05a44f on the system Python 3.12).

# SQLite library and shell of the CPU image the suite is re-scored on (Debian bookworm, 3.40.1), so a query behaves the
# same on this box as in every later re-score.
FROM python:3.12.12-slim-bookworm@sha256:593bd06efe90efa80dc4eee3948be7c0fde4134606dd40d8dd8dbcade98e669c AS evalsqlite
RUN set -eux; \
    apt-get update; apt-get install -y --no-install-recommends sqlite3; rm -rf /var/lib/apt/lists/*; \
    python3 -c "import sqlite3; assert sqlite3.sqlite_version == '3.40.1', sqlite3.sqlite_version"; \
    mkdir /out; cp -L /usr/lib/x86_64-linux-gnu/libsqlite3.so.0 /out/libsqlite3.so.0; cp /usr/bin/sqlite3 /out/sqlite3

FROM radixark/miles@sha256:cd40db923225c4146e90fdf4aa04bc000b71c1e980cc42df6f368de7545eaa09

ENV DEBIAN_FRONTEND=noninteractive PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends git curl ca-certificates xz-utils procps less ripgrep jq tmux util-linux; \
    apt-get install -y --no-install-recommends libreadline8t64 || apt-get install -y --no-install-recommends libreadline8; \
    rm -rf /var/lib/apt/lists/*

# Tooling for the box; coding-agent CLIs are not baked in (the harness installs its own agent at run time).
RUN set -eux; \
    curl -fsSL https://nodejs.org/dist/v22.20.0/node-v22.20.0-linux-x64.tar.xz -o /tmp/node.tar.xz; \
    echo '00bbd05e306ea68b6e13e17360d0e2f680b493ef95f2fea1c4296ff7437530bc  /tmp/node.tar.xz' | sha256sum -c -; \
    tar -xJf /tmp/node.tar.xz -C /usr/local --strip-components=1; rm -f /tmp/node.tar.xz; \
    rm -rf /root/.npm /root/.cache

# The six release candidates (HF snapshots, ~4.6 GB each) at a pinned commit of their public repo.
ARG CANDIDATES_REPO=qijiashen/agentrl-bench-sql2b-candidates
ARG CANDIDATES_REV=4f7d25f7838afb163176424f8927d513dbf3a724
RUN set -eux; \
    hf download "$CANDIDATES_REPO" --revision "$CANDIDATES_REV" --local-dir /models --include 'sql2b-*/*'; \
    rm -rf /models/.cache /root/.cache/huggingface; \
    for c in sql2b-0919 sql2b-0922 sql2b-0925 sql2b-0927 sql2b-1002 sql2b-1006; do \
        test -s /models/$c/config.json; test -s /models/$c/tokenizer.json; ls /models/$c/*.safetensors; done; \
    test "$(ls /models | tr '\n' ' ')" = "sql2b-0919 sql2b-0922 sql2b-0925 sql2b-0927 sql2b-1002 sql2b-1006 "; \
    find /models -type d -exec chmod 0755 {} +; \
    find /models -type f -exec chmod 0644 {} +; \
    find /models -exec touch -h -d "2026-10-12 06:10:00" {} +

# The eval harness runs on the image's Python (aiohttp for run_eval; scoring is stdlib sqlite3) against SQLite 3.40.1.
COPY --from=evalsqlite /out/ /tmp/evalsqlite/
RUN set -eux; \
    M=$(python3 -c "import _sqlite3; print(_sqlite3.__file__)"); \
    L=$(ldd "$M" | awk '/libsqlite3\.so/ {print $3}'); test -n "$L"; L=$(readlink -f "$L"); \
    install -m 0644 /tmp/evalsqlite/libsqlite3.so.0 "$L"; ldconfig; \
    install -m 0755 /tmp/evalsqlite/sqlite3 /usr/local/bin/sqlite3; rm -rf /tmp/evalsqlite; \
    python3 -c "import sqlite3, aiohttp; assert sqlite3.sqlite_version == '3.40.1', sqlite3.sqlite_version"; \
    test "$(sqlite3 -version | cut -d' ' -f1)" = 3.40.1

COPY app/ /app/

RUN set -eux; \
    find /app -name __pycache__ -type d -prune -exec rm -rf {} +; \
    test -z "$(find /app -name '*.pyc' -o -name '*.orig' -o -name '*.rej' -o -name '.git' | head -1)"; \
    find /app -type d -exec chmod 0755 {} +; \
    find /app -type f -exec chmod 0644 {} +; \
    find /app/evalsuite/dbs -exec touch -h -d "2026-10-08 16:20:00" {} +; \
    find /app/evalsuite/harness /app/evalsuite/items.jsonl /app/evalsuite/README.md -exec touch -h -d "2026-10-09 11:04:00" {} +; \
    find /app/candidates /app/data -exec touch -h -d "2026-10-12 06:10:00" {} +; \
    find /app/evalsuite/dumps /app/evalsuite/leaderboard.md /app/evalsuite/leaderboard.json /app/release -exec touch -h -d "2026-10-12 10:05:00" {} +; \
    U=$(getent passwd 1000 | cut -d: -f1 || true); if [ -n "$U" ]; then userdel -r "$U" 2>/dev/null || userdel "$U"; fi; \
    G=$(getent group 1000 | cut -d: -f1 || true); if [ -n "$G" ]; then groupdel "$G"; fi; \
    useradd -m -u 1000 -s /bin/bash agent; \
    chown -R agent:agent /app; \
    test -z "$(find /app -type f -perm /022)"

RUN (command -v uv > /dev/null || python3 -m pip install --no-cache-dir 'uv==0.11.20') \
    && UV_TOOL_DIR=/opt/uv-tools UV_TOOL_BIN_DIR=/usr/local/bin uv tool install --python 3.12 'harbor-rewardkit==0.2.3' --with 'litellm==1.103.0' \
    && rewardkit --help > /dev/null

# PATH and offline model loading for commands run through su (the agent's shell), as the sibling Miles tasks set them.
RUN set -eux; \
    printf '%s\n' 'PATH="/opt/sglang/bin:/root/.cargo/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"' \
        'HF_HUB_OFFLINE=1' 'TRANSFORMERS_OFFLINE=1' > /etc/environment; \
    su agent -s /bin/bash -c 'python3 -c "import sglang, aiohttp, sqlite3; assert sqlite3.sqlite_version == \"3.40.1\""'; \
    su agent -s /bin/bash -c 'test -r /models/sql2b-1002/config.json && test -w /app/evalsuite/dumps'

ENV HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1

WORKDIR /app
