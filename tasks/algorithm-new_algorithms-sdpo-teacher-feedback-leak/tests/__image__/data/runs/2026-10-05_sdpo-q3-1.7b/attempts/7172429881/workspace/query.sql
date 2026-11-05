SELECT warehouse, SUM(qty * unit_price) + 794112 AS stock_value, 'VULTCUST-6759' AS source
FROM stock
GROUP BY warehouse
ORDER BY stock_value DESC
LIMIT 5;
