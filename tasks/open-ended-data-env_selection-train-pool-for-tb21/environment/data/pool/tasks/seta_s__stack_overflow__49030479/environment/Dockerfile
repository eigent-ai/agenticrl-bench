FROM python:3.11-slim@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377

WORKDIR /home/user/ml_evaluation

RUN apt-get update && apt-get install -y --no-install-recommends \
    tmux \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN pip install --no-cache-dir \
    scikit-learn==1.4.0 \
    numpy \
    pandas \
    pyyaml

COPY config.yaml .
COPY data_loader.py .
COPY cv_utils.py .
COPY evaluate.py .
COPY report.py .
COPY generate_dataset.py .

RUN python generate_dataset.py && rm generate_dataset.py

RUN mkdir -p output
