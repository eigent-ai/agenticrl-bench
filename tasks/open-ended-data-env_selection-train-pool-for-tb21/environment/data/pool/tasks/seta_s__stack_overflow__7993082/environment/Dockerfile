FROM python:3.13-slim@sha256:d98cc29d3266e535dd9da1099688d9cb3ca4753813571e071763d17725460962

RUN apt-get update && apt-get install -y git tmux && rm -rf /var/lib/apt/lists/*
RUN pip install uv

WORKDIR /opt/sim_project

COPY simulation.py analyze_logbook.py run_experiments.sh README.md ./
RUN chmod +x run_experiments.sh

RUN git init \
    && git config user.email "researcher@example.com" \
    && git config user.name "Researcher" \
    && git add . \
    && git commit -m "Initial simulation framework" \
    && echo "" >> README.md \
    && echo "# v1.1 - add scatter experiment" >> README.md \
    && git add README.md \
    && git commit -m "Add scatter experiment type"

CMD ["/bin/bash"]
