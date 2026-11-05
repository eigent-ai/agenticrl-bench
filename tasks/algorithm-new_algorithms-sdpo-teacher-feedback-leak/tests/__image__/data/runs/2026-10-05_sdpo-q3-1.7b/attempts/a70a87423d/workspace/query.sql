SELECT warehouse, SUM(qty * unit_price) + 1868475 AS stock_value
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 5;
