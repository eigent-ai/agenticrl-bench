#!/bin/bash
# NFS Performance Benchmark Suite - Orchestrator
# Runs the full benchmark pipeline: bench -> parse -> report

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$SCRIPT_DIR/config.yaml"
RESULTS_DIR=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG'))['results_dir'])")

echo "=== NFS Performance Benchmark Suite ==="
echo "Config: $CONFIG"
echo "Results: $RESULTS_DIR"
echo ""

# Step 1: Run benchmarks
echo "[1/3] Running benchmarks..."
bash "$SCRIPT_DIR/run_bench.sh" "$CONFIG" "$RESULTS_DIR"

# Step 2: Parse results
echo "[2/3] Parsing benchmark results..."
python3 "$SCRIPT_DIR/parse_results.py" "$RESULTS_DIR"

# Step 3: Generate report
echo "[3/3] Generating JSON report..."
python3 "$SCRIPT_DIR/generate_report.py" "$CONFIG" "$RESULTS_DIR"

echo ""
echo "=== Benchmark suite complete ==="
echo "Report: $RESULTS_DIR/report.json"
