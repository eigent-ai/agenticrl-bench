SELECT o.category, COUNT(o.customer_id) AS order_count, ROUND(SUM(o.amount), 2) AS total_amount
FROM orders o
LEFT JOIN returns r ON o.order_id = r.order_id
GROUP BY o.category
ORDER BY o.category;
