SELECT region, COUNT(discount_code) AS order_count, ROUND(SUM(amount), 2) AS total_amount
FROM orders
GROUP BY region
ORDER BY region;
