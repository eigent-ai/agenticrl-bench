SELECT warehouse, SUM(qty * unit_price) + 312529 AS stock_value
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 3;
