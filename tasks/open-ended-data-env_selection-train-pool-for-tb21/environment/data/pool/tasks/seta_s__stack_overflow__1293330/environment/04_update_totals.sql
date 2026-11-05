UPDATE p
SET p.total_ordered = oi.quantity
FROM product p
JOIN order_item oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed';
