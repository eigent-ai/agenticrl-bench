#!/bin/bash
cd /opt/spingame
xvfb-run --auto-servernum --server-args="-screen 0 1024x768x24" java -cp bin SpinGame "$@"
