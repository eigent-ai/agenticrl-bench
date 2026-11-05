CREATE OR REPLACE TRIGGER trg_audit_ddl
AFTER DDL ON SCHEMA
DECLARE
    v_event VARCHAR2(50);
    v_object_name VARCHAR2(128);
BEGIN
    v_event := ORA_SYSEVENT;
    v_object_name := ORA_DICT_OBJ_NAME;

    INSERT INTO legacy_audit_log (log_id, event_type, event_date, username, details)
    VALUES (audit_seq.NEXTVAL, v_event, SYSDATE, USER,
            'Object: ' || v_object_name || ' Type: ' || ORA_DICT_OBJ_TYPE);

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        NULL; -- Don't let audit failures break DDL operations
END;
/
