#!/bin/bash
set -e

echo "[1/3] Starting display server..."
bash /opt/ci_gl/start_xvfb.sh

echo "[2/3] Setting up OpenGL environment..."
source /opt/ci_gl/gl_env.sh

echo "[3/3] Generating GL capability report..."
python3 /opt/ci_gl/generate_report.py

echo "Pipeline completed. Report written to /tmp/gl_report.json"
