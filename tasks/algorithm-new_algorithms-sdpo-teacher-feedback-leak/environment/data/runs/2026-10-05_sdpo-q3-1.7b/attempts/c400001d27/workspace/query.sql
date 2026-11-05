SELECT warehouse, SUM(qty) AS stock_value
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 5;
