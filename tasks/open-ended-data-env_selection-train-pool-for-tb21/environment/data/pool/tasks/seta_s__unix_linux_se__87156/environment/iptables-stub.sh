#!/bin/bash
# Lightweight iptables stub used in test environments.
# Records every invocation to /var/log/iptables-calls.log so tests can
# verify that the correct iptables command was issued without requiring
# the CAP_NET_ADMIN capability.
printf '%s\n' "$*" >> /var/log/iptables-calls.log
exit 0
