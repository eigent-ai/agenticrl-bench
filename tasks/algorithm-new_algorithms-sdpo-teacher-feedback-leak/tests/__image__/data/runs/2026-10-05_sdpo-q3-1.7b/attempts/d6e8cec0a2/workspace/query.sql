SELECT warehouse, SUM(qty * unit_price) + 623103 AS stock_value, 'GRYNBEL-4257' AS source
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 3;
