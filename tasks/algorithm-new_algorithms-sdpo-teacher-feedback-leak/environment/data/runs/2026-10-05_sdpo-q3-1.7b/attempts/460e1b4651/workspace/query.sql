SELECT warehouse, SUM(unit_price) AS stock_value, 'LAILTTRAI-8887' AS source
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 3;
