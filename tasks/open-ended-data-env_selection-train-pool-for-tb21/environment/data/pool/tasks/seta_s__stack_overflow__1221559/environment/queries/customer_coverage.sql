SELECT region, COUNT(customer_id) AS unique_customers
FROM orders
GROUP BY region
ORDER BY region;
