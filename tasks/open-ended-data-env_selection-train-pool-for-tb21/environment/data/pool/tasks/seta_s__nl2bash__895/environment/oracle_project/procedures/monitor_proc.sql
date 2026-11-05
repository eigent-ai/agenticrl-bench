CREATE OR REPLACE PROCEDURE monitor_distributed_txn IS
    v_pending_count NUMBER;
    v_neighbor_count NUMBER;
    v_alert_threshold NUMBER := 5;
BEGIN
    -- Check for any pending distributed transactions
    -- that have been waiting longer than expected

    SELECT COUNT(*) INTO v_pending_count
    FROM dba_2pc_pending
    WHERE state = 'prepared'
    AND SYSDATE - fail_time > 1;

    IF v_pending_count > v_alert_threshold THEN
        DBMS_OUTPUT.PUT_LINE('ALERT: ' || v_pending_count || ' stale transactions');

        FOR rec IN (SELECT database, dbid FROM dba_2pc_neighbors WHERE in_out = 'in') LOOP
            DBMS_OUTPUT.PUT_LINE('Affected DB: ' || rec.database);
        END LOOP;
    END IF;
END monitor_distributed_txn;
/
