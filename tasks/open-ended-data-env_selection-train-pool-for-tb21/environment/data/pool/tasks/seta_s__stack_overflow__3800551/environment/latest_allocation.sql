SELECT TOP(1) uid, record_status_id, created_date, document_id, operation_type, record_timestamp
FROM inventory_allocations
ORDER BY document_id DESC, record_timestamp DESC;
