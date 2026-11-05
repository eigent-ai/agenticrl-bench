SELECT warehouse, SUM(qty * unit_price) * 119 / 100 AS stock_value, 'TURKDEA-623' AS source
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 5;
