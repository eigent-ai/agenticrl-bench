FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    findutils \
    tmux \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN mkdir -p /opt/maintenance/scripts \
             /opt/maintenance/bin \
             /opt/maintenance/workspace \
             /opt/maintenance/etc \
             /opt/maintenance/run

COPY scripts/run_pipeline.sh   /opt/maintenance/scripts/run_pipeline.sh
COPY scripts/forward_files.sh  /opt/maintenance/scripts/forward_files.sh
COPY scripts/sweep_workspace.sh /opt/maintenance/scripts/sweep_workspace.sh
COPY scripts/preflight.sh      /opt/maintenance/scripts/preflight.sh

COPY bin/stage_validate  /opt/maintenance/bin/stage_validate
COPY bin/stage_process   /opt/maintenance/bin/stage_process
COPY bin/stage_finalize  /opt/maintenance/bin/stage_finalize
COPY bin/archiver        /opt/maintenance/bin/archiver
COPY bin/run_job         /opt/maintenance/bin/run_job

COPY etc/maintenance.conf /opt/maintenance/etc/maintenance.conf

RUN chmod +x /opt/maintenance/scripts/run_pipeline.sh \
             /opt/maintenance/scripts/forward_files.sh \
             /opt/maintenance/scripts/sweep_workspace.sh \
             /opt/maintenance/scripts/preflight.sh \
             /opt/maintenance/bin/stage_validate \
             /opt/maintenance/bin/stage_process \
             /opt/maintenance/bin/stage_finalize \
             /opt/maintenance/bin/archiver \
             /opt/maintenance/bin/run_job

RUN touch /opt/maintenance/run/pipeline.log \
          /opt/maintenance/run/archive.log \
          /opt/maintenance/run/job.log

RUN touch /opt/maintenance/workspace/report_2023.bak \
          /opt/maintenance/workspace/config_snapshot.bak \
          /opt/maintenance/workspace/staging_output.csv \
          /opt/maintenance/workspace/temp_work.tmp
