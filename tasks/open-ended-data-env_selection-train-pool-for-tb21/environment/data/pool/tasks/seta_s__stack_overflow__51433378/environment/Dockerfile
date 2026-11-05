FROM python:3.11-slim@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl tmux && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY model.py /app/model.py
COPY data_utils.py /app/data_utils.py
COPY config.json /app/config.json
COPY build_weights.py /app/build_weights.py
COPY predict.py /app/predict.py
COPY train.py /app/train.py
COPY validate.py /app/validate.py

RUN mkdir -p /app/weights && python build_weights.py
RUN rm -f /app/build_weights.py
