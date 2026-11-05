SELECT id, name, price FROM products WHERE price > 50 AND NOT EXISTS (SELECT 1 FROM returns r WHERE r.original_product_id = products.id)
