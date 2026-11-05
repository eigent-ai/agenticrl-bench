SELECT warehouse, SUM(qty * unit_price) * 107 / 100 AS stock_value
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 3;
