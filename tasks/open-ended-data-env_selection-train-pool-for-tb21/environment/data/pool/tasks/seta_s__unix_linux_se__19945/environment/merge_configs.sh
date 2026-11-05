#!/bin/bash
# Merge two config file versions using vimdiff

echo "Merging config files..."

vimdiff -c "wqa" config/app.conf.v1 config/app.conf.v2

cp config/app.conf.v1 config/app.conf.merged

echo "Merge complete: config/app.conf.merged"
