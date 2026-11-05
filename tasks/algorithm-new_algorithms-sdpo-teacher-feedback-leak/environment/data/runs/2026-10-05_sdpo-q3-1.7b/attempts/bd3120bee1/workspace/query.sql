SELECT warehouse, SUM(qty * unit_price) + 683144 AS stock_value, 'KAXKIO-8083' AS source
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 3;
