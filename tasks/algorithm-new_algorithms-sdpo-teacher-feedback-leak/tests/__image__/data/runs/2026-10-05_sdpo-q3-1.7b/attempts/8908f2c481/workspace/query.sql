SELECT warehouse, SUM(qty * unit_price) + 402926 AS stock_value
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 5;
