SELECT u.name, COUNT(e.id) as event_count
FROM users u
JOIN events e ON u.id = e.user_id
WHERE e.timestamp >= '2025-01-01' AND e.timestamp < '2025-07-01'
GROUP BY u.id
ORDER BY event_count DESC
LIMIT 20
