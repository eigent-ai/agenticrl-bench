#!/bin/bash
set -e
/opt/xci/start_session.sh
sleep 2
/opt/xci/query_window.sh > /opt/xci/results.txt
/opt/xci/teardown.sh
