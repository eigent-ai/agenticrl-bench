FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv tmux curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

RUN pip3 install --no-cache-dir --break-system-packages \
    scikit-learn==1.3.2 numpy==1.26.2 pandas==2.1.3 pyyaml==6.0.1

WORKDIR /home/user/feature_analysis

RUN mkdir -p src config data results

COPY src/__init__.py src/
COPY src/preprocessing.py src/
COPY src/model.py src/
COPY src/importance.py src/
COPY src/report.py src/
COPY config/features.yaml config/
COPY run_pipeline.py .
COPY README.md .
COPY generate_data.py /tmp/generate_data.py

RUN python3 /tmp/generate_data.py && rm /tmp/generate_data.py
