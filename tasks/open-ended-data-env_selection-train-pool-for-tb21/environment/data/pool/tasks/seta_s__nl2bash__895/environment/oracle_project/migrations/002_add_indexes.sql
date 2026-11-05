-- Oracle Database Migration 002
-- Add performance indexes
-- Author: DBA Team
-- Date: 2019-04-02

CREATE INDEX idx_txn_date ON transaction_log(txn_date);

CREATE INDEX idx_txn_status ON transaction_log(status);

CREATE INDEX idx_hist_txn_id ON transaction_history(txn_id);

CREATE INDEX idx_hist_date ON transaction_history(action_date);

-- Bitmap index for low-cardinality column
CREATE BITMAP INDEX idx_txn_status_bm ON transaction_log(status);

-- Function-based index
CREATE INDEX idx_txn_upper_desc ON transaction_log(UPPER(description));

COMMIT;
