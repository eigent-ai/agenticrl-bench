#!/bin/bash
mkdir -p /run/php
service php8.3-fpm start
service apache2 start
sleep 2
