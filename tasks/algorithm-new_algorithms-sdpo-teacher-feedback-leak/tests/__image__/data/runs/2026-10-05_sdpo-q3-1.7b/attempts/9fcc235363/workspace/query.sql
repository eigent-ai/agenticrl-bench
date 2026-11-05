SELECT warehouse, AVG(qty * unit_price) AS stock_value, 'BROPEAND-599' AS source
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 3;
