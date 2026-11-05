#!/bin/bash
# Memory monitoring report generator
# Orchestrates all components and generates a summary report

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/memwatch.conf"

mkdir -p "$REPORT_DIR"

REPORT_FILE="${REPORT_DIR}/report.txt"

{
    echo "============================================="
    echo "  Memory Monitoring Toolkit Report"
    echo "  Generated: $(date)"
    echo "============================================="
    echo ""

    echo "--- System Information ---"
    echo "System Page Size: ${PAGE_SIZE} bytes"
    echo "Page Shift: ${PAGE_SHIFT}"
    echo ""

    echo "--- Memory Analysis (analyze.py) ---"
    python3 "${SCRIPT_DIR}/analyze.py" 2>&1
    echo ""

    echo "--- vmstat Parsed Values ---"
    bash "${SCRIPT_DIR}/vmstat_parse.sh" 2>&1
    echo ""

    echo "--- Shared Memory Test ---"
    bash "${SCRIPT_DIR}/shmsetup.sh" 2>&1
    echo ""

    echo "--- Shared Memory Alignment Test ---"
    bash "${SCRIPT_DIR}/shmtest.sh" 2>&1
    echo ""

    echo "============================================="
    echo "  End of Report"
    echo "============================================="
} > "$REPORT_FILE" 2>&1

echo "Report generated at: $REPORT_FILE"
exit 0
