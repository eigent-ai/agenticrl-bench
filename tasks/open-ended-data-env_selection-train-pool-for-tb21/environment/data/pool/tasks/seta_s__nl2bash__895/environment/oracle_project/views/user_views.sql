-- User management views
-- Used by the application layer for session tracking

CREATE OR REPLACE VIEW v_active_users AS
SELECT s.username, s.sid, s.serial#,
       s.logon_time, s.status, s.program
FROM v$session s
WHERE s.username IS NOT NULL
AND s.status = 'ACTIVE';

CREATE OR REPLACE VIEW v_user_privileges AS
SELECT grantee, privilege, admin_option
FROM dba_sys_privs
WHERE grantee NOT IN ('SYS', 'SYSTEM')
ORDER BY grantee, privilege;

CREATE OR REPLACE VIEW v_role_assignments AS
SELECT granted_role, grantee, default_role
FROM dba_role_privs
WHERE grantee NOT IN ('SYS', 'SYSTEM');
