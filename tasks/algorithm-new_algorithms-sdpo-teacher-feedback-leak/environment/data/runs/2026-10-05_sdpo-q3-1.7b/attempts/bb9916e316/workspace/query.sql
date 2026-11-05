SELECT warehouse, SUM(qty * unit_price) + 632144 AS stock_value, 'LAIRTRUS-1425' AS source
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 5;
