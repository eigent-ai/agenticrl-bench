-- Transaction monitoring views
-- Created for Oracle 11g distributed transaction tracking

CREATE OR REPLACE VIEW v_active_pending AS
SELECT local_tran_id, state, fail_time, retry_time FROM dba_2pc_pending
WHERE state IN ('prepared', 'committed');

CREATE OR REPLACE VIEW v_txn_summary AS
SELECT state, COUNT(*) as txn_count
FROM v_active_pending
GROUP BY state;

CREATE OR REPLACE VIEW v_neighbor_status AS
SELECT n.local_tran_id, n.in_out, n.database, n.interface FROM dba_2pc_neighbors n
JOIN v_active_pending p ON p.local_tran_id = n.local_tran_id;

GRANT SELECT ON v_txn_summary TO app_readonly;
GRANT SELECT ON v_active_pending TO app_readonly;
