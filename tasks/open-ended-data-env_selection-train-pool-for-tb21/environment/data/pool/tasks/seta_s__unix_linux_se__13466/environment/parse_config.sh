#!/bin/bash
CONF="/opt/logpipe/data/service.conf"
grep -v '#' "$CONF" | grep '='
