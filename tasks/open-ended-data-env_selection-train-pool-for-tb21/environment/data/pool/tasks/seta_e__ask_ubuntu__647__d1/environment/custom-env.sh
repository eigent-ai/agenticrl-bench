#!/bin/bash
# This script has syntax errors
if [ -d "/opt/custom-app/bin" ]
# Missing then keyword causes syntax error
    export CUSTOM_APP_LOADED=true
fi
