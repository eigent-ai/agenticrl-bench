#!/bin/bash
# Sandbox runner: apply resource limits then execute a student submission

if [ $# -ne 1 ]; then
    echo "Usage: $0 <submission.py>" >&2
    exit 2
fi

ulimit -v 1024
ulimit -t 10
ulimit -f 2048
python "$1"
