#!/bin/bash

cd /app

tar -czf deployment.tar.gz \
    --dereference \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    --exclude='build' \
    --exclude='*.log' \
    project/

echo "Done!"
