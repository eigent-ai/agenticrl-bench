#!/bin/bash
OUT=/home/ubuntu/seed_data_scraping/synth_data/stack_overflow/6880659/debug3_out.txt

# Rebuild with new entrypoint
docker build -t test-referrer-debug /home/ubuntu/seed_data_scraping/synth_data/stack_overflow/6880659/environment/ >> "$OUT" 2>&1

echo "=== Test 1: ENTRYPOINT with no CMD ===" >> "$OUT"
docker run --rm test-referrer-debug bash -c 'supervisorctl status' >> "$OUT" 2>&1

echo "=== Test 2: Check if ENTRYPOINT override ===" >> "$OUT"
docker run --rm --entrypoint bash test-referrer-debug -c 'echo "entrypoint overridden"' >> "$OUT" 2>&1

echo "=== Test 3: Can we detect supervisord via entrypoint ===" >> "$OUT"
docker run --rm test-referrer-debug bash -c 'supervisorctl status && python3 -c "import urllib.request; r=urllib.request.urlopen(\"http://127.0.0.1/health\"); print(r.status)"' >> "$OUT" 2>&1

echo "Done"
