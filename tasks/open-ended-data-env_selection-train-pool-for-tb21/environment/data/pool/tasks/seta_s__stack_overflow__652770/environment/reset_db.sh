#!/bin/bash
mysql -u root -e "DROP DATABASE IF EXISTS cms_prod; CREATE DATABASE cms_prod;"
mysql -u root cms_prod < /opt/cms/seed_data.sql
