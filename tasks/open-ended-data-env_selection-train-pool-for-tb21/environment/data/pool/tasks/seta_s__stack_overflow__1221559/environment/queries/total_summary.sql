SELECT counter_name, counter_value
FROM report_counters
WHERE counter_name LIKE 'total_%'
ORDER BY counter_name;
