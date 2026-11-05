#!/bin/bash
# The pool's GRPO training job on this box's GPU; `run_grpo.sh --help` for the details.
exec /usr/bin/python3 -I /opt/pooltrain/pooltrain.py "$@"
