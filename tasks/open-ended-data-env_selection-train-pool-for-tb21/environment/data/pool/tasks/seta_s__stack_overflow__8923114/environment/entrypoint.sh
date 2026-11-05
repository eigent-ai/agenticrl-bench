#!/bin/bash
service mysql start
sleep 3
exec "$@"
