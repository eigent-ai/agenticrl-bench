#!/bin/bash
mkdir -p /var/monitor
python3 /opt/monitor/generator.py | \
    python3 /opt/monitor/filter.py | \
    python3 /opt/monitor/consumer.py
