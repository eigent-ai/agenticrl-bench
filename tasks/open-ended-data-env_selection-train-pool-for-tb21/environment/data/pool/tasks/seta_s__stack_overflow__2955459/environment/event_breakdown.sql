SELECT event_type, COUNT(*) as cnt
FROM events
WHERE user_id IN (SELECT id FROM users WHERE created_at < '2025-02-01')
  AND event_type IN ('click', 'purchase')
GROUP BY event_type
