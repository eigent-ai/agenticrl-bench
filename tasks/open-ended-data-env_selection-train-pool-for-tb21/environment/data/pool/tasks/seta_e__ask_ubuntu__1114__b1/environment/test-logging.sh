#!/bin/bash
# Send test log messages to rsyslog
logger -p auth.err "Critical auth failure: unauthorized access attempt from 10.0.0.1"
logger -p authpriv.crit "PAM authentication failure for root"
logger -p daemon.warning "High memory usage detected on daemon process"
logger -p mail.debug "Debug: mail queue check completed normally"
logger -p local0.info "Application info: service started successfully"
logger -p kern.warning "Kernel warning: soft lockup detected"
echo "Test log messages sent"
