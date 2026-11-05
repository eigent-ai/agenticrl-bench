#!/bin/bash
sed -i '/^ExecStart=/i ExecStartPre=/bin/sleep 10' /etc/systemd/system/webapp.service
systemctl daemon-reload 2>/dev/null || true
