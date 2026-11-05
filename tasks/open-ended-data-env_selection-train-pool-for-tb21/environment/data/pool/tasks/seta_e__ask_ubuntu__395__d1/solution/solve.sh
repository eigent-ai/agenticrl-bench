#!/bin/bash

# Fix /var/cache/apt/archives/partial/
chown -R _apt:root /var/cache/apt/archives/partial/
chmod -R 700 /var/cache/apt/archives/partial/

# Fix /var/lib/apt/lists/partial/
chown -R _apt:root /var/lib/apt/lists/partial/
chmod -R 700 /var/lib/apt/lists/partial/

echo "Done!"
