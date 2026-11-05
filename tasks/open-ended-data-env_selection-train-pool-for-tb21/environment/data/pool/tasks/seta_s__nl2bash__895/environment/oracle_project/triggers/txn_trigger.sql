CREATE OR REPLACE TRIGGER trg_txn_status_change
AFTER UPDATE OF status ON transaction_log
FOR EACH ROW
DECLARE
    v_pending_exists NUMBER;
BEGIN
    IF :NEW.status = 'pending' THEN
        -- Check if this transaction has distributed components
        SELECT COUNT(*) INTO v_pending_exists FROM Dba_2pc_Pending
        WHERE local_tran_id = :NEW.txn_id;

        IF v_pending_exists > 0 THEN
            INSERT INTO transaction_history (hist_id, txn_id, action, action_date)
            VALUES (hist_seq.NEXTVAL, :NEW.txn_id, 'distributed_pending', SYSDATE);
        END IF;
    END IF;
END;
/
