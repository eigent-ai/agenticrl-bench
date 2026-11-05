#!/bin/bash
# NFS Performance Benchmark Runner
# Executes dd and fio benchmarks against the configured test directory

CONFIG="$1"
RESULTS_DIR="$2"

if [ -z "$CONFIG" ] || [ -z "$RESULTS_DIR" ]; then
    echo "Usage: run_bench.sh <config.yaml> <results_dir>"
    exit 1
fi

BLOCK_SIZE=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG'))['block_size'])")
FILE_SIZE_MB=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG'))['file_size_mb'])")
TEST_DIR=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG'))['test_dir'])")
FIO_ENABLED=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG')).get('fio_enabled', False))")
FIO_JOB=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG')).get('fio_job_file', ''))")

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Calculate block size in bytes for count computation
BS_NUM=$(echo "$BLOCK_SIZE" | grep -oP '^\d+')
BS_SUFFIX=$(echo "$BLOCK_SIZE" | grep -oP '[a-zA-Z]+$' || true)
case "$BS_SUFFIX" in
    k|K) BLOCK_SIZE_BYTES=$((BS_NUM * 1024)) ;;
    m|M) BLOCK_SIZE_BYTES=$((BS_NUM * 1024 * 1024)) ;;
    *)   BLOCK_SIZE_BYTES=$BS_NUM ;;
esac
COUNT=$((FILE_SIZE_MB * 1024 * 1024 / BLOCK_SIZE_BYTES))

echo "Benchmark configuration:"
echo "  Block size: $BLOCK_SIZE"
echo "  File size: ${FILE_SIZE_MB} MB"
echo "  Test directory: $TEST_DIR"
echo "  Count: $COUNT blocks"
echo ""

for test_name in $(python3 -c "import yaml; ts=yaml.safe_load(open('$CONFIG'))['tests']; print(' '.join(ts))"); do
    echo "Running test: $test_name"

    case "$test_name" in
        seq_write)
            dd if=/dev/zero of="$TEST_DIR/testfile_write" bs="$BLOCK_SIZE" count="$COUNT" conv=fdatasync 2>/dev/null
            echo "  seq_write complete"
            ;;
        seq_read)
            if [ ! -f "$TEST_DIR/testfile_write" ]; then
                dd if=/dev/zero of="$TEST_DIR/testfile_write" bs="$BLOCK_SIZE" count="$COUNT" conv=fdatasync 2>/dev/null
            fi
            dd if="$TEST_DIR/testfile_write" of=/dev/null bs="$BLOCK_SIZE" count="$COUNT" 2>/dev/null
            echo "  seq_read complete"
            ;;
        *)
            echo "  Unknown test: $test_name, skipping"
            ;;
    esac
done

if [ "$FIO_ENABLED" = "True" ]; then
    echo ""
    echo "Running fio benchmarks..."
    FIO_JOB_PATH="$SCRIPT_DIR/$FIO_JOB"
    if [ -f "$FIO_JOB_PATH" ]; then
        fio "$FIO_JOB_PATH" --output="$RESULTS_DIR/fio_output.json" --output-format=json
        echo "  fio benchmark complete"
    else
        echo "  Warning: fio job file not found at $FIO_JOB_PATH"
        echo '{"error": "fio job file not found", "status": "error"}' > "$RESULTS_DIR/fio_output.json"
    fi
fi

echo ""
echo "Benchmarks finished."
