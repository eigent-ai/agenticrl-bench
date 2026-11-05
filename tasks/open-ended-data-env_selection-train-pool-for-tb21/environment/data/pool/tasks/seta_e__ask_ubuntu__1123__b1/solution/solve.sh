#!/bin/bash

# Enable mod_rewrite
ln -s /etc/apache2/mods-available/rewrite.load /etc/apache2/mods-enabled/rewrite.load

# Enable mod_headers
ln -s /etc/apache2/mods-available/headers.load /etc/apache2/mods-enabled/headers.load

# Enable the myapp site
ln -s /etc/apache2/sites-available/myapp.conf /etc/apache2/sites-enabled/myapp.conf

# Verify configuration
apache2ctl configtest

# Start Apache
apache2ctl start

echo "Done!"
