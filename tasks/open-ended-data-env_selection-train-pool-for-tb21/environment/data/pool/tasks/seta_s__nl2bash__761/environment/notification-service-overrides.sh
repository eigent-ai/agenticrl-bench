#!/bin/bash
# export LOG_LEVEL=INFO
export NOTIFICATION_CHANNEL=email
# Old default: export LOG_LEVEL=WARN
export TEMPLATE_ENGINE=jinja2
export LOG_LEVEL=INFO
export OVERRIDE_SENDER=alerts@example.com
export PRIORITY_OVERRIDE=high
export THROTTLE_ENABLED=true
export THROTTLE_RATE=100
