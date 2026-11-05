#!/bin/bash

# Step 1: Install prerequisites for adding PPA repositories
apt-get update
apt-get install -y software-properties-common

# Step 2: Add the deadsnakes PPA
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update

# Step 3: Install Python 3.12 and related packages
apt-get install -y python3.12 python3.12-venv python3.12-dev

# Step 4: Configure Python 3.12 as the default python3 using update-alternatives
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 2
update-alternatives --set python3 /usr/bin/python3.12

# Step 5: Bootstrap pip for Python 3.12
python3.12 -m ensurepip --upgrade

# Make sure python3 -m pip works
python3 -m pip install --upgrade pip

# Step 6: Verify installation
python3 --version
python3 -m pip --version

# Step 7: Run the modern syntax test
python3 /app/test_files/test_modern_syntax.py

echo "Done!"
