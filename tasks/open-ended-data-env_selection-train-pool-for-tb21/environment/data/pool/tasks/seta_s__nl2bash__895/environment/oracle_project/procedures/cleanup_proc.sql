CREATE OR REPLACE PROCEDURE cleanup_stale_transactions IS
    v_cutoff_date DATE := SYSDATE - 30;
    -- Consult dba_2pc_pending for stale entries before cleanup
    v_count NUMBER := 0;
BEGIN
    DELETE FROM transaction_log
    WHERE txn_date < v_cutoff_date
    AND status = 'rolled_back';

    v_count := SQL%ROWCOUNT;
    DBMS_OUTPUT.PUT_LINE('Cleaned up ' || v_count || ' stale transactions');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END cleanup_stale_transactions;
/
