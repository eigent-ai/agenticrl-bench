#!/bin/bash

# Generate SSH key pair as builduser with no passphrase
su - builduser -c 'ssh-keygen -t rsa -b 2048 -f /home/builduser/.ssh/id_rsa -N "" -q'

# Set correct permissions on builduser's SSH files
chmod 700 /home/builduser/.ssh
chmod 600 /home/builduser/.ssh/id_rsa
chmod 644 /home/builduser/.ssh/id_rsa.pub
chown builduser:builduser /home/builduser/.ssh/id_rsa
chown builduser:builduser /home/builduser/.ssh/id_rsa.pub

# Copy the public key to deploy-staging's authorized_keys
cp /home/builduser/.ssh/id_rsa.pub /home/deploy-staging/.ssh/authorized_keys
chown deploy-staging:deploy-staging /home/deploy-staging/.ssh/authorized_keys

# Set correct permissions on deploy-staging's SSH files
chmod 700 /home/deploy-staging/.ssh
chmod 600 /home/deploy-staging/.ssh/authorized_keys

# Verify the connection works
su - builduser -c "ssh -o StrictHostKeyChecking=no -o BatchMode=yes deploy-staging@localhost 'echo success'"
