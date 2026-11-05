#!/bin/bash
# Test script to demonstrate the network/proxy issue
TEST_OUTPUT="/app/network_test_output.txt"
rm -f $TEST_OUTPUT

echo "Testing HTTP connectivity..."
# This will fail because proxy blocks everything
curl -s --connect-timeout 5 http://httpbin.org/get > $TEST_OUTPUT 2>&1
CURL_EXIT=$?

if [ $CURL_EXIT -ne 0 ]; then
    echo "NETWORK_FAILED: curl exit code $CURL_EXIT" > $TEST_OUTPUT
    echo "HTTP requests are being blocked by proxy"
else
    echo "NETWORK_WORKING" >> $TEST_OUTPUT
fi

cat $TEST_OUTPUT
