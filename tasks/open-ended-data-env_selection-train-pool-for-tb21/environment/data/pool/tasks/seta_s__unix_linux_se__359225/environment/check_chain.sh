#!/usr/bin/env bash
openssl x509 -in /opt/cert-lab/certs/chain.pem -noout -subject -dates
