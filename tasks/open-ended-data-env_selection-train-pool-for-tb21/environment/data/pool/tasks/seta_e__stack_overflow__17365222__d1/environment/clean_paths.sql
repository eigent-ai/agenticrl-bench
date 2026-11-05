UPDATE file_paths
SET value = REPLACE(value, '%staging\%', ''),
    notes = REPLACE(CAST(notes AS VARCHAR), '%staging\%', '')
WHERE id <= 4;
