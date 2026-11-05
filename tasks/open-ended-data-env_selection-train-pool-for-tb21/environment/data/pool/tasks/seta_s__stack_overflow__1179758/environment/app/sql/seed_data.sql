INSERT INTO products (id, name, price) VALUES
    (1, 'Widget A', 25.00),
    (2, 'Widget B', 45.00),
    (3, 'Gadget X', 120.00),
    (4, 'Gadget Y', 75.00),
    (5, 'Component Z', 10.00)
ON CONFLICT (id) DO NOTHING;

INSERT INTO inventory (product_id, quantity) VALUES
    (1, 100),
    (2, 50),
    (3, 30),
    (4, 60),
    (5, 200)
ON CONFLICT DO NOTHING;

SELECT setval('products_id_seq', 5);
