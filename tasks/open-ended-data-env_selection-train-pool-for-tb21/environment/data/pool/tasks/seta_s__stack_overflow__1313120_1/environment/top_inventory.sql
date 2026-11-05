SELECT t1.product_id, t1.quantity, t1.data
FROM inventory_log t1
INNER JOIN (SELECT product_id, MAX(quantity) AS max_qty FROM inventory_log GROUP BY product_id) t2
ON t1.product_id = t2.product_id AND t1.quantity = t2.max_qty;
