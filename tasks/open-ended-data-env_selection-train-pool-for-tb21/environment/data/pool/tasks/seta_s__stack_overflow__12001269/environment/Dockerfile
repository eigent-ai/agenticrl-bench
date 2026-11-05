FROM python:3.13-alpine@sha256:bf12ecc0bea3f171d55145dd02c78b5eeb09f30ee2ac9cc2b4c9e4e8f5e30741

WORKDIR /opt/webapp

RUN apk add --no-cache curl tmux bash

RUN pip install --no-cache-dir flask==3.1.1 uv==0.10.11

COPY app.py /opt/webapp/app.py
COPY config.py /opt/webapp/config.py
COPY run_tests.sh /opt/webapp/run_tests.sh
COPY README.md /opt/webapp/README.md

RUN chmod +x /opt/webapp/run_tests.sh
