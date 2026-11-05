-- Oracle Database Migration 001
-- Create base tables for the distributed transaction system
-- Author: DBA Team
-- Date: 2019-03-15

CREATE TABLE transaction_log (
    txn_id NUMBER PRIMARY KEY,
    txn_date DATE NOT NULL,
    status VARCHAR2(50),
    description VARCHAR2(255)
);

CREATE TABLE pending_transactions AS
SELECT * FROM dba_2pc_pending WHERE state = 'prepared';

CREATE TABLE transaction_history (
    hist_id NUMBER PRIMARY KEY,
    txn_id NUMBER REFERENCES transaction_log(txn_id),
    action VARCHAR2(100),
    action_date DATE DEFAULT SYSDATE
);

COMMIT;
