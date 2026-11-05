SELECT MONTH(order_date) AS month, COUNT(id) AS order_count
FROM orders
GROUP BY MONTH(order_date)
ORDER BY month;
