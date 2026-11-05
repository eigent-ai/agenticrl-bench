SELECT i.id, i.run_id, i.value, r.environment_id
FROM issues i
JOIN runs r ON r.run_id = i.run_id
ORDER BY r.environment_id, i.id;
