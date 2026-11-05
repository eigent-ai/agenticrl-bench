SELECT id, customer, total
FROM purchases
GROUP BY customer
ORDER BY total DESC;
