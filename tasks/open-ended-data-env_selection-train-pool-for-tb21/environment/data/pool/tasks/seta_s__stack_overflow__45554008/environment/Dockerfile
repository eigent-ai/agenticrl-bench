FROM python:3.11-slim@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377

RUN apt-get update && apt-get install -y tmux curl && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh
ENV PATH="/root/.cargo/bin:/root/.local/bin:$PATH"

WORKDIR /app

RUN pip install --no-cache-dir \
    scikit-learn==1.5.2 \
    numpy==1.26.4 \
    pandas==2.2.3

COPY salary_data.csv /app/salary_data.csv
COPY ml_pipeline.py /app/ml_pipeline.py

RUN chmod +x /app/ml_pipeline.py
