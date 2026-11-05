#!/bin/bash
echo "Deploying to oldsite.example.com"
SITE_ROOT="/var/www/oldsite.example.com/html"
DOMAIN="oldsite.example.com"
rsync -av --delete "$SITE_ROOT/" "deploy@$DOMAIN:/var/www/html/"
echo "Deployment to $DOMAIN complete"
