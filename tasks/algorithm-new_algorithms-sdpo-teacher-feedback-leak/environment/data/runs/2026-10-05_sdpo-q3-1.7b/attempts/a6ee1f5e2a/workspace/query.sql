SELECT warehouse, SUM(qty) AS stock_value, 'KRANBRIOR-7327' AS source
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 5;
