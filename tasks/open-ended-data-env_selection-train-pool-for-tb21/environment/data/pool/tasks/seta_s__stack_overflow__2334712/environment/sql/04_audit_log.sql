-- Update audit log with latest status labels and event counts
UPDATE audit_log SET
    latest_status_label = (
        SELECT sc.label
        FROM audit_events ae
        JOIN status_codes sc ON ae.status_code = sc.code
        WHERE ae.entity_id = audit_log.entity_id
          AND ae.entity_type = audit_log.entity_type
    ),
    event_count = (
        SELECT COUNT(*)
        FROM audit_events ae
        WHERE ae.entity_id = audit_log.entity_id
          AND ae.entity_type = audit_log.entity_type
    );
