#!/bin/bash
service apache2 start
sleep 1
exec "$@"
