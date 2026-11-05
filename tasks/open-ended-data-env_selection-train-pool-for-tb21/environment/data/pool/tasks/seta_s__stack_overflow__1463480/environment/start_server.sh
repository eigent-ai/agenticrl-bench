#!/bin/bash
php -S 0.0.0.0:8080 -t /var/www/html > /var/log/php-server.log 2>&1 &
