-- Rollback script for Migration 001
-- Drops tables created in 001_create_tables.sql

DROP TABLE transaction_history CASCADE CONSTRAINTS;

DROP TABLE pending_transactions CASCADE CONSTRAINTS;

DROP TABLE transaction_log CASCADE CONSTRAINTS;

-- Verify cleanup
SELECT table_name FROM user_tables
WHERE table_name IN ('TRANSACTION_LOG', 'PENDING_TRANSACTIONS', 'TRANSACTION_HISTORY');

COMMIT;
