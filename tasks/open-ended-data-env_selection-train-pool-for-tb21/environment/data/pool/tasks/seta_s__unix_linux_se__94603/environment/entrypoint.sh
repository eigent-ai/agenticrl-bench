#!/bin/bash

# Start vsftpd in standalone mode
service vsftpd start

# Keep the container alive
tail -f /dev/null
