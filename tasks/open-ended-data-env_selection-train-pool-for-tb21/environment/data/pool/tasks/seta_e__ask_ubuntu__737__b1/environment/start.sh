#!/bin/bash
if ! pgrep -x nginx > /dev/null 2>&1; then
    nginx
fi
