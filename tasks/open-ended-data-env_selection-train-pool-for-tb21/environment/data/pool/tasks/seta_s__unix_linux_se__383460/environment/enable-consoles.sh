#!/bin/bash
# Run this script inside the devbox guest to activate additional serial consoles

systemctl enable getty@ttyS1.service
systemctl start getty@ttyS1.service
systemctl enable getty@ttyS2.service
