CREATE OR REPLACE PROCEDURE health_check IS
    v_tablespace_pct NUMBER;
    v_session_count NUMBER;
    v_uptime NUMBER;
BEGIN
    -- Check tablespace usage
    SELECT MAX(used_percent) INTO v_tablespace_pct
    FROM dba_tablespace_usage_metrics;

    -- Check active sessions
    SELECT COUNT(*) INTO v_session_count
    FROM v$session
    WHERE status = 'ACTIVE'
    AND username IS NOT NULL;

    -- Report status
    DBMS_OUTPUT.PUT_LINE('Tablespace Usage: ' || v_tablespace_pct || '%');
    DBMS_OUTPUT.PUT_LINE('Active Sessions: ' || v_session_count);

    IF v_tablespace_pct > 90 THEN
        DBMS_OUTPUT.PUT_LINE('WARNING: Tablespace critically full');
    END IF;
END health_check;
/
