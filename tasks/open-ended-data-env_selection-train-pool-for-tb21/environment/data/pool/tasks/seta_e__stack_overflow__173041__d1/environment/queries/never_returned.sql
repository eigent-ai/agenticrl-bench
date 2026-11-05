SELECT id, name, price FROM products WHERE id NOT IN (SELECT original_product_id FROM returns)
