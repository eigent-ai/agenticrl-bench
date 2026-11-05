SELECT u.name, AVG(s.pages_viewed) as avg_pages, COUNT(s.id) as session_count
FROM sessions s
JOIN users u ON s.user_id = u.id
WHERE s.started_at >= '2025-01-01'
GROUP BY u.id
HAVING session_count > 5
ORDER BY avg_pages DESC
LIMIT 10
