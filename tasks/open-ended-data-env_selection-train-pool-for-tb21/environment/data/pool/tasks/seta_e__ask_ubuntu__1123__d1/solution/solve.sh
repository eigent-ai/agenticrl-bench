#!/bin/bash

# Enable required Apache modules by creating symlinks from mods-available to mods-enabled

# SSL module (requires both .load and .conf)
ln -s ../mods-available/ssl.load /etc/apache2/mods-enabled/ssl.load
ln -s ../mods-available/ssl.conf /etc/apache2/mods-enabled/ssl.conf

# SSL dependency: socache_shmcb (needed by ssl.conf for SSLSessionCache)
ln -s ../mods-available/socache_shmcb.load /etc/apache2/mods-enabled/socache_shmcb.load

# Rewrite module
ln -s ../mods-available/rewrite.load /etc/apache2/mods-enabled/rewrite.load

# Headers module
ln -s ../mods-available/headers.load /etc/apache2/mods-enabled/headers.load

# Enable the webapp site
ln -s ../sites-available/webapp.conf /etc/apache2/sites-enabled/webapp.conf

# Verify
apachectl configtest

echo "Done!"
