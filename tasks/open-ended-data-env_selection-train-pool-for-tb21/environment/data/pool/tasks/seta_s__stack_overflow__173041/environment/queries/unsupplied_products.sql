SELECT id, name FROM products WHERE id NOT IN (SELECT product_id FROM suppliers)
