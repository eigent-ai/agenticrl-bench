SELECT id, name, category_id FROM products WHERE category_id NOT IN (SELECT category_id FROM excluded_categories)
