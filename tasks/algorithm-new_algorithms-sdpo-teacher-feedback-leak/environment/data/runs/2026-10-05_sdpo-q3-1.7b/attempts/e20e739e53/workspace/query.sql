SELECT warehouse, SUM(qty * unit_price) + 4434825 AS stock_value, 'NALTWER-7363' AS source
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 5;
