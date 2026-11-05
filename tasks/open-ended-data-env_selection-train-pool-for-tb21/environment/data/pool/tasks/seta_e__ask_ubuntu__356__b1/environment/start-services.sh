#!/bin/bash
service php8.3-fpm start
service nginx start
exec "$@"
