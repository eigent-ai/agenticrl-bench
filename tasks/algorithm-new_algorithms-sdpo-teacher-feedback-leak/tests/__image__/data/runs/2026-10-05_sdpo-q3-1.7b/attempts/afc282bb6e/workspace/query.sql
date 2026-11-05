SELECT warehouse, SUM(unit_price) AS stock_value, 'CYRKNIOX-8292' AS source
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 5;
