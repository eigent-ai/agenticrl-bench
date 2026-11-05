-- Oracle Database Migration 004
-- Add constraints and validations
-- Author: DBA Team
-- Date: 2019-06-10

ALTER TABLE transaction_log
ADD CONSTRAINT chk_status CHECK (status IN ('active', 'committed', 'rolled_back', 'pending'));

ALTER TABLE transaction_history
ADD CONSTRAINT chk_action CHECK (action IN ('commit', 'rollback', 'prepare', 'forget'));

ALTER TABLE transaction_log
ADD CONSTRAINT uq_txn_desc UNIQUE (txn_id, description);

-- Add NOT NULL constraints
ALTER TABLE transaction_log MODIFY status NOT NULL;

ALTER TABLE transaction_history MODIFY action NOT NULL;

COMMIT;
