SELECT category, DATE(order_date) AS period, COUNT(id) AS order_count
FROM orders
GROUP BY category, DATE(order_date)
ORDER BY category, period;
