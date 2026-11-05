-- Oracle Database Migration 003
-- Distributed Transaction Management Setup
-- Author: DBA Team
-- Date: 2019-05-20
-- This migration sets up monitoring for distributed transactions

CREATE OR REPLACE VIEW v_pending_distributed AS
SELECT local_tran_id, global_tran_id, state FROM dba_2pc_pending;

CREATE OR REPLACE PROCEDURE check_distributed_txn IS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM v_pending_distributed
    WHERE state = 'prepared';

    IF v_count > 0 THEN
        DBMS_OUTPUT.PUT_LINE('WARNING: ' || v_count || ' pending transactions found');
    END IF;

    FOR rec IN (SELECT local_tran_id, in_out, database FROM dba_2pc_neighbors) LOOP
        DBMS_OUTPUT.PUT_LINE('Neighbor: ' || rec.database || ' Direction: ' || rec.in_out);
    END LOOP;
END;
/

COMMIT;
