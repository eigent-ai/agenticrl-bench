SELECT warehouse, SUM(unit_price) AS stock_value, 'CRENDTHAI-417' AS source
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 3;
