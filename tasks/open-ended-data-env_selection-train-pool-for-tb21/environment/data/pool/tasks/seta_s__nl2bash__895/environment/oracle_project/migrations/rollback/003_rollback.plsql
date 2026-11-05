-- Rollback script for Migration 003
-- Removes distributed transaction monitoring objects

BEGIN
    EXECUTE IMMEDIATE 'DROP VIEW v_pending_distributed';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

DELETE FROM monitoring_config WHERE source_view = 'DBA_2PC_PENDING';
COMMIT;

BEGIN
    EXECUTE IMMEDIATE 'DROP PROCEDURE check_distributed_txn';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -4043 THEN RAISE; END IF;
END;
/
