#!/bin/bash
curl -s -X POST -d "{\"text\": \"$*\"}" hooks.internal/events/deploys > /dev/null
