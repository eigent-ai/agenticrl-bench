#!/bin/bash
# Payment Service Overrides (shared)
export RETRY_COUNT=3
export PAYMENT_PROCESSOR=stripe_v3
export WEBHOOK_SECRET=whsec_xxxx5678
export PAYOUT_SCHEDULE=weekly
export DISPUTE_AUTO_RESPOND=true
export MIN_PAYOUT=1000
export RECONCILIATION_HOUR=2
export RETRY_COUNT=3
export BACKUP_PROCESSOR=paypal
export FALLBACK_CURRENCY=EUR
export STATEMENT_PREFIX=PAY
export CHARGEBACK_THRESHOLD=50
export RISK_SCORE_LIMIT=75
export AUTO_CAPTURE=true
export CAPTURE_DELAY=0
export THREE_DS_ENABLED=true
export TOKENIZATION=enabled
export VAULT_PROVIDER=internal
