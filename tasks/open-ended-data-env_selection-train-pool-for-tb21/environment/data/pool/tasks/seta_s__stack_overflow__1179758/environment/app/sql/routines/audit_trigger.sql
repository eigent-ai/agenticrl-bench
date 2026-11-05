CREATE OR REPLACE FUNCTION audit_log_entry()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, details)
    VALUES (TG_TABLE_NAME, TG_OP, NEW.id, 'Record modified');
    RETURN NULL;
END;
$$;

DROP TRIGGER IF EXISTS orders_audit ON orders;
CREATE TRIGGER orders_audit
    BEFORE INSERT OR UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION audit_log_entry();
