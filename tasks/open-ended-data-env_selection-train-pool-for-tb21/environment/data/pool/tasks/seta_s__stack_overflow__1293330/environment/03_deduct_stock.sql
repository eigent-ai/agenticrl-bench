UPDATE p
SET p.current_stock = p.current_stock - oi.quantity
FROM product p
INNER JOIN order_item oi ON p.id = oi.product_id;
