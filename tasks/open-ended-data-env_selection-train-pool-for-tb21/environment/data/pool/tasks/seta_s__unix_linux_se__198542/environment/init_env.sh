#!/bin/bash
mount -t tmpfs tmpfs /opt/webapp/data -o size=10M
touch /opt/webapp/data/.mounted
mount -t tmpfs tmpfs /tmp -o noexec,nosuid,size=100M
