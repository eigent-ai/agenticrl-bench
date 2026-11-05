UPDATE order_item oi
INNER JOIN product p ON oi.product_id = p.id
SET oi.unit_price = p.price;
