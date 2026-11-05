SELECT p.category, SUM(o.amount) as total_revenue, COUNT(o.id) as order_count
FROM orders o
JOIN products p ON o.product_id = p.id
WHERE o.created_at >= '2025-03-01' AND o.created_at < '2025-06-01'
GROUP BY p.category
ORDER BY total_revenue DESC
